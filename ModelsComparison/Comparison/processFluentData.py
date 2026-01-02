import pandas as pd
import numpy as np
import os

# Configuration
MODEL = 'komSST'
INPUT_FILE = f'rawData/solutionData_{MODEL}.csv'
RHO = 1
U_BULK = 1.0
STATIONS = [25, 35, 45, 55, 65]
D = 0.2

# Ensure output directory exists
if not os.path.exists('cleanData'):
    os.makedirs('cleanData')


def process_jet_data(filename):
    # Load data
    df = pd.read_csv(filename, skipinitialspace=True)

    # 1. Stress Reconstruction (Boussinesq Hypothesis)
    df['uu'] = 2 * df['viscosity-turb'] * df['daxial-velocity-dx'] - \
        (2/3) * RHO * df['turb-kinetic-energy']

    df['vv'] = 2 * df['viscosity-turb'] * df['dradial-velocity-dy'] - \
        (2/3) * RHO * df['turb-kinetic-energy']

    df['uv'] = df['viscosity-turb'] * \
        (df['daxial-velocity-dy'] + df['dradial-velocity-dx'])

    # 2. Generate Centerline File (CL.csv)
    # Increased tolerance to 1e-8 for safety
    cl_df = df[np.abs(df['y-coordinate']) < 1e-8].copy()
    cl_df = cl_df.sort_values(by='x-coordinate')

    cl_cols = ['x-coordinate', 'axial-velocity',
               'turb-kinetic-energy', 'uu', 'vv', 'uv']
    cl_df[cl_cols].to_csv(f'cleanData/CL_{MODEL}.csv', index=False)

    # 3. Extract CLEAN Radial Profiles
    profile_list = []

    for z_D in STATIONS:
        x_target = z_D * D

        # FIX: Use a tolerance window instead of exact match
        # This captures all nodes within 0.1% of the Diameter from the target plane
        tol = 0.001 * D
        station_df = df[np.abs(df['x-coordinate'] - x_target) < tol].copy()

        if not station_df.empty:
            # Sort by y to ensure smooth radial profiles
            station_df = station_df.sort_values('y-coordinate')

            # STANDARDISATION: Force the x-coordinate to be exactly the target.
            # This ensures np.isclose in your plotting script finds ALL these points.
            station_df['x-coordinate'] = x_target

            profile_list.append(station_df)
            print(
                f"Extracted {len(station_df)} points for z/D={z_D} at x={x_target}")
        else:
            print(
                f"Warning: No nodes found within tolerance for z/D={z_D} (target x={x_target})")

    # Combine all cleaned stations into one file
    if profile_list:
        final_profiles = pd.concat(profile_list)
        output_cols = ['x-coordinate', 'y-coordinate',
                       'axial-velocity', 'radial-velocity', 'uv']
        final_profiles[output_cols].to_csv(
            f'cleanData/profiles_{MODEL}.csv', index=False)
        print(
            f"\nSuccess: 'CL_{MODEL}.csv' and 'profiles_{MODEL}.csv' created.")
    else:
        print("\nError: No profile data was extracted. Check your station x-values vs mesh x-values.")


if __name__ == "__main__":
    process_jet_data(INPUT_FILE)
