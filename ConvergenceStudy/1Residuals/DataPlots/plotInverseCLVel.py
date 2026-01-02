import matplotlib.pyplot as plt
import numpy as np


def plot_normalized_CL_vel(x_array, v_array, label=None):
    """
    arr: Nx2 NumPy array -> [:,0] = Xcoord, [:,1] = velocity
    """

    x = x_array / 0.2               # scale X
    v0 = v_array[0]                     # first velocity
    v = v0 / v_array                    # normalized inverse velocity

    plt.figure()
    plt.plot(x, v)
    plt.xlabel("Xcoord / 0.2")
    plt.ylabel(r"(v / v0)^{-1}")
    if label:
        plt.title(f"Normalized inverse velocity – {label}")
    plt.grid(True)
    plt.ylim(0, None)
    plt.show()


data = np.loadtxt("clean/1e-7UzCL_cldomain.csv",
                  delimiter=",", skiprows=1)

x = data[:, 0]
v = data[:, 1]
plot_normalized_CL_vel(x, v)
