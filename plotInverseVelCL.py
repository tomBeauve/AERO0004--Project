import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def convert_csv(input_path: str, output_path: str):
    # read whitespace-separated data but ignore lines starting with '#'
    df = pd.read_csv(
        input_path,
        delim_whitespace=True,
        comment="#",
        header=None,
        names=["Xcoord", "velocity"]
    )

    df.to_csv(output_path, sep=",", index=False)


def plot_normalized_inverse(input_path: str):
    # Load CSV and force numeric conversion
    df = pd.read_csv(input_path)

    df["Xcoord"] = pd.to_numeric(df["Xcoord"], errors="coerce")
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce")

    x = df["Xcoord"].values / 0.2
    v = df["velocity"].values

    v0 = v[0]
    y = v/v0

    plt.figure()
    plt.plot(x, y)
    plt.xlabel("Xcoord")
    plt.ylabel("(v / v0)^(-1)")
    plt.title("Normalized inverse velocity")
    plt.grid(True)
    plt.ylim(0, None)
    plt.show()


convert_csv("V1/csvFiles/clvel.csv", "V1/csvFiles/centerlineVelFormatted.csv")

plot_normalized_inverse("V1/csvFiles/centerlineVelFormatted.csv")
