import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Don't raise error - allow app to work without AI
llm = None
if GROQ_API_KEY and GROQ_API_KEY != "your-groq-api-key":
    try:
        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            temperature=0.2,
            model="openai/gpt-oss-120b",
            timeout=10  # 10 second timeout
        )
    except Exception as e:
        print(f"⚠️ Failed to initialize Groq LLM: {e}")
        llm = None
else:
    print("⚠️ GROQ_API_KEY not found. AI features disabled.")

# Prompt template of AI Structural advisor 
template = """
You are a structural engineering assistant. Based on the inputs below, provide *point-wise* engineering suggestions. 
Do **not include any calculations or equations**.

Inputs:
- Building Type: {building_type}
- Beam Length: {length} m
- Load Type: {load_type}
- Load Value: {load_value} kN/m or kN

Provide the following in numbered format:
Respond using the following emoji tags and preserve them in the output:

1. 🔄 Suggested load distribution (Dead Load - DL, Live Load - LL)
2. 📏 Recommended beam dimensions (width b × depth d in mm)
3. ⚠️ Any warnings about stress or deflection limits being exceeded
4. 🛠️ Fixes or recommendations if limits are likely to be exceeded
5. 📚 Include a short explanation for each recommendation
6. 📋 Check the beam or column design for compliance with IS 456:2000 or ACI 318. Validate minimum and maximum reinforcement, spacing, and cover. Report any violations.

Keep the output concise and professional. Use line breaks for clarity where needed.
"""

prompt = ChatPromptTemplate.from_template(template)

def langchain_suggestions(building_type, length, load_type, load_value):
    """Generate AI-based suggestions via LangChain and Groq."""
    if not llm:
        return "AI suggestions temporarily disabled. Calculation results work perfectly!"
    
    try:
        chain = prompt | llm
        response = chain.invoke({
            "building_type": building_type,
            "length": length,
            "load_type": load_type,
            "load_value": load_value/1000
        })
        return response.content.strip()
    except Exception as e:
        print(f"LangChain suggestions error: {e}")
        return "AI suggestions temporarily unavailable. Calculation results work perfectly!"


# Engineering Heuristics-Based Functions


# def suggest_loads_by_building_type(building_type):
#     """Returns standard DL/LL suggestions."""
#     standard_loads = {
#         "residential": {"DL": 2.5, "LL": 2.0},
#         "office": {"DL": 3.0, "LL": 3.0},
#         "warehouse": {"DL": 4.0, "LL": 5.0},
#         "school": {"DL": 3.0, "LL": 4.0},
#     }
#     return standard_loads.get(building_type.lower(), {"DL": 2.5, "LL": 2.0})

# def recommend_beam_size(load_kN_per_m, span_m, material="M20"):
#     """
#     Recommends beam width (b) and depth (d) in mm based on load and span.
#     """
#     span_mm = span_m * 1000
#     d = span_mm / 15  # typical thumb rule for depth
#     b = d / 2         # assume width is half the depth

#     if load_kN_per_m > 10:  # heavier loading? scale up dimensions
#         d *= 1.2
#         b *= 1.2

#     return int(b), int(d)

# when deflection and stress level exceeds
def suggest_fix_for_stress_warning(stress, material):
    if material == "M20":
        return "Increase to M25 grade concrete or increase depth of beam."
    elif material == "Fe415":
        return "Use Fe500 steel or increase reinforcement percentage (Ast)."
    elif material == "Fe500":
        return "Try increasing effective depth or redistribute loads if possible."
    else:
        return "Switch to a stronger material or redesign section geometry."

def suggest_fix_for_deflection_warning(deflection, limit):
    return (
        f"Increase moment of inertia (I) by increasing depth, use stiffer material, or "
        f"reduce span length with intermediate supports."
    )

# when failure occurs

def langchain_error_explanation(length, b, d, material, stress, stress_ok, deflection, deflection_ok, load_type):
    """Generate AI-based error explanations via LangChain and Groq."""
    if not llm:
        return "AI explanations temporarily disabled. Check calculation results above."
    
    prompt = f"""
You are a structural engineering assistant. Do not include any asterisks (* or **) in your response.

A beam with the following details failed a design check:
- Length = {length} m
- Section = {int(b*1000)} mm × {int(d*1000)} mm
- Material = {material}
- Load Type = {load_type}

Results:
- Stress = {round(stress)} MPa → {'✅ OK' if stress_ok else '❌ Exceeds Limit'}
- Deflection = {round(deflection, 2)} mm → {'✅ OK' if deflection_ok else '❌ Exceeds Limit'}

🧠 Explain Briefly:
1️⃣ What failed?
2️⃣ Why it is failed?
3️⃣ How to fix it? Suggest a new depth, stronger material (e.g., M25 or M30), or alternative like I-beam.

Keep the output concise and professional. Use line breaks for clarity where needed. 
"""
    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        print(f"LangChain error explanation error: {e}")
        return "AI explanations temporarily unavailable. Check calculation results above."
