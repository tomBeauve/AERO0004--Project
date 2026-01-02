import pandas as pd
import numpy as np

# Configuration
MODEL = 'komSST'
INPUT_FILE = f'rawData/solutionData_{MODEL}.csv'
RHO = 1  # Ensure this matches your Fluent fluid density
U_BULK = 1.0  # For potential non-dimensionalization
STATIONS = [25, 35, 45, 55, 65]
D = 0.2


def process_jet_data(filename):
    # Load data - skipping initial spaces if any in headers
    df = pd.read_csv(filename, skipinitialspace=True)

    # 1. Stress Reconstruction (Boussinesq Hypothesis)
    # uu = -rho * <u'u'>
    df['uu'] = 2 * df['viscosity-turb'] * df['daxial-velocity-dx'] - \
        (2/3) * RHO * df['turb-kinetic-energy']

    # vv = -rho * <v'v'>
    df['vv'] = 2 * df['viscosity-turb'] * df['dradial-velocity-dy'] - \
        (2/3) * RHO * df['turb-kinetic-energy']

    # uv = -rho * <u'v'> (Shear Stress)
    df['uv'] = df['viscosity-turb'] * \
        (df['daxial-velocity-dy'] + df['dradial-velocity-dx'])

    # 2. Generate Centerline File (CL.csv)
    # Filter where y (radial) is near zero
    cl_df = df[np.abs(df['y-coordinate']) < 1e-5].copy()
    cl_df = cl_df.sort_values(by='x-coordinate')

    cl_cols = ['x-coordinate', 'axial-velocity',
               'turb-kinetic-energy', 'uu', 'vv', 'uv']
    cl_df[cl_cols].to_csv(f'cleanData/CL_{MODEL}.csv', index=False)

    # 3. Extract CLEAN Radial Profiles (profiles.csv)
    profile_list = []

    # Find the unique X-coordinates available in the mesh
    available_x = df['x-coordinate'].unique()

    for z_D in STATIONS:
        x_target = z_D * D
        # Find the closest actual x in the mesh to our target z/D
        closest_x = available_x[np.abs(available_x - x_target).argmin()]

        # Filter for this specific X-plane
        # AND exclude the centerline point if it causes "spikes" in radial plots
        station_df = df[df['x-coordinate'] == closest_x].copy()

        if not station_df.empty:
            station_df = station_df.sort_values('y-coordinate')
            profile_list.append(station_df)
            print(f"Extracted Station z/D={z_D} at mesh x={closest_x:.4f}")

    # Combine all cleaned stations into one file
    if profile_list:
        final_profiles = pd.concat(profile_list)
        # Only save the columns you need for the arrays
        output_cols = ['x-coordinate', 'y-coordinate',
                       'axial-velocity', 'radial-velocity', 'uv']
        final_profiles[output_cols].to_csv(
            f'cleanData/profiles_{MODEL}.csv', index=False)

    print(
        f"Success: 'CL.csv' ({len(cl_df)} pts) and 'profiles.csv' ({len(df)} pts) created.")


if __name__ == "__main__":
    process_jet_data(INPUT_FILE)
