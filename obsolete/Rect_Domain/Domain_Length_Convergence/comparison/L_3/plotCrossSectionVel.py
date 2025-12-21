import matplotlib.pyplot as plt
import numpy as np


def plot_Uz_velocity_profiles(paths, labels):
    plt.figure()

    for i, path in enumerate(paths):
        data = np.loadtxt(path, delimiter=",", skiprows=1)
        y = data[:, 0]
        v = data[:, 1]

        v_norm = v/np.max(v)

        # idx = np.min(idx)
        eta = y/(2*i+5)
        v_norm = v_norm

        plt.plot(eta, v_norm, label=labels[i])
    plt.xlabel(r"$\eta$")
    plt.ylabel(r"$\frac{U_z}{ U_{z,c}}$", fontsize=16)
    plt.xlim(0, 0.3)
    # plt.grid(True)
    plt.legend()
    plt.ylim(0, None)
    plt.xticks([0, 0.1, 0.2])
    plt.savefig("Uz.png", dpi=300)

    plt.show()


def plot_Ur_velocity_profiles(pathsUz, pathsUr, labels):
    plt.figure()

    for i, (pathUz, pathUr) in enumerate(zip(pathsUz, pathsUr)):
        dataUz = np.loadtxt(pathUz, delimiter=",", skiprows=1)
        dataUr = np.loadtxt(pathUr, delimiter=",", skiprows=1)
        y = dataUz[:, 0]
        Uz = dataUz[:, 1]
        Ur = dataUr[:, 1]

        Ur_norm = Ur/np.max(Uz)

        eta = y/(2*i+5)

        plt.plot(eta, Ur_norm, label=labels[i])
    plt.xlabel(r"$\eta$")
    plt.ylabel(r"$\frac{U_r}{ U_{z,c}}$", fontsize=16)
    plt.xticks([0, 0.1, 0.2])
    plt.xlim(0, 0.3)
    # plt.grid(True)
    plt.legend()
    plt.savefig("Ur.png", dpi=300)
    plt.show()


paths_Uz = [f"cleanData/Uz_l_{2*i+5}-m.csv" for i in range(6)]
labels = [f"x = {2*i+5} m" for i in range(6)]
plot_Uz_velocity_profiles(paths_Uz, labels)

paths_Ur = [f"cleanData/Ur_l_{2*i+5}-m.csv" for i in range(6)]
plot_Ur_velocity_profiles(paths_Uz, paths_Ur, labels)
