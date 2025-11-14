from flask import Flask, render_template, request, jsonify, session
from flask_pymongo import PyMongo
from beam_logic import (
    calculate_all,
    get_material_properties,
    rectangular_section,
    stress_check,
    calculate_loads, 
    factored_loads,

)
from suggestions import (
    suggest_fix_for_stress_warning,
    suggest_fix_for_deflection_warning,
    langchain_suggestions,
    langchain_error_explanation,
)
from chatbot import structural_chatbot_response
import numpy as np
import datetime
import traceback
import uuid
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# 🔌 MongoDB connection - uses environment variable or defaults to local
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/beamdb")
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# 🔥 Firebase Admin initialization (optional - only if FIREBASE_CREDENTIALS is set)
firebase_initialized = False
firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
if firebase_creds:
    try:
        import json
        # Check if it's a JSON string or file path
        if firebase_creds.startswith("{") or firebase_creds.startswith("["):
            # It's a JSON string
            cred_dict = json.loads(firebase_creds)
            cred = credentials.Certificate(cred_dict)
        else:
            # It's a file path
            cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
        firebase_initialized = True
        print("✅ Firebase Admin initialized successfully")
    except Exception as e:
        print(f"⚠️ Firebase initialization failed: {e}")
        print("   Continuing without Firebase authentication verification")

def safe_float(value, default=0.0):
    try:
        if isinstance(value, list):
            value = value[0]
        return float(value)
    except (ValueError, TypeError):
        return default

@app.route('/')
def index():
    return render_template('index.html', show_modal=True)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        print("✅ Form submitted")
        form = request.form
        load_type = form.get("loadType", "")
        building_type = form.get("buildingType", "residential")
        length = safe_float(form.get("length")) 

        params = {k: v if isinstance(v, str) else v[0] for k, v in form.items()}
        print(f"📥 Received params: {params}")

        b = safe_float(params.get("b")) / 1000 
        d = safe_float(params.get("d")) / 1000 

        material_key = params.get("material", "M20")
        material = get_material_properties(material_key)
        E_modulus = material.get("E", 25e9) 

        if load_type == "udl":
            w = safe_float(params.get("w")) * 1000 
            params["w"] = w
        elif load_type in ["point_center", "point_anywhere"]:
            P = safe_float(params.get("P")) * 1000
            params["P"] = P
        elif load_type == "uvl":
            w_max = safe_float(params.get("w_max")) * 1000 
            params["w_max"] = w_max
        elif load_type == "moment":
            M_applied = safe_float(params.get("M_applied")) * 1000 
            params["M_applied"] = M_applied

        section = rectangular_section(b, d)

        val = 0.0
        if load_type == "udl":
            val = params.get("w", 0)
        elif load_type in ["point_center", "point_anywhere"]:
            val = params.get("P", 0)
        elif load_type == "uvl":
            val = params.get("w_max", 0)
        elif load_type == "moment":
            val = params.get("M_applied", 0)

        results = None
        dl = il = wl = None

        if request.method == "POST":
            limit_state = request.form.get("limit_state")

            # Inputs
            length = safe_float(request.form.get("length"))
            b = safe_float(request.form.get("b")) / 1000  # convert mm→m
            d = safe_float(request.form.get("d")) / 1000
            P = safe_float(request.form.get("P"))
            w = safe_float(request.form.get("w"))
            w_max = safe_float(request.form.get("w_max"))
            M_applied = safe_float(request.form.get("M_applied"))

            # Calculate loads
            dl, il, wl = calculate_loads(length, b, d, P, w, w_max, M_applied)

            # Factored loads
            results = factored_loads(limit_state, dl, il, wl)
        
        volume_concrete = b * d * length 
        steel_weight = volume_concrete * 120 
        cost_concrete = volume_concrete * 6000 
        cost_steel = steel_weight * 65 
        binding_wire_weight = steel_weight * 0.01
        binding_wire_cost = binding_wire_weight * 72
        total_cost = cost_concrete + cost_steel + binding_wire_cost

        R1, R2, M_max, x_vals, V_vals, M_vals, deflection_vals, max_deflection = calculate_all(
            length, load_type, params, E=E_modulus, I=section["I"]
        )
        # R1, R2, M_max, delta_max, x_vals, V_vals, M_vals, deflection_vals = calculate_all(length, load_type, params)
        
        stress, stress_ok = stress_check(M_max * 1e6, section["Z"] * 1e9, material.get("fck", 0))
        stress = round(stress, 2)
        stress_warning = stress_fix = ""
        if not stress_ok:
            stress_warning = "⚠️ Warning: stress exceeds allowable limit!"
            stress_fix = suggest_fix_for_stress_warning(stress, material_key)

        stress_ratio = round(stress / material.get("fck", 1), 2)

        stress_profile = {
            "depths": np.linspace(0, d * 1000, 10).tolist(),
            "stresses": np.linspace(0, stress, 10).tolist()
        }

        deflection = max_deflection
        deflection_limit = length * 1000 / 250 
        deflection_ok = deflection <= deflection_limit

        deflection_warning = deflection_fix = ""
        if not deflection_ok:
            deflection_warning = f"⚠️ Warning: Deflection {round(deflection, 2)} mm exceeds limit of {round(deflection_limit, 2)} mm."
            deflection_fix = suggest_fix_for_deflection_warning(deflection, deflection_limit)

        deflection_ratio = round(deflection / deflection_limit, 2)

        # Disable AI calls temporarily to prevent timeouts on Render free tier
        # AI features can be re-enabled when upgrading to paid plan
        ai_error_explanation = ""
        ai_response = ""
        
        # Uncomment below to enable AI (requires paid Render plan):
        # try:
        #     if not stress_ok or not deflection_ok:
        #         ai_error_explanation = langchain_error_explanation(...)
        # except Exception as e:
        #     print(f"⚠️ AI error explanation failed: {e}")
        #     ai_error_explanation = "AI explanation temporarily unavailable."

        beam_data = {
            "_id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow(),
            "length": length,
            "loadType": load_type,
            "P": safe_float(params.get("P")),
            "a": safe_float(params.get("a")),
            "w": safe_float(params.get("w")),
            "w_max": safe_float(params.get("w_max")),
            "M_applied": safe_float(params.get("M_applied")),
            "b": b * 1000,
            "d": d * 1000,
            "material": material_key,
            "results": {
                "R1": R1,
                "R2": R2,
                "M_max": M_max,
                "max_deflection": max_deflection,
                "stress": stress,
                "stress_ok": stress_ok,
                "deflection_ok": deflection_ok,
                "stress_ratio": stress_ratio,
                "deflection_ratio": deflection_ratio
            },
            "cost": {
                "volume_concrete": volume_concrete,
                "steel_weight": steel_weight,
                "cost_concrete": cost_concrete,
                "cost_steel": cost_steel,
                "binding_wire_cost": binding_wire_cost,
                "total_cost": total_cost
            }
        }

        # 💾 Save beam_data to MongoDB (wrapped in try/except to prevent crashes)
        try:
            mongo.db.projects.insert_one(beam_data)
        except Exception as e:
            print(f"⚠️ MongoDB save failed (non-critical): {e}")
            # Continue without saving - calculation results still work

        return render_template('index.html',
                               R1=round(R1, 2),
                               R2=round(R2, 2),
                               M_max=M_max,
                               x_vals=x_vals,
                               V_vals=V_vals,
                               M_vals=M_vals,
                               deflection_vals=deflection_vals,
                               stress=stress,
                               stress_ok="✅ OK" if stress_ok else "❌ Exceeds Limit",
                               stress_warning=stress_warning,
                               stress_fix=stress_fix,
                               deflection=round(deflection, 2),
                               deflection_ok="✅ OK" if deflection_ok else "❌ Exceeds Limit",
                               deflection_warning=deflection_warning,
                               deflection_fix=deflection_fix,
                               results=results,
                               dl=dl,
                               il=il,
                               wl=wl,
                               building_type=building_type,
                               stress_profile=stress_profile,
                               ai_response=ai_response,
                               volume_concrete=round(volume_concrete, 3),
                               steel_weight=round(steel_weight, 1),
                               cost_concrete=int(cost_concrete),
                               cost_steel=int(cost_steel),
                               total_cost=int(total_cost),
                               binding_wire_weight=round(binding_wire_weight, 2),
                               binding_wire_rate=72,
                               binding_wire_cost=int(binding_wire_cost),
                               ai_error_explanation=ai_error_explanation,
                               beam_data=beam_data,
                               stress_ratio=stress_ratio,
                               deflection_ratio=deflection_ratio
                               )

    except Exception as e:
        print("❌ ERROR:", e)
        traceback.print_exc()
        return render_template('index.html', error=f"Calculation Error: {e}")

@app.route("/verify_token", methods=["POST"])
def verify_token():
    """Verify Firebase ID token"""
    try:
        data = request.get_json()
        id_token = data.get("idToken")
        
        if not id_token:
            return jsonify({"error": "No token provided"}), 400
        
        if firebase_initialized:
            # Verify the token using Firebase Admin SDK
            decoded_token = auth.verify_id_token(id_token)
            session["user_id"] = decoded_token["uid"]
            session["user_email"] = decoded_token.get("email", "")
            return jsonify({"success": True, "uid": decoded_token["uid"]})
        else:
            # If Firebase Admin is not configured, just accept the token
            # (for development/testing purposes)
            session["user_id"] = "dev_user"
            session["user_email"] = "dev@example.com"
            return jsonify({"success": True, "message": "Token accepted (dev mode)"})
    except Exception as e:
        print(f"Token verification error: {e}")
        return jsonify({"error": "Token verification failed"}), 401

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_query = data.get("message", "")
        if not user_query:
            return jsonify({"response": "Please enter a valid question."})
        
        # Temporarily disable AI chatbot on free tier to prevent timeouts
        # Return a simple response instead
        return jsonify({
            "response": "AI chatbot is temporarily disabled on the free tier to ensure reliable calculations. Please upgrade to a paid plan for AI features, or use the calculation results which work perfectly!"
        })
        
        # Uncomment below to enable AI chatbot (requires paid Render plan):
        # response = structural_chatbot_response(user_query)
        # return jsonify({"response": response})
    except Exception as e:
        print("Chatbot Error:", e)
        return jsonify({"response": "Sorry, the assistant is currently unavailable."})

# 🧾 Optional API: Get all saved projects
@app.route("/get_projects", methods=["GET"])
def get_projects():
    projects = list(mongo.db.projects.find({}, {"_id": 0}))
    return jsonify(projects)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
