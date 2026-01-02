import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###### Import Raw quantities ####

DNSData = pd.read_csv(
    "1_Moments.txt",
    sep=r"\s+",
    header=None
)
DNSData = DNSData.iloc[1:].reset_index(drop=True)
DNSData = DNSData.apply(pd.to_numeric, errors="coerce")
DNSData = DNSData.dropna(axis=1, how="all")


DNSData.columns = [
    "r", "z",
    "U_r", "U_phi", "U_z",
    "U_r U_r",
    "U_phi U_phi",
    "U_z U_z",
    "U_r U_phi",
    "U_r U_z"
]


r = DNSData["r"].to_numpy()
z = DNSData["z"].to_numpy()

Ur = DNSData["U_r"].to_numpy()
Uphi = DNSData["U_phi"].to_numpy()
Uz = DNSData["U_z"].to_numpy()

Ur_Ur = DNSData["U_r U_r"].to_numpy()
Uphi_Uphi = DNSData["U_phi U_phi"].to_numpy()
Uz_Uz = DNSData["U_z U_z"].to_numpy()

Ur_Uphi = DNSData["U_r U_phi"].to_numpy()
Ur_Uz = DNSData["U_r U_z"].to_numpy()

##### Extract quantities of interest used in in the paper #####


def fluctFromMean(secondMoment, mean, meanbis=None):
    if meanbis is None:
        return secondMoment - mean**2
    else:
        return secondMoment - mean*meanbis


# centerline and velocity at centerline
z_CL = z[r == 0]
Uz_CL = Uz[r == 0]
Ur_CL = Ur[r == 0]
Uphi_CL = Uphi[r == 0]

# velocity profiles at different z/D locations
r_profiles = r[z == 25]
Uz_zd25 = Uz[z == 25]
Ur_zd25 = Ur[z == 25]
Ur_Ur_zd25 = Ur_Ur[z == 25]
Uz_Uz_zd25 = Uz_Uz[z == 25]
Ur_Uz_zd25 = Ur_Uz[z == 25]
ur2_zd25 = fluctFromMean(Ur_Ur_zd25, Ur_zd25)
uz2_zd25 = fluctFromMean(Uz_Uz_zd25, Uz_zd25)
ur_uz_zd25 = fluctFromMean(Ur_Uz_zd25, Uz_zd25, Ur_zd25)

# --- z/D = 35 ---
r_profiles_35 = r[z == 35]
Uz_zd35 = Uz[z == 35]
Ur_zd35 = Ur[z == 35]
Ur_Ur_zd35 = Ur_Ur[z == 35]
Uz_Uz_zd35 = Uz_Uz[z == 35]
Ur_Uz_zd35 = Ur_Uz[z == 35]
ur2_zd35 = fluctFromMean(Ur_Ur_zd35, Ur_zd35)
uz2_zd35 = fluctFromMean(Uz_Uz_zd35, Uz_zd35)
ur_uz_zd35 = fluctFromMean(Ur_Uz_zd35, Uz_zd35, Ur_zd35)

# --- z/D = 45 ---
r_profiles_45 = r[z == 45]
Uz_zd45 = Uz[z == 45]
Ur_zd45 = Ur[z == 45]
Ur_Ur_zd45 = Ur_Ur[z == 45]
Uz_Uz_zd45 = Uz_Uz[z == 45]
Ur_Uz_zd45 = Ur_Uz[z == 45]
ur2_zd45 = fluctFromMean(Ur_Ur_zd45, Ur_zd45)
uz2_zd45 = fluctFromMean(Uz_Uz_zd45, Uz_zd45)
ur_uz_zd45 = fluctFromMean(Ur_Uz_zd45, Uz_zd45, Ur_zd45)

# --- z/D = 55 ---
r_profiles_55 = r[z == 55]
Uz_zd55 = Uz[z == 55]
Ur_zd55 = Ur[z == 55]
Ur_Ur_zd55 = Ur_Ur[z == 55]
Uz_Uz_zd55 = Uz_Uz[z == 55]
Ur_Uz_zd55 = Ur_Uz[z == 55]
ur2_zd55 = fluctFromMean(Ur_Ur_zd55, Ur_zd55)
uz2_zd55 = fluctFromMean(Uz_Uz_zd55, Uz_zd55)
ur_uz_zd55 = fluctFromMean(Ur_Uz_zd55, Uz_zd55, Ur_zd55)

# --- z/D = 65 ---
r_profiles_65 = r[z == 65]
Uz_zd65 = Uz[z == 65]
Ur_zd65 = Ur[z == 65]
Ur_Ur_zd65 = Ur_Ur[z == 65]
Uz_Uz_zd65 = Uz_Uz[z == 65]
Ur_Uz_zd65 = Ur_Uz[z == 65]
ur2_zd65 = fluctFromMean(Ur_Ur_zd65, Ur_zd65)
uz2_zd65 = fluctFromMean(Uz_Uz_zd65, Uz_zd65)
ur_uz_zd65 = fluctFromMean(Ur_Uz_zd65, Uz_zd65, Ur_zd65)

#  velocity fluctuations at centerline
# to get fluctuations from second moment and mean velocities we must do
# u_i**2 = Ui_Ui - Ui**2 (fluctuation ii = second moment ii - mean velocity i squared)


Uz_Uz_CL = Uz_Uz[r == 0]
Ur_Ur_CL = Ur_Ur[r == 0]
Uphi_Uphi_CL = Uphi_Uphi[r == 0]

ur2_CL = Ur_Ur_CL - Ur_CL**2
uz2_CL = Uz_Uz_CL - Uz_CL**2
uphi2_CL = Uphi_Uphi_CL - Uphi_CL**2

Ur_Uz_CL = Ur_Uz[r == 0]

ur_uz_CL = Ur_Uz_CL - Uz_CL * Ur_CL

k_CL = 1/2 * (ur2_CL + uz2_CL + uphi2_CL)
# plt.plot(CL, np.sqrt(k_CL)/UzCL)
# plt.show()


##### Put quantities of interest inside CSV files ####

df_CL = pd.DataFrame({
    "x-coordinate": z_CL,
    "axial-velocity": Uz_CL,
    "uu": uz2_CL,
    "vv": ur2_CL,
    "ww": uphi2_CL,
    'uv': ur_uz_CL,
    "turb-kinetic-energy": k_CL
})

df_profiles = pd.DataFrame({
    "y-coordinate": r_profiles,

    # --- Mean Velocities ---
    "Uz_zd25": Uz_zd25, "Ur_zd25": Ur_zd25,
    "Uz_zd35": Uz_zd35, "Ur_zd35": Ur_zd35,
    "Uz_zd45": Uz_zd45, "Ur_zd45": Ur_zd45,
    "Uz_zd55": Uz_zd55, "Ur_zd55": Ur_zd55,
    "Uz_zd65": Uz_zd65, "Ur_zd65": Ur_zd65,

    # --- Reynolds Normal Stress (Axial: uu) ---
    "uu_zd25": uz2_zd25,
    "uu_zd35": uz2_zd35,
    "uu_zd45": uz2_zd45,
    "uu_zd55": uz2_zd55,
    "uu_zd65": uz2_zd65,

    # --- Reynolds Normal Stress (Radial: vv) ---
    "vv_zd25": ur2_zd25,
    "vv_zd35": ur2_zd35,
    "vv_zd45": ur2_zd45,
    "vv_zd55": ur2_zd55,
    "vv_zd65": ur2_zd65,

    # --- Reynolds Shear Stress (uv) ---
    "uv_zd25": ur_uz_zd25,
    "uv_zd35": ur_uz_zd35,
    "uv_zd45": ur_uz_zd45,
    "uv_zd55": ur_uz_zd55,
    "uv_zd65": ur_uz_zd65
})
df_CL.to_csv("DNS_processed_CL.csv", index=False)
df_profiles.to_csv("DNS_processed_profiles.csv", index=False)
