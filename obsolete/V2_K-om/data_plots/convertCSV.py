import re
import numpy as np
import pandas as pd

raw = open("rawNoLimiter/centerlineVel.csv").read()

blocks = re.findall(
    r'\(\(xy/key/label\s+"([^"]+)"\)\s*(.*?)\)', raw, flags=re.S)

for label, block in blocks:
    arr = np.fromstring(block, sep='\t').reshape(-1, 2)
    df = pd.DataFrame(arr, columns=["Position", "AxialVelocity"])
    df.to_csv(f"cleanNoLimiter/Uz_{label}.csv", index=False)
