import numpy as np
import matplotlib.pyplot as plt

meshLabels = ["xfine", "fine", "mid"]
uz45paths = [f"clean/{mesh}Uz_zd45.csv" for mesh in meshLabels]
uz5paths = [f"clean/{mesh}Uz_zd5.csv" for mesh in meshLabels]


for i in range(len(meshLabels)):
    file45 = np.loadtxt(uz45paths[i], delimiter=",", skiprows=1)
    uz45 = file45[:, 1]
    y45 = file45[:, 0]

    plt.plot(y45, uz45, label=meshLabels[i])

plt.ylabel(r"$U_z / U_{z,CL}$")
plt.xlabel(r"$\eta$")
plt.legend()
plt.grid(True, alpha=0.2)
plt.savefig("uz45Plot.svg", dpi=300)
plt.show()

for i in range(len(meshLabels)):
    file5 = np.loadtxt(uz5paths[i], delimiter=",", skiprows=1)
    uz5 = file5[:, 1]
    y5 = file5[:, 0]

    plt.plot(y5, uz5, label=meshLabels[i])
plt.legend()
plt.show()
