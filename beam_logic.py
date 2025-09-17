import numpy as np
import math


# 1. Load Cases


def point_load_center(L, P, E=25e9, I=8.33e-6):
    R1 = R2 = P / 2  
    x = np.linspace(0, L, 10)
    V = np.piecewise(x, [x < L / 2, x >= L / 2], [lambda x: R1, lambda x: -R2])
    V = (V / 1000).tolist()  


    M = np.piecewise(
        x,
        [x < L / 2, x >= L / 2],
        [lambda x: R1 * x, lambda x: R1 * x - P * (x - L / 2)]
    )
    M = (M / 1000).tolist()  

    # Max Moment 
    M_max = (P * L) / 4 / 1000  

    # Deflection 
    deflection_vals = []
    for xi in x:
        if xi <= L / 2:
            dx = (P * xi) / (48 * E * I) * (3 * L ** 2 - 4 * xi ** 2)
        else:
            dx = (P * (L - xi)) / (48 * E * I) * (3 * L ** 2 - 4 * (L - xi) ** 2)
        deflection_vals.append(dx * 1000)  

    max_deflection = (P * L ** 3) / (48 * E * I) * 1000  

    return R1 / 1000, R2 / 1000, M_max, x.tolist(), V, M, deflection_vals, max_deflection


# def max_deflection_point_load_anywhere(P, L, a, E, I):
#     b = L - a
#     if a < b:
#         delta_max = (P * a * b ** 2) / (3 * E * I * L)
#     else:
#         delta_max = (P * b * a ** 2) / (3 * E * I * L)
#     return delta_max * 1000  


# def point_load_anywhere(L, P_raw, a_raw, E=25e9, I=8.33e-6):
#     try:
#         P = float(P_raw)
#         a = float(a_raw)
#     except (ValueError, TypeError):
#         P = 0.0
#         a = 0.0

#     b = L - a

#     R1 = (P * b) / L
#     R2 = (P * a) / L
#     x = np.linspace(0, L, 10)

#     V = np.piecewise(x, [x < a, x >= a], [lambda x: R1, lambda x: R1 - P])
#     M = np.piecewise(
#         x,
#         [x <= a, x > a],
#         [lambda x: R1 * x, lambda x: R1 * x - P * (x - a)]
#     )

#     # Deflection profile
#     delta = []
#     for xi in x:
#         if xi <= a:
#             dx = (P * b * xi * (L ** 2 - b ** 2 - xi ** 2)) / (6 * L * E * I)
#         else:
#             dx = (P * a * (L - xi) * (L ** 2 - a ** 2 - (L - xi) ** 2)) / (6 * L * E * I)
#         delta.append(dx * 1000)  # mm

#     M_max = max(abs(M))
#     max_delta = max_deflection_point_load_anywhere(P, L, a, E, I)

#     return R1, R2, M_max, x.tolist(), V.tolist(), M.tolist(), delta, max_delta


def udl(L, w, E=25e9, I=8.33e-6):
    P = w * L  
    R1 = R2 = P / 2  
    x = np.linspace(0, L, 10) 
    V = (R1 - w * x) / 1000  
    M = (R1 * x - (w * x ** 2) / 2) / 1000  
    M_max = (w * L ** 2) / 8 / 1000
    delta_vals = x_deflection_profile_udl(w, L, x, E, I)
    max_delta = max_deflection_udl(w, L, E, I) * 1000

    return R1 / 1000, R2 / 1000, M_max, x.tolist(), V.tolist(), M.tolist(), delta_vals, max_delta


import numpy as np

def max_deflection_uvl(w_max, L, E, I):
    # Max deflection (mm): delta_max = (w_max * L^4) / (30 * E * I)
    return (w_max * L**4) / (30 * E * I) * 1000  # in mm

def x_deflection_profile_uvl(w_max, L, x, E, I):
    # Deflection at each x: delta(x) = (w_max / (120 * E * I * L)) * x^2 * (5L^2 - x^2)
    return ((w_max * x**2 * (5 * L**2 - x**2)) / (120 * E * I * L)) * 1000  # mm

def uvl(L, w_max, E=25e9, I=8.33e-6):
    P = (w_max * L) / 2
    x_cg = (2 * L) / 3
    R2 = (P * x_cg) / L
    R1 = P - R2

    x = np.linspace(0, L, 10)
    V = R1 - (w_max / L) * (x ** 2) / 2
    V=V/1000
    M = R1 * x - (w_max * x ** 3) / (6 * L)
    M=M/1000
    M_max = (w_max * L ** 2) / (9 * math.sqrt(3))  
    M_max = round(M_max / 1000,2)


    delta_vals = x_deflection_profile_uvl(w_max, L, x, E, I)
    max_delta = max_deflection_uvl(w_max, L, E, I)

    return R1/1000, R2/1000, M_max, x.tolist(), V.tolist(), M.tolist(), delta_vals.tolist(), max_delta


def moment_applied(L, M_applied, E=25e9, I=8.33e-6):
    R1 = -M_applied / L
    R2 = M_applied / L
    x = np.linspace(0, L, 10)
    V = np.full_like(x, R1)
    V=V/1000
    M = R1 * x
    M=M/1000
    M_max = abs(M_applied)
    M_max=M_max/1000
    delta_vals = [0] * len(x) 
    max_delta = 0

    return R1, R2, M_max, x.tolist(), V.tolist(), M.tolist(), delta_vals, max_delta



# 2. Material Properties


materials = {
    "M20": {"fck": 20, "E": 25e9},
    "M25": {"fck": 25, "E": 30e9},
    "Fe415": {"fy": 415, "E": 2e11},
    "Fe500": {"fy": 500, "E": 2e11}
}


def get_material_properties(name):
    return materials.get(name, {})



# 3. Section Properties


def rectangular_section(b, d):
    I = (b * d ** 3) / 12
    A = b * d
    Z = I / (d / 2)
    return {"I": I, "A": A, "Z": Z}



# 4. Stress Check


def stress_check(M_max, Z, allowable_stress):
    actual_stress = M_max / Z  
    return actual_stress, actual_stress <= allowable_stress



# 5. Deflection for UDL & Helpers


def max_deflection_udl(w, L, E, I):
    delta = (5 * w * L ** 4) / (384 * E * I)  
    return delta


def x_deflection_profile_udl(w, L, x, E=25e9, I=8.33e-6):
    delta = (w * x * (L ** 3 - 2 * L * x ** 2 + x ** 3)) / (24 * E * I)
    return (delta * 1000).tolist()  



# 6. Dispatcher

def calculate_all(L, load_type, params, E=25e9, I=8.33e-6):
    try:
        if load_type == "point_center":
            P = float(params.get("P", 0))
            return point_load_center(L, P, E, I)
        elif load_type == "point_anywhere":
            return point_load_anywhere(L, params.get("P", 0), params.get("a", 0), E, I)
        elif load_type == "udl":
            w = float(params.get("w", 0))
            return udl(L, w, E, I)
        elif load_type == "uvl":
            w_max = float(params.get("w_max", 0))
            return uvl(L, w_max, E, I)
        elif load_type == "moment":
            M_applied = float(params.get("M_applied", 0))
            return moment_applied(L, M_applied, E, I)
        else:
            raise ValueError("Invalid load type")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input parameters: {e}")


def map_input_to_loads(load_type, value):
    dl = ll = wl = eq = 0
    if load_type == "udl":
        dl = value/1000
    elif load_type in ["point_center", "point_anywhere"]:
        ll = value/1000
    elif load_type == "uvl":
        wl = value/1000
    elif load_type == "moment":
        eq = value/1000
    return dl, ll, wl, eq


def generate_load_combinations(dead, live, wind=0, seismic=0, mode="strength"):
    """
    Generate load combinations based on selected design mode.
    mode = "strength" (default), "serviceability", or "compressibility"
    """

    if mode == "strength":  # Ultimate Limit State (ULS)
        return [
            {"name": "DL + LL", "load": dead + live},
            {"name": "1.5DL + 1.5LL", "load": 1.5 * (dead + live)},
            {"name": "1.2DL + 1.2LL + 1.2WL", "load": 1.2 * (dead + live + wind)},
            {"name": "1.5DL + 1.5WL", "load": 1.5 * (dead + wind)},
            {"name": "0.9DL + 1.5WL", "load": 0.9 * dead + 1.5 * wind},
            {"name": "0.9DL + 1.5EQ", "load": 0.9 * dead + 1.5 * seismic},
        ]

    elif mode == "serviceability":  # Serviceability Limit State (SLS)
        return [
            {"name": "DL only", "load": dead},
            {"name": "DL + LL (unfactored)", "load": dead + live},
            {"name": "DL + WL (unfactored)", "load": dead + wind},
            {"name": "DL + EQ (unfactored)", "load": dead + seismic},
        ]

    elif mode == "compressibility":  # Long-term / stability check
        return [
            {"name": "DL only (creep check)", "load": dead},
            {"name": "DL + 0.3LL", "load": dead + 0.3 * live},  # sustained live load
            {"name": "DL + 0.3WL", "load": dead + 0.3 * wind},
            {"name": "DL + 0.3EQ", "load": dead + 0.3 * seismic},
        ]

    else:
        raise ValueError("Invalid mode. Choose 'strength', 'serviceability', or 'compressibility'")


def stress_distribution(fck, d):
    depths = np.linspace(0, d, 10).tolist()
    stresses = [fck * (1 - x / d) for x in depths]
    return {"depths": depths, "stresses": stresses}
