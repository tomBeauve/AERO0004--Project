import matplotlib.pyplot as plt
import numpy as np


def compare_Uz_profiles(paths, labels, z_user):
    plt.figure()

    # --- Load and Normalize Reference Data (paths[0]) ---
    data_ref = np.loadtxt(paths[0], delimiter=",", skiprows=1)
    y_ref, Uz_ref = data_ref[:, 0], data_ref[:, 1]
    Uz_ref_norm = Uz_ref / np.max(Uz_ref)

    # Define common grid for robust comparison
    y_min = y_ref.min()
    y_max = y_ref.max()
    y_common = np.linspace(y_min, y_max, 400)

    # Interpolate Reference onto the common grid
    Uz_ref_i = np.interp(y_common, y_ref, Uz_ref_norm)
    eta_common = y_common / z_user

    # --- Iterate through remaining files (paths[1:]) ---
    for i, path in enumerate(paths[1:]):
        data_i = np.loadtxt(path, delimiter=",", skiprows=1)
        y_i, Uz_i = data_i[:, 0], data_i[:, 1]

        Uz_i_norm = Uz_i / np.max(Uz_i)

        # Interpolate Current Profile onto the common grid
        Uz_i_i = np.interp(y_common, y_i, Uz_i_norm)

        # Calculate difference relative to the reference
        diff = Uz_i_i - Uz_ref_i

        # Label the difference plot correctly
        label_diff = f"Uz : {labels[i+1]} - {labels[0]}"
        plt.plot(eta_common, diff, label=label_diff)

    plt.xlabel(r"$\eta$")
    plt.ylabel(r"$\Delta\left(\frac{U_z}{U_{z,c}}\right)$")
    plt.xlim(0, 0.3)
    plt.legend()
    plt.grid(True)
    plt.show()


def compare_Ur_profiles(pathsUz, pathsUr, labels, z_user):
    plt.figure()

    # --- Load and Normalize Reference Data (paths[0]) ---
    dataUz_ref = np.loadtxt(pathsUz[0], delimiter=",", skiprows=1)
    dataUr_ref = np.loadtxt(pathsUr[0], delimiter=",", skiprows=1)

    y_ref = dataUz_ref[:, 0]
    Uz_ref = dataUz_ref[:, 1]
    Ur_ref = dataUr_ref[:, 1]
    Ur_ref_norm = Ur_ref / np.max(Uz_ref)

    # Define common grid
    y_min = y_ref.min()
    y_max = y_ref.max()
    y_common = np.linspace(y_min, y_max, 400)

    # Interpolate Reference Ur onto the common grid
    Ur_ref_i = np.interp(y_common, y_ref, Ur_ref_norm)
    eta_common = y_common / z_user

    # --- Iterate through remaining files (paths[1:]) ---
    for i, (pathUz, pathUr) in enumerate(zip(pathsUz[1:], pathsUr[1:])):
        dataUz_i = np.loadtxt(pathUz, delimiter=",", skiprows=1)
        dataUr_i = np.loadtxt(pathUr, delimiter=",", skiprows=1)

        y_i = dataUz_i[:, 0]
        Uz_i = dataUz_i[:, 1]
        Ur_i = dataUr_i[:, 1]

        Ur_i_norm = Ur_i / np.max(Uz_i)

        # Interpolate Current Profile onto the common grid
        Ur_i_i = np.interp(y_common, y_i, Ur_i_norm)

        # Calculate difference relative to the reference
        diff = Ur_i_i - Ur_ref_i

        # Label the difference plot correctly
        label_diff = f"Ur : {labels[i+1]} - {labels[0]}"
        plt.plot(eta_common, diff, label=label_diff)

    plt.xlabel(r"$\eta$")
    plt.ylabel(r"$\Delta\left(\frac{U_r}{U_{z,c}}\right)$")
    plt.xlim(0, 0.3)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_Uz_profiles(paths, labels, z_user):
    """
    Plots multiple normalized axial velocity profiles (Uz/Uz,c) vs. the similarity variable (eta).
    """
    plt.figure()

    for i, path in enumerate(paths):
        # Load data
        data = np.loadtxt(path, delimiter=",", skiprows=1)
        y = data[:, 0]
        Uz = data[:, 1]

        # Normalization and Scaling
        Uz_norm = Uz / np.max(Uz)  # Uz is normalized by its own max (Uz,c)
        eta = y / z_user          # y is normalized by the axial position z_user

        # Plotting
        plt.plot(eta, Uz_norm, label=labels[i])

    plt.xlabel(r"$\eta$")
    plt.ylabel(r"$\frac{U_z}{U_{z,c}}$", fontsize=16)
    plt.xlim(0, 0.3)
    plt.ylim(0, 1.05)  # Constrain Y-axis based on normalization
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_Ur_profiles(pathsUz, pathsUr, labels, z_user):
    """
    Plots multiple normalized radial velocity profiles (Ur/Uz,c) vs. the similarity variable (eta).
    Requires the corresponding Uz file for normalization.
    """
    plt.figure()

    # Iterates over corresponding Uz and Ur paths
    for i, (pathUz, pathUr) in enumerate(zip(pathsUz, pathsUr)):
        # Load data
        dataUz = np.loadtxt(pathUz, delimiter=",", skiprows=1)
        dataUr = np.loadtxt(pathUr, delimiter=",", skiprows=1)

        y = dataUz[:, 0]
        Uz = dataUz[:, 1]  # Needed for normalization factor
        Ur = dataUr[:, 1]  # The quantity being plotted

        # Normalization and Scaling
        # Ur is normalized by the maximum axial velocity (Uz,c)
        Ur_norm = Ur / np.max(Uz)
        eta = y / z_user

        # Plotting
        plt.plot(eta, Ur_norm, label=labels[i])

    plt.xlabel(r"$\eta$")
    plt.ylabel(r"$\frac{U_r}{U_{z,c}}$", fontsize=16)
    plt.xticks([0, 0.1, 0.2])
    plt.xlim(0, 0.3)
    plt.legend()
    plt.grid(True)
    plt.show()


z = 13
paths_Uz = [
    f"L_10/cleanData/Uz_l_{z}-m.csv",
    f"L_5/cleanData/Uz_l_{z}-m.csv",
    f"L_1-5/cleanData/Uz_line-{z}-m.csv",
    f"L_3/cleanData/Uz_l_{z}-m.csv"
]
paths_Ur = [
    f"L_10/cleanData/Ur_l_{z}-m.csv",
    f"L_5/cleanData/Ur_l_{z}-m.csv",
    f"L_1-5/cleanData/Ur_line-{z}-m.csv",
    f"L_3/cleanData/Ur_l_{z}-m.csv"
]

labels = ["L = 10 (Ref)", "L= 5", "L = 1.5", "L = 3"]

plot_Uz_profiles(paths_Uz, labels, z)
compare_Uz_profiles(paths_Uz, labels, z)

plot_Ur_profiles(paths_Uz, paths_Ur, labels, z)
compare_Ur_profiles(paths_Uz, paths_Ur, labels, z)
