import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter


def calculate_potential_core(z_coords, uz_values, u_exit):
    # Find first index where velocity drops below 98% of exit
    for i in range(len(uz_values)):
        if uz_values[i] < 0.98 * u_exit:
            return z_coords[i]
    return z_coords[-1]  # if there is a problem, still returns something


def calculate_y_05(y_coords, uz_values, uz_CL):
    for i in range(len(uz_values)):
        if uz_values[i] < 0.5 * uz_CL:
            return y_coords[i]

    return y_coords[-1]  # if there is a problem, still returns something


prefixes = ["A", "B1", "B2"]
files = ["UzCL_cldompt1.csv", "UzProfiles_zd45.csv", "UzProfiles_zd25.csv"]
tkeMax = {
    "A": 0.1029994,
    "B1": 0.1037837,
    "B2": 0.1027692
}

results = {}

print("-----potential core length-----")
for pre in prefixes:
    results[pre] = {}

    dataCL = np.loadtxt(f"clean/{pre}_{files[0]}", delimiter=",", skiprows=1)
    uzCL = dataCL[:, 1]
    zCL = dataCL[:, 0]
    potCoreLength = calculate_potential_core(zCL, uzCL, uzCL[0])
    results[pre]["potCore"] = potCoreLength

    print(f"case {pre} : {potCoreLength}")

print("-----y 0.5 at z/D = 25-----")
for pre in prefixes:
    data25 = np.loadtxt(f"clean/{pre}_{files[2]}", delimiter=",", skiprows=1)
    uz25 = data25[:, 1]
    r25 = data25[:, 0]
    y_05 = calculate_y_05(r25, uz25, uz25[0])
    results[pre]["y05_25"] = y_05

    print(f"case {pre} : {y_05}")


print("-----Uz CL at z/D = 25-----")
for pre in prefixes:
    data25 = np.loadtxt(f"clean/{pre}_{files[2]}", delimiter=",", skiprows=1)
    uz25 = data25[:, 1]
    uzCL25 = uz25[0]
    results[pre]["uzCL25"] = uzCL25

    print(f"case {pre} : {uzCL25}")


print("-----y 0.5 at z/D = 45-----")
for pre in prefixes:
    data45 = np.loadtxt(f"clean/{pre}_{files[1]}", delimiter=",", skiprows=1)
    uz45 = data45[:, 1]
    r45 = data45[:, 0]
    y_05 = calculate_y_05(r45, uz45, uz45[0])
    results[pre]["y05_45"] = y_05

    print(f"case {pre} : {y_05}")


print("-----Uz CL at z/D = 45-----")
for pre in prefixes:
    data45 = np.loadtxt(f"clean/{pre}_{files[1]}", delimiter=",", skiprows=1)
    uz45 = data45[:, 1]
    uzCL45 = uz45[0]
    results[pre]["uzCL45"] = uzCL45

    print(f"case {pre} : {uzCL45}")


print("-----tke Max-----")
for pre in prefixes:
    tke = tkeMax[pre]
    results[pre]["tkeMax"] = tke

    print(f"case {pre} : {tke}")


print("-----relative differences w.r.t case A-----")

for case in ["B1", "B2"]:
    print(f"\ncase {case} vs A:")

    for key in results["A"]:
        rel_diff = (results[case][key] - results["A"][key]) / results["A"][key]
        print(f"{key}: {100*rel_diff:.4f} %")
