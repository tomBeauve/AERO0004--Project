import re
import numpy as np
import pandas as pd
import os  # Import os for directory creation
domain = "Ext3_375"
type = "UzOut"
rawfile = f"rawData{domain}/{type}.csv"
print(rawfile)

# Ensure the output directory exists
os.makedirs("clean", exist_ok=True)

# Load the raw Fluent output file
raw = open(rawfile).read()

# Regex to find blocks of data and their labels
# Finds ((xy/key/label "LABEL") DATA_BLOCK)
blocks = re.findall(
    r'\(\(xy/key/label\s+"([^"]+)"\)\s*(.*?)\)', raw, flags=re.S)

for label, block in blocks:
    # 1. Parse the block data into a NumPy array
    arr = np.fromstring(block, sep='\t').reshape(-1, 2)

    # Separate the Position (y) and Velocity (U) components
    y = arr[:, 0]
    U = arr[:, 1]

    # 2. Implement the Reversal Logic (Standardization)
    # Check if the radial position array is descending
    if y[0] > y[-1]:
        print(f"Reversing order for file labeled: {label}")
        y = y[::-1]  # Reverse the y-array
        U = U[::-1]  # Reverse the velocity array to match

    # 3. Create DataFrame and Export
    df = pd.DataFrame(
        {
            "Position": y,
            "RadialVelocity": U
        }
    )

    # Save the standardized data to a new CSV file
    df.to_csv(f"clean/{domain}{type}_{label}.csv", index=False)
