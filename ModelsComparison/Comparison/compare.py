import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Load Data ---

D = 0.2
z_over_D_stations = [25, 35, 45, 55, 65]

model = "keps"
INPUT_CL = f'cleanData/CL_{model}.csv'
INPUT_PROF = f'cleanData/profiles_{model}.csv'


STATIONS = [25, 35, 45, 55, 65]


def load_target_arrays():
    # 1. Load Centerline Data
    df_cl = pd.read_csv(INPUT_CL)
    arrays = {
        'x_CL': df_cl['x-coordinate'].values,
        'Uz_CL': df_cl['axial-velocity'].values,
        'k_CL': df_cl['turb-kinetic-energy'].values,
        'uu_CL': df_cl['uu'].values,
        'vv_CL': df_cl['vv'].values,
        'uv_CL': df_cl['uv'].values
    }

    # 2. Load Profile Data
    df_prof = pd.read_csv(INPUT_PROF)

    for z_D in STATIONS:
        x_target = z_D * D

        # Filter with a tolerance for mesh coordinates
        mask = np.isclose(df_prof['x-coordinate'], x_target, atol=1e-4)
        station_df = df_prof[mask].sort_values('y-coordinate')

        if not station_df.empty:
            # Descriptive keys as requested
            arrays[f'r_zd{z_D}'] = station_df['y-coordinate'].values
            arrays[f'Uz_zd{z_D}'] = station_df['axial-velocity'].values
            arrays[f'Ur_zd{z_D}'] = station_df['radial-velocity'].values
            arrays[f'uv_zd{z_D}'] = station_df['uv'].values
        else:
            print(f"Warning: No data found for z/D = {z_D} (x = {x_target})")

    return arrays


# Execute
data = load_target_arrays()
print("Available arrays:", data.keys())
