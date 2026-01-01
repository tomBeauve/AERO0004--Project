import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter
#print(plt.colormaps())


# Graph parameters
plt.rcParams.update({
    "text.usetex": True,              # Use LaTeX for all text rendering
    "image.cmap" : "cividis",
    "font.family": "serif",           # Use LaTeX's default font family
    "font.serif": ["Times New Roman"],# Use Computer Modern for a LaTeX-like font
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


def get_l2_norm(data_a, data_b):
    """Direct discrete L2 relative error."""
    return (np.linalg.norm(data_a - data_b) / np.linalg.norm(data_a)) * 100


prefixes = ["Base", "Ext1_5", "Ext2_25", "Ext3_375"]
files = ["pressureCL_cldompt1.csv", "UzOut_out75d.csv", "UrTop_top32d.csv"]
labels = ["Static Pressure", "Axial Velocity (Uz)", "Radial Velocity (Ur)"]
x_label = ["x/D", "r/D", "x/D"]
y_label = ["Pressure (Pa)", r"Uz $\mathrm{(m.s^{-1})}$", r"Ur $\mathrm{(m.s^{-1})}$"]

print("--- Domain Independence Quantitative Results ---")

i=0

for filename, title in zip(files, labels):
    plt.figure(figsize=(8, 4))
    values = []

    for pre in prefixes:
        # Load file - assuming Col 0 is Coord, Col 1 is Value
        df = pd.read_csv(f"clean/{pre}{filename}")

        # Sort by the first column (coordinate) to ensure nodal alignment
        df = df.sort_values(by=df.columns[0])

        coords = df.iloc[:, 0].values
        data = df.iloc[:, 1].values
        values.append(data)

        plt.plot(coords, data, label=pre)

    # Compute L2 Norms
    err1 = get_l2_norm(values[1], values[0])  # Base vs 1.5
    err2 = get_l2_norm(values[2], values[1])  # 1.5 vs 2.25
    err3 = get_l2_norm(values[3], values[2])  # 2.25 vs 3.375

    print(f"{title}:")
    print(f"  Base vs Ext1.5: {err1:.4f}%")
    print(f"  Ext1.5 vs Ext2.25: {err2:.4f}%")
    print(f"  Ext2.25 vs Ext3.375: {err3:.4f}%")
    plt.xlabel(x_label[i])
    plt.ylabel(y_label[i])
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    ax = plt.gca()
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    file_name = f"{title.replace(" ", "_").lower()}_domain_independence.pdf" 
    plt.savefig(file_name, bbox_inches='tight')
    i=i+1
plt.show()
