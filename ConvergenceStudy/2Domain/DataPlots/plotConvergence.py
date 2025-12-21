import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_l2_norm(data_a, data_b):
    """Direct discrete L2 relative error."""
    return (np.linalg.norm(data_a - data_b) / np.linalg.norm(data_a)) * 100


prefixes = ["Base", "Ext1_5", "Ext2_25", "Ext3_375"]
files = ["pressureCL_cldompt1.csv", "UzOut_out75d.csv", "UrTop_top32d.csv"]
labels = ["Static Pressure", "Axial Velocity (Uz)", "Radial Velocity (Ur)"]

print("--- Domain Independence Quantitative Results ---")

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

    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()
