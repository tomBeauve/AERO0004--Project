import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter
# print(plt.colormaps())


# Graph parameters
plt.rcParams.update({
    "text.usetex": True,              # Use LaTeX for all text rendering
    "image.cmap": "cividis",
    "font.family": "serif",           # Use LaTeX's default font family
    # Use Computer Modern for a LaTeX-like font
    "font.serif": ["Times New Roman"],
    "font.size": 12,                  # Global font size to match LaTeX
    "axes.titlesize": 14,             # Font size for title
    "axes.labelsize": 14,             # Font size for axis labels
    "xtick.labelsize": 12,            # Font size for x-axis ticks
    "ytick.labelsize": 12,            # Font size for y-axis ticks
    "legend.fontsize": 12,             # Font size for legend
    "axes.grid": True,
    "grid.color": "0.9",
    "grid.linewidth": 0.7,
    "grid.alpha": 0.9
})


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
plt.figure()
plt.plot(tols, Uz, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols, Uz)
plt.xscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel(r'Uz $\mathrm{(m.s^{-1})}$')
plt.title('Uz')
plt.tight_layout()
ax = plt.gca()
ax.invert_xaxis()
ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
# ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.3f}"))  # 3 decimals
plt.savefig("Uz_normal.pdf", bbox_inches='tight')
# plt.show()

plt.figure()
plt.plot(tols[1:], deltaUz, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols[1:], deltaUz)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel(r'$\mathrm{\Delta Uz}$ from 10*tol to tol (%)')
plt.gca().invert_xaxis()
plt.savefig("deltaUz.pdf", bbox_inches='tight')
# plt.show()


# plot mass imbalance
plt.figure()
plt.plot(tols, massImbalance, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols, massImbalance)
plt.xscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel('Mass imbalance (-)')
plt.title('Mass imbalance as fraction of inlet mass flow with tolerance')
plt.tight_layout()
ax = plt.gca()
ax.invert_xaxis()
ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
# ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.3f}"))  # 3 decimals
plt.savefig("mass_imbalance.pdf", bbox_inches='tight')
# plt.show()

# plot mass imbalance absolute value in log scale
plt.figure()
plt.plot(tols, np.abs(massImbalance), linestyle='-',
         marker='o', lw=2, markersize=6)
# plt.scatter(tols, massImbalance)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel('Mass imbalance (-)')
plt.title(
    'Mass imbalance absolute value as fraction of inlet mass flow with tolerance')
plt.tight_layout()
ax = plt.gca()
ax.invert_xaxis()
# ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
# ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.3f}"))  # 3 decimals
plt.savefig("mass_imbalance_abs.pdf", bbox_inches='tight')
# plt.show()


plt.figure()
plt.plot(tols[1:], deltaMass, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols[1:], deltaMass)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel('relative change from 10*tol to tol (%)')
plt.gca().invert_xaxis()
plt.savefig("delta_mass.pdf", bbox_inches='tight')
# plt.show()

# plot shear Uz
plt.figure()
plt.plot(tols, Uz_shearLayer, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols, Uz_shearLayer)
plt.xscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel(r'Uz $\mathrm{(m.s^{-1})}$')
plt.title('Uz in shear layer')
plt.tight_layout()
ax = plt.gca()
ax.invert_xaxis()
ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
# ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.3f}"))  # 3 decimals
plt.savefig("Uz_shear_layer.pdf", bbox_inches='tight')
# plt.show()

plt.figure()
plt.plot(tols[1:], deltaShearL, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols[1:], deltaShearL)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel('relative change from 10*tol to tol (%)')
plt.title(r'$\mathrm{\Delta Uz}$ shear layer')
plt.gca().invert_xaxis()
plt.savefig("delta_shear_layer.pdf", bbox_inches='tight')
# plt.show()

# plot max tke
plt.figure()
plt.plot(tols, tkeMax, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols, tkeMax)
plt.xscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel(r'Maximum TKE $\mathrm{(m^2.s^{-2})}$')
plt.title('Maximum TKE')
plt.tight_layout()
ax = plt.gca()
ax.invert_xaxis()
ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
# ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.3f}"))  # 3 decimals
plt.savefig("deltaTke.pdf", bbox_inches='tight')
# plt.show()

plt.figure()
plt.plot(tols[1:], deltaTke, linestyle='-', marker='o', lw=2, markersize=6)
# plt.scatter(tols[1:], deltaTke)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Tolerance (-)')
plt.ylabel('relative change from 10*tol to tol (%)')
plt.title(r'$\mathrm{\Delta TKE}$')
plt.gca().invert_xaxis()
plt.show()
plt.savefig("deltaTke.pdf", bbox_inches='tight')
