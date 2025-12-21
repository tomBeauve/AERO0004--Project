import matplotlib.pyplot as plt
import numpy as np


def plot_normalized_CL_vel_comp(x_arrays, v_arrays, labels=None):
    plt.figure()
    for i in range(len(x_arrays)):
        x_array = x_arrays[i]
        v_array = v_arrays[i]

        x = x_array / 0.2               # scale X
        v0 = v_array[0]                     # first velocity
        v = v0 / v_array                    # normalized inverse velocity

        if labels:
            plt.plot(x, v, label=labels[i])
        else:
            plt.plot(x, v)

    plt.xlabel("Xcoord / 0.2")
    plt.ylabel(r"(v / v0)^{-1}")

    plt.grid(True)
    plt.ylim(0, None)
    plt.xlim(0, 75)
    plt.xticks([0, 25, 50, 75])
    plt.yticks([0, 5, 10, 15])
    plt.legend()
    plt.show()


def plot_CL_vel_difference(x_arrays, v_arrays):
    plt.figure()
    x_array1 = x_arrays[0]/0.2
    v_array1 = v_arrays[0][0]/v_arrays[0]

    for i in range(1, len(x_arrays)):
        x_arr = x_arrays[i]/0.2
        v_arr = v_arrays[i][0]/v_arrays[i]
        plt.plot(x_arr, v_arr - v_array1, label=f"{i+1} vs 1")

        plt.plot()
    plt.legend()
    plt.show()


data1_5 = np.loadtxt("L_1-5/cleanData/Uz_cldompt1.csv",
                     delimiter=",", skiprows=1)

x1_5 = data1_5[:, 0]
v1_5 = data1_5[:, 1]

data3 = np.loadtxt("L_3/cleanData/Uz_cldompt1.csv",
                   delimiter=",", skiprows=1)

x3 = data3[:, 0]
v3 = data3[:, 1]

plot_normalized_CL_vel_comp([x1_5, x3], [v1_5, v3], labels=["L = 1.5", "L= 3"])
plot_CL_vel_difference([x1_5, x3], [v1_5, v3])
