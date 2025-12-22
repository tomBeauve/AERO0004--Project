import numpy as np


def find_half_width(data):
    """
    Interpolates to find the radial position where Uz = 0.5 * Uz_CL.
    Assumes data[:, 0] is radial position (y) and data[:, 1] is velocity (Uz).
    """
    y = data[:, 0]
    uz = data[:, 1]
    target = uz[0] * 0.5  # uz[0] is the centerline value (Uz_CL)

    # Find the index where uz first drops below the target
    # We look for the crossover point
    for i in range(len(uz) - 1):
        if uz[i] >= target >= uz[i+1]:
            # Linear interpolation for higher precision
            y_low, y_high = y[i], y[i+1]
            u_low, u_high = uz[i], uz[i+1]
            fraction = (target - u_low) / (u_high - u_low)
            return y_low + fraction * (y_high - y_low)
    return np.nan


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
Y05_45D = np.zeros(len(meshLabels))
Y05_5D = np.zeros(len(meshLabels))

for i in range(len(meshLabels)):
    file45 = np.loadtxt(uz45paths[i], delimiter=",", skiprows=1)
    UzCL45[i] = file45[0, 1]
    Y05_45D[i] = find_half_width(file45)

    file5 = np.loadtxt(uz5paths[i], delimiter=",", skiprows=1)
    UzCL5[i] = file5[0, 1]
    Y05_5D[i] = find_half_width(file5)

print(Y05_5D)
print(Y05_45D)

tke_max = [0.1035398, 0.10299944, 0.10277273, 0.103065,
           0.10492145]  # xxfine, xfine, fine, med, coarse

data = {
    "Max_TKE": tke_max,
    "Uz_CL_45D": UzCL45,
    "Uz_CL_5D": UzCL5,
    "Y05_45D": Y05_45D,
    "Y05_5D": Y05_5D
}

r = 1.5
for i in range(len(meshLabels) - 2):
    print(
        f"-------------{meshLabels[i]}--{meshLabels[i+1]}--{meshLabels[i+2]}-------------")
    for label, values in data.items():
        stats = analyze_grid_convergence(
            values[i], values[i+1], values[i+2], r)
        print(f"\n--- {label} ---")
        print(f"Order p: {stats['p']:.4f}")
        print(f"GCI: {stats['GCI_fine_%']:.3f}%")
        print(f"Check G: {stats['Asymptotic_G']:.4f}")
