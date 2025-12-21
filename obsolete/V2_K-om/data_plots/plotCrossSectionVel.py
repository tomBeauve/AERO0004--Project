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
        eta = y/(i+1)
        v_norm = v_norm

        plt.plot(eta, v_norm, label=labels[i])
    plt.xlabel(r"\eta")
    plt.ylabel(r"(v / v0)")
    plt.xlim(0, 0.25)
    # plt.grid(True)
    plt.legend()
    plt.ylim(0, None)
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

        eta = y/(i+1)

        plt.plot(eta, Ur_norm, label=labels[i])
    plt.xlabel(r"\eta")
    plt.ylabel(r"(v / v0)")
    plt.xlim(0, 0.25)
    # plt.grid(True)
    plt.legend()
    plt.show()


paths_Uz = [f"cleanNoLimiter/Uz_line-{i+1}-m.csv" for i in range(15)]
labels = [f"x = {i+1} m" for i in range(15)]
plot_Uz_velocity_profiles(paths_Uz, labels)

paths_Ur = [f"cleanNoLimiter/Ur_line-{i+1}-m.csv" for i in range(15)]
plot_Ur_velocity_profiles(paths_Uz, paths_Ur, labels)
