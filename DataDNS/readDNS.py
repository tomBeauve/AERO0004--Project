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

# centerline and velocity at centerline
z_CL = z[r == 0]
Uz_CL = Uz[r == 0]
Ur_CL = Ur[r == 0]
Uphi_CL = Uphi[r == 0]

# velocity profiles at different z/D locations
r_profiles = r[z == 25]
Uz_zd25 = Uz[z == 25]
Ur_zd25 = Ur[z == 25]

Uz_zd35 = Uz[z == 35]
Ur_zd35 = Ur[z == 35]

Uz_zd45 = Uz[z == 45]
Ur_zd45 = Ur[z == 45]

Uz_zd55 = Uz[z == 55]
Ur_zd55 = Ur[z == 55]

Uz_zd65 = Uz[z == 65]
Ur_zd65 = Ur[z == 65]


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
    "Uz_zd25": Uz_zd25,
    "Ur_zd25": Ur_zd25,
    "Uz_zd35": Uz_zd35,
    "Ur_zd35": Ur_zd35,
    "Uz_zd45": Uz_zd45,
    "Ur_zd45": Ur_zd45,
    "Uz_zd55": Uz_zd45,
    "Ur_zd55": Ur_zd55,
    "Uz_zd65": Uz_zd65,
    "Ur_zd65": Ur_zd65
})

df_CL.to_csv("DNS_processed_CL.csv", index=False)
df_profiles.to_csv("DNS_processed_profiles.csv", index=False)
