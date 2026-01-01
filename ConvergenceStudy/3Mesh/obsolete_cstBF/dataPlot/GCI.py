import numpy as np


def analyze_grid_convergence(f1, f2, f3, r, Fs=1.25):
    """
    Calculates GCI for a triplet of meshes.
    Parameters:
    f1, f2, f3 : Values from Fine, Medium, and Coarse meshes
    r          : Refinement ratio (e.g., 1.5)
    Fs         : Safety factor (1.25 for 3 meshes)
    """
    # 1. Relative errors
    e21 = abs((f2 - f1) / f1)
    e32 = abs((f3 - f2) / f2)

    # 2. Observed order of accuracy (p)
    # Using the standard formula for constant refinement ratio
    p = np.log(abs((f3 - f2) / (f2 - f1))) / np.log(r)

    # 3. Grid Convergence Index (GCI)
    gci_fine = (Fs * e21) / (r**p - 1)
    gci_medium = (Fs * e32) / (r**p - 1)

    # 4. Extrapolated Solution (Richardson Extrapolation)
    # This is the "infinite resolution" estimate
    f_ext = f1 + (f1 - f2) / (r**p - 1)

    # 5. Asymptotic Range Check
    # Should be close to 1.0
    G = gci_medium / (r**p * gci_fine)

    return {
        "p": p,
        "GCI_fine_%": gci_fine * 100,
        "f_ext": f_ext,
        "Asymptotic_G": G
    }


meshLabels = ["xxfine", "xfine", "fine", "mid", "coarse"]
uz45paths = [f"clean/{mesh}Uz_zd45.csv" for mesh in meshLabels]
uz5paths = [f"clean/{mesh}Uz_zd5.csv" for mesh in meshLabels]
UzCL45 = np.zeros(len(uz45paths))
UzCL5 = np.zeros(len(uz5paths))

for i in range(3):
    file45 = np.loadtxt(uz45paths[i], delimiter=",", skiprows=1)
    UzCL45[i] = file45[0, 1]
    file5 = np.loadtxt(uz5paths[i], delimiter=",", skiprows=1)
    UzCL5[i] = file5[0, 1]

print(UzCL45[:3])
print(UzCL5[:3])

tke_xfinebis = 0.1030347
tke_xfine = 0.1042055
tke_max = [0.1036965, tke_xfine, 0.10171920, 0.096870191,
           0.090040987]  # xxfine, xfine, fine, med, coarse

data = {
    "Max_TKE": tke_max[:3],
    "Uz_CL_45D": UzCL45,
    "Uz_CL_5D": UzCL5,
}

r = 1.5
for label, values in data.items():
    stats = analyze_grid_convergence(values[0], values[1], values[2], r)
    print(f"\n--- {label} ---")
    print(f"Order p: {stats['p']:.4f}")
    print(f"GCI: {stats['GCI_fine_%']:.3f}%")
    print(f"Check G: {stats['Asymptotic_G']:.4f}")
