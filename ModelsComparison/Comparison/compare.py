from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd

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
            prof_arrays[f'uu_zd{z_D}'] = station_df['uu'].values
            prof_arrays[f'vv_zd{z_D}'] = station_df['vv'].values

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
    PROF_results["dns"][f'uu_zd{z_D}'] = df_dns_prof[f'uu_zd{z_D}'].values
    PROF_results["dns"][f'vv_zd{z_D}'] = df_dns_prof[f'vv_zd{z_D}'].values
    PROF_results["dns"][f'uv_zd{z_D}'] = df_dns_prof[f'uv_zd{z_D}'].values


MODELS.append("dns")
D = 1


# Create directory for figures if it doesn't exist
output_dir = Path("figures")
output_dir.mkdir(exist_ok=True)

# --- Configuration ---
plt.rcParams.update({
    "text.usetex": True,              # Use LaTeX for all text rendering
    "image.cmap": "cividis",
    "font.family": "serif",           # Use LaTeX's default font family
    # Use Computer Modern for a LaTeX-like font
    "font.serif": ["Times New Roman"],
    "font.size": 12,                  # Global font size to match LaTeX
    "axes.titlesize": 18,             # Font size for title
    "axes.labelsize": 18,             # Font size for axis labels
    "xtick.labelsize": 16,            # Font size for x-axis ticks
    "ytick.labelsize": 16,            # Font size for y-axis ticks
    "legend.fontsize": 16,             # Font size for legend
    "axes.grid": True,
    "grid.color": "0.9",
    "grid.linewidth": 0.7,
    "grid.alpha": 0.9
})

MODEL_CFG = {
    'dns':    {'color': 'black',  'ls': '-',  'lw': 1.5, 'label': 'DNS'},
    'keps':   {'color': '#1f77b4', 'ls': '--', 'lw': 1.5, 'label': r'$k$-$\epsilon$'},
    'komSST': {'color': '#d62728', 'ls': '-.', 'lw': 1.5, 'label': r'$k$-$\omega$ SST'}
}

STATION_ALPHAS = {25: 0.3, 35: 0.45, 45: 0.6, 55: 0.8, 65: 1.0}

# Helper to avoid repetitive code and save figures


def finalize_plot(filename):
    plt.tight_layout()
    plt.savefig(output_dir / f"{filename}.pdf", bbox_inches='tight', dpi=300)
    plt.show()


# 1. Inverse CL velocity
plt.figure(figsize=(8, 4))
for m in MODELS:
    plt.plot(CL_results[m]['x'], CL_results[m]['inv_Uz'], **MODEL_CFG[m])
plt.xlabel(r'$z/D$')
plt.ylabel(r'$U_{exit}/U_{z,CL}$')
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.legend()
finalize_plot("centerline_decay_inverse")

# 2. Velocity profile Uz (Self-similar)
plt.figure(figsize=(8, 4))
for z_D in STATIONS:
    for m in MODELS:
        plot_settings = MODEL_CFG[m].copy()

        # Only keep the label for the last station to avoid legend clutter
        if z_D != STATIONS[-1]:
            plot_settings['label'] = ""
        plt.plot(PROF_results[m][f'r_zd{z_D}'] / z_D,
                 PROF_results[m][f'Uz_zd{z_D}'] /
                 PROF_results[m][f'Uz_zd{z_D}'][0],
                 **plot_settings, alpha=STATION_ALPHAS[z_D])
plt.xlabel(r'$\eta$')
plt.ylabel(r'$\bar{U}_z/\bar{U}_{z,c}$')
plt.xlim((0, 0.4))
plt.xticks([0, 0.1, 0.2, 0.3, 0.4])
plt.legend()
finalize_plot("profile_Uz_similarity")

# 3. Velocity profile Ur
plt.figure(figsize=(8, 4))
for z_D in STATIONS:
    for m in MODELS:
        plot_settings = MODEL_CFG[m].copy()

        # Only keep the label for the last station to avoid legend clutter
        if z_D != STATIONS[-1]:
            plot_settings['label'] = ""
        plt.plot(PROF_results[m][f'r_zd{z_D}'] / z_D,
                 PROF_results[m][f'Ur_zd{z_D}'] /
                 PROF_results[m][f'Uz_zd{z_D}'][0],
                 **plot_settings, alpha=STATION_ALPHAS[z_D])
plt.xlabel(r'$\eta$')
plt.ylabel(r'$\bar{U}_r/\bar{U}_{z,c}$')
plt.xlim((0, 0.4))
plt.xticks([0, 0.1, 0.2, 0.3, 0.4])

plt.legend()
finalize_plot("profile_Ur_similarity")

# 4. Reynolds stress zz (Centerline)
plt.figure(figsize=(8, 4))
for m in MODELS:
    plt.plot(CL_results[m]['x'], np.sqrt(CL_results[m]
             ['uu'])/CL_results[m]['Uz'], **MODEL_CFG[m])
plt.xlabel(r'$z/D$')
plt.ylabel(r"$\sqrt{\overline{u_z'^2}}/ \bar{U}_{z,c}$")
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.legend()
finalize_plot("cl_reynolds_stress_zz")

# 5. Reynolds stress rr (Centerline)
plt.figure(figsize=(8, 4))
for m in MODELS:
    plt.plot(CL_results[m]['x'], np.sqrt(CL_results[m]
             ['vv'])/CL_results[m]['Uz'], **MODEL_CFG[m])
plt.xlabel(r'$z/D$')
plt.ylabel(r"$\sqrt{\overline{u_r'^2}}/ \bar{U}_{z,c}$")
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.legend()
finalize_plot("cl_reynolds_stress_rr")

# 6. Profiles: Reynolds stress rr
plt.figure(figsize=(8, 4))
for z_D in STATIONS:
    for m in MODELS:
        plot_settings = MODEL_CFG[m].copy()

        # Only keep the label for the last station to avoid legend clutter
        if z_D != STATIONS[-1]:
            plot_settings['label'] = ""
        plt.plot(PROF_results[m][f'r_zd{z_D}']/z_D,
                 PROF_results[m][f'vv_zd{z_D}'] /
                 PROF_results[m][f'Uz_zd{z_D}'][0]**2,
                 **plot_settings, alpha=STATION_ALPHAS[z_D])
plt.xlabel(r'$\eta$')
plt.ylabel(r"$\overline{u_r' u_r'}/ \bar{U}_{z,c}^2$")
plt.xlim((0, 0.4))
plt.xticks([0, 0.1, 0.2, 0.3, 0.4])
plt.legend()
finalize_plot("profile_reynolds_rr")

# 7. Profiles: Reynolds stress zz
plt.figure(figsize=(8, 4))
for z_D in STATIONS:
    for m in MODELS:
        plot_settings = MODEL_CFG[m].copy()

        # Only keep the label for the last station to avoid legend clutter
        if z_D != STATIONS[-1]:
            plot_settings['label'] = ""
        plt.plot(PROF_results[m][f'r_zd{z_D}']/z_D,
                 PROF_results[m][f'uu_zd{z_D}'] /
                 PROF_results[m][f'Uz_zd{z_D}'][0]**2,
                 **plot_settings, alpha=STATION_ALPHAS[z_D])
plt.xlabel(r'$\eta$')
plt.ylabel(r"$\overline{u_z' u_z'}/ \bar{U}_{z,c}^2$")
plt.xlim((0, 0.4))
plt.xticks([0, 0.1, 0.2, 0.3, 0.4])
plt.legend()
finalize_plot("profile_reynolds_zz")

# 8. Profiles: Reynolds stress rz (Shear)
plt.figure(figsize=(8, 4))
for z_D in STATIONS:
    for m in MODELS:
        plot_settings = MODEL_CFG[m].copy()

        # Only keep the label for the last station to avoid legend clutter
        if z_D != STATIONS[-1]:
            plot_settings['label'] = ""
        plt.plot(PROF_results[m][f'r_zd{z_D}']/z_D,
                 PROF_results[m][f'uv_zd{z_D}'] /
                 PROF_results[m][f'Uz_zd{z_D}'][0]**2,
                 **plot_settings, alpha=STATION_ALPHAS[z_D])
plt.xlabel(r'$\eta$')
plt.ylabel(r"$\overline{u_r' u_z'}/ \bar{U}_{z,c}^2$")
plt.xlim((0, 0.4))
plt.xticks([0, 0.1, 0.2, 0.3, 0.4])
plt.legend()
finalize_plot("profile_reynolds_rz")


#### computing decay constant #####

def compute_jet_constants(z_D, inv_Uz, start_zD=25):
    # Filter for the fully developed region
    mask = z_D > start_zD
    x = z_D[mask]
    y = inv_Uz[mask]

    # Linear fit: y = m*x + c
    m, c = np.polyfit(x, y, 1)

    Bu = 1 / m
    z0 = -c / m

    return Bu, z0


# Example usage for your models:
for m in MODELS:
    Bu, z0 = compute_jet_constants(CL_results[m]['x'], CL_results[m]['inv_Uz'])
    print(f"Model {m}: Bu = {Bu:.3f}, z0/D = {z0:.3f}")


def compute_spreading_rate(m, stations, prof_data):
    r_half_list = []
    z_list = []

    for z_D in stations:
        # Already r/D if D was set to 1 or handled in get_data
        r = prof_data[m][f'r_zd{z_D}']
        Uz = prof_data[m][f'Uz_zd{z_D}']
        Uz_center = Uz[0]

        # Interpolate to find r where Uz/Uz_center = 0.5
        # We only look at the positive r-branch
        f_interp = interp1d(Uz/Uz_center, r, kind='linear')
        try:
            r_half = f_interp(0.5)
            r_half_list.append(r_half)
            z_list.append(z_D)
        except ValueError:
            print(f"Warning: Could not find r0.5 for {m} at z/D={z_D}")

    # Linear fit: r_half = S * z + C
    S, C = np.polyfit(z_list, r_half_list, 1)
    z0_spreading = -C / S

    return S, z0_spreading


# Calculate and print for all models
print("\n--- Jet Spreading Analysis ---")
for m in MODELS:
    S, z0_s = compute_spreading_rate(m, STATIONS, PROF_results)
    print(f"Model {m}: Spreading Rate (S) = {S:.4f}, z0/D = {z0_s:.3f}")


z_fit = np.linspace(min(STATIONS) - 10, max(STATIONS) + 10, 200)

for m in MODELS:
    r_half_list = []
    z_list = []

    for z_D in STATIONS:
        r = PROF_results[m][f'r_zd{z_D}']
        Uz = PROF_results[m][f'Uz_zd{z_D}']
        Uz_center = Uz[0]

        f_interp = interp1d(Uz / Uz_center, r, kind='linear')
        try:
            r_half = f_interp(0.5)
            r_half_list.append(r_half)
            z_list.append(z_D)
        except ValueError:
            continue

    z_list = np.array(z_list)
    r_half_list = np.array(r_half_list)

    # Scatter: stations
    plt.scatter(
        z_list,
        r_half_list,
        color=MODEL_CFG[m]['color'],
        s=40,
        zorder=3
    )

    # Linear fit
    S, C = np.polyfit(z_list, r_half_list, 1)
    plt.plot(
        z_fit,
        S * z_fit + C,
        **MODEL_CFG[m]
    )

plt.xlabel(r'$z/D$')
plt.ylabel(r'$r_{1/2}/D$')
plt.xlim((20, 75))
plt.xticks([20, 40, 60])
plt.legend()
finalize_plot("jet_spreading_rate")
