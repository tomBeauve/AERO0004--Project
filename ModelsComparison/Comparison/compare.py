import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Configuration ---
D = 0.2
MODELS = ["keps", "komSST"]
STATIONS = [25, 35, 45, 55, 65]
DNS_CL = "cleanData/DNS_processed_CL.csv"
DNS_PROF = "cleanData/DNS_processed_profiles.csv"


################# READ DATA AND STORE IN ARRAYS ################


def get_model_data(model_name):
    """Internal helper to read and parse CSVs for a single model."""
    cl_path = f'cleanData/CL_{model_name}.csv'
    prof_path = f'cleanData/profiles_{model_name}.csv'

    # Read Centerline
    df_cl = pd.read_csv(cl_path)
    cl_arrays = {
        'x': df_cl['x-coordinate'].values / D,
        'Uz': df_cl['axial-velocity'].values,
        'k': df_cl['turb-kinetic-energy'].values,
        'uu': df_cl['uu'].values,
        'vv': df_cl['vv'].values,
        'uv': df_cl['uv'].values,
        'inv_Uz': df_cl['axial-velocity'].values[0] / df_cl['axial-velocity'].values
    }

    # Read Profiles
    df_prof = pd.read_csv(prof_path)
    prof_arrays = {}
    for z_D in STATIONS:
        x_target = z_D * D
        mask = np.isclose(df_prof['x-coordinate'], x_target, atol=1e-4)
        station_df = df_prof[mask].sort_values('y-coordinate')

        if not station_df.empty:
            prof_arrays[f'r_zd{z_D}'] = station_df['y-coordinate'].values / D
            prof_arrays[f'Uz_zd{z_D}'] = station_df['axial-velocity'].values
            prof_arrays[f'Ur_zd{z_D}'] = station_df['radial-velocity'].values
            prof_arrays[f'uv_zd{z_D}'] = station_df['uv'].values

    return cl_arrays, prof_arrays


CL_results = {}
PROF_results = {}

for m in MODELS:
    cl, prof = get_model_data(m)
    CL_results[m] = cl
    PROF_results[m] = prof


df_dns_cl = pd.read_csv(DNS_CL)
CL_results["dns"] = {
    'x': df_dns_cl['x-coordinate'].values,
    'Uz': df_dns_cl['axial-velocity'].values,
    'k': df_dns_cl['turb-kinetic-energy'].values,
    'uu': df_dns_cl['uu'].values,
    'vv': df_dns_cl['vv'].values,
    'ww': df_dns_cl['ww'].values,
    'uv': df_dns_cl['uv'].values,
    'inv_Uz': df_dns_cl['axial-velocity'].values[0] / df_dns_cl['axial-velocity'].values
}

df_dns_prof = pd.read_csv(DNS_PROF)
PROF_results["dns"] = {}
for z_D in STATIONS:
    PROF_results["dns"][f'r_zd{z_D}'] = df_dns_prof['y-coordinate'].values
    PROF_results["dns"][f'Uz_zd{z_D}'] = df_dns_prof[f'Uz_zd{z_D}'].values
    PROF_results["dns"][f'Ur_zd{z_D}'] = df_dns_prof[f'Ur_zd{z_D}'].values


MODELS = ["keps", "komSST", "dns"]
D = 1
########## Inverse CL velocity ###############
plt.figure()
for m in MODELS:
    plt.plot(CL_results[m]['x']/D, CL_results[m]['inv_Uz'], label=m)
plt.xlabel('x/D')
plt.ylabel('$U_{exit}/U_{CL}$')
plt.title('Centerline Velocity Decay')
plt.legend()
plt.grid(True)
plt.show()


########### velocity profile Uz at z/D = 25 #########
plt.figure()
for z_D in [25]:
    for m in MODELS:
        plt.plot(PROF_results[m][f'r_zd{z_D}']/z_D,
                 PROF_results[m][f'Uz_zd{z_D}']/PROF_results[m][f'Uz_zd{z_D}'][0], label=m)
plt.xlabel('r')
plt.ylabel('Uz')

plt.legend()
plt.grid(True)
plt.show()
