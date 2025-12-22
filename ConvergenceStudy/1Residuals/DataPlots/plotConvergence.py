import matplotlib.pyplot as plt
import numpy as np


def delta_rel(qty):
    delta_rel = np.zeros(len(qty)-1)
    for i in range(len(qty)-1):
        delta_rel[i] = abs(qty[i+1] - qty[i])/abs(qty[i+1])
    return delta_rel


tols = [1e-3, 1e-4, 1e-5, 1e-6, 1e-7]

paths_Uz = [f"clean/1e-{idx}Uz_zd35.csv" for idx in range(3, 8)]
Uz = np.zeros(len(paths_Uz))
for i, path in enumerate(paths_Uz):
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    Uz[i] = data[0, 1]

massImbalance = [-0.001509, -0.0001972374, -
                 7.811934e-6, 8.677598e-7, 4.046597e-7]
massRateIn = 0.03158853
massImbalance = np.array(massImbalance) / massRateIn
Uz_shearLayer = [0.219194, 0.217761, 0.216866, 0.216769, 0.216778]
tkeMax = [0.0968416, 0.09686802, 0.09686928, 0.09687027, 0.09687034]

print("uz centerline z/D = 35")
print(Uz)
print("mass imbalance")
print(massImbalance)
print("uz at z/D = 20, r/D = 0.5")
print(Uz_shearLayer)
print("tke max")
print(tkeMax)

deltaUz = delta_rel(Uz) * 100
deltaMass = delta_rel(massImbalance)*100
deltaShearL = delta_rel(Uz_shearLayer)*100
deltaTke = delta_rel(tkeMax)*100


# plot Uz
plt.plot(tols, Uz)
plt.scatter(tols, Uz)
plt.xscale('log')
plt.title('Uz')
plt.tight_layout()
plt.gca().invert_xaxis()
plt.show()

plt.plot(tols[1:], deltaUz)
plt.scatter(tols[1:], deltaUz)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('relative change from 10*tol to tol (%)')
plt.gca().invert_xaxis()
plt.show()


# plot mass imbalance
plt.plot(tols, massImbalance)
plt.scatter(tols, massImbalance)
plt.xscale('log')
plt.title('mass imbalance')
plt.tight_layout()
plt.gca().invert_xaxis()
plt.show()

plt.plot(tols[1:], deltaMass)
plt.scatter(tols[1:], deltaMass)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('relative change from 10*tol to tol (%)')
plt.gca().invert_xaxis()
plt.show()

# plot shear Uz
plt.plot(tols, Uz_shearLayer)
plt.scatter(tols, Uz_shearLayer)
plt.xscale('log')
plt.title('Uz in sehar layer')
plt.tight_layout()
plt.gca().invert_xaxis()
plt.show()

plt.plot(tols[1:], deltaShearL)
plt.scatter(tols[1:], deltaShearL)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('relative change from 10*tol to tol (%)')
plt.gca().invert_xaxis()
plt.show()

# plot max tke
plt.plot(tols, tkeMax)
plt.scatter(tols, tkeMax)
plt.xscale('log')
plt.title('maximum tke')
plt.tight_layout()
plt.gca().invert_xaxis()
plt.show()

plt.plot(tols[1:], deltaTke)
plt.scatter(tols[1:], deltaTke)
plt.xscale('log')
plt.yscale('log')
plt.ylabel('relative change from 10*tol to tol (%)')
plt.gca().invert_xaxis()
plt.show()
