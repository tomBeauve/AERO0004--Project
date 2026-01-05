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
slide_params = {
    # Text Sizes (Large for visibility)
    'font.size': 20,           # General default
    'axes.labelsize': 28,      # x and y labels
    'axes.titlesize': 24,      # Title
    'xtick.labelsize': 20,     # Tick numbers
    'ytick.labelsize': 20,
    'legend.fontsize': 18,     # Legend text

    # axes are dark grey
    'axes.edgecolor': "#7D7D7D",    # Dark grey spines
    'xtick.color': '#7D7D7D',       # Dark grey ticks
    'ytick.color': '#7D7D7D',
    'axes.labelcolor': '#7D7D7D',

    # Line & Marker Geometries (Thick for projectors)
    'lines.linewidth': 5,    # Thicker data lines
    'lines.markersize': 2,    # Much larger markers (default was too small)
    'lines.markeredgewidth': 0,  # Remove marker outline for cleaner look

    # Structural Geometries
    'axes.linewidth': 2.0,     # Thicker spines (box)
    'xtick.major.width': 2.0,  # Thicker ticks
    'ytick.major.width': 2.0,
    'xtick.major.size': 8.0,   # Longer ticks
    'ytick.major.size': 8.0,

    # Slide Aesthetics
    'font.family': 'sans-serif',  # Sans-serif is more legible on slides than serif
    'figure.autolayout': True,   # Similar to tight_layout
    'figure.figsize': (12, 9),   # 16:9 Aspect Ratio by default
}


plt.rcParams.update(slide_params)


MODEL_CFG = {
    'dns':    {'color': 'black',  'ls': '-', 'label': 'DNS'},
    'keps':   {'color': '#1f77b4', 'ls': '--', 'label': r'$k$-$\epsilon$'},
    'komSST': {'color': '#d62728', 'ls': '-.', 'label': r'$k$-$\omega$ SST'}
}

STATION_ALPHAS = {25: 0.3, 35: 0.45, 45: 0.6, 55: 0.8, 65: 1.0}


def finalize_plot(filename, show_grid=True):
    ax = plt.gca()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.yaxis.label.set_rotation(0)
    ax.yaxis.label.set_horizontalalignment('right')
    ax.yaxis.label.set_verticalalignment('center')

    ax.yaxis.labelpad = 10

    if show_grid == "horizontal":
        ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.8)
    elif show_grid:
        ax.grid(True, which='major', axis='both', linestyle='--', alpha=0.8)

    plt.tight_layout()
    plt.savefig(output_dir / f"{filename}.svg", bbox_inches='tight', dpi=300)
    plt.savefig(output_dir / f"{filename}.pdf", bbox_inches='tight', dpi=300)

    plt.close()


# Inverse CL velocity
for m in MODELS:
    plt.plot(CL_results[m]['x'], CL_results[m]['inv_Uz'], **MODEL_CFG[m])
    plt.text(CL_results[m]['x'][-1] + 1, CL_results[m]['inv_Uz'][-1], MODEL_CFG[m]['label'],
             color=MODEL_CFG[m]['color'],
             va='center', fontweight='bold', fontsize=22)
plt.xlabel(r'$z/D$')
plt.ylabel(r'$ \frac{U_{exit}}{U_{z,CL}}$', fontsize=32)

plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.yticks([14.7, 19, 24.7], ["14.7", "19", "24.7"])
# plt.legend()
finalize_plot("centerline_decay_inverse", show_grid="horizontal")

# Velocity profile Uz (Self-similar)
for z_D in STATIONS:
    for m in MODELS:
        plot_settings = MODEL_CFG[m].copy()

        if z_D != STATIONS[-1]:
            plot_settings['label'] = ""
        else:
            yLoc = 0
            if m == 'dns':
                xLoc = 0.12
                yLoc = 0.1
            if m == 'keps':
                xLoc = 0.225
                yLoc = 0.2
            if m == 'komSST':
                xLoc = 0.2
                yLoc = 0.3
            plt.text(xLoc, yLoc, MODEL_CFG[m]['label'],
                     color=MODEL_CFG[m]['color'],
                     va='center', fontweight='bold', fontsize=22)
        plt.plot(PROF_results[m][f'r_zd{z_D}'] / z_D,
                 PROF_results[m][f'Uz_zd{z_D}'] /
                 PROF_results[m][f'Uz_zd{z_D}'][0],
                 **plot_settings, alpha=STATION_ALPHAS[z_D])
plt.xlabel(r'$\eta$')
plt.ylabel(r'$\frac{\bar{U}_z}{\bar{U}_{z,c}}$', fontsize=32)
plt.xlim((0, 0.4))
plt.ylim((0, None))
plt.xticks([0, 0.1, 0.2, 0.3, 0.4])
plt.legend()
finalize_plot("profile_Uz_similarity", show_grid=False)


# Reynolds stress zz (Centerline)
for m in MODELS:
    plt.plot(CL_results[m]['x'], np.sqrt(CL_results[m]
             ['uu'])/CL_results[m]['Uz'], **MODEL_CFG[m])
    plt.text(CL_results[m]['x'][-1] + 1, np.sqrt(CL_results[m]
             ['uu'][-1])/CL_results[m]['Uz'][-1], MODEL_CFG[m]['label'],
             color=MODEL_CFG[m]['color'],
             va='center', fontweight='bold', fontsize=22)
plt.xlabel(r'$z/D$')
plt.ylabel(r"$\frac{\sqrt{\overline{u_z'^2}}}{\bar{U}_{z,c}}$", fontsize=32)
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.yticks([0.05, 0.13,  0.235, 0.3], ["0.05", "0.13", "0.24", "0.3"])


plt.legend()
finalize_plot("cl_reynolds_stress_zz", show_grid="horizontal")


# Profiles: Reynolds stress rz (Shear)
for z_D in STATIONS:
    for m in MODELS:
        plot_settings = MODEL_CFG[m].copy()

        if z_D != STATIONS[-1]:
            plot_settings['label'] = ""
        else:
            if m == 'dns':
                xLoc = 0.11
                yLoc = 0.015
            if m == 'keps':
                xLoc = 0.2
                yLoc = 0.012
            if m == 'komSST':
                xLoc = 0.12
                yLoc = 0.025
            plt.text(xLoc, yLoc, MODEL_CFG[m]['label'],
                     color=MODEL_CFG[m]['color'],
                     va='center', fontweight='bold', fontsize=22)
        plt.plot(PROF_results[m][f'r_zd{z_D}']/z_D,
                 PROF_results[m][f'uv_zd{z_D}'] /
                 PROF_results[m][f'Uz_zd{z_D}'][0]**2,
                 **plot_settings, alpha=STATION_ALPHAS[z_D])
plt.xlabel(r'$\eta$')
plt.ylabel(r"$\frac{\overline{u_r' u_z'}}{\bar{U}_{z,c}^2}$", fontsize=32)
plt.xlim((0, 0.4))
plt.ylim((-0.0001, None))
plt.xticks([0, 0.1, 0.2, 0.3, 0.4])
plt.yticks([0, 0.019, 0.025], ["0", "0.019", "0.025"])
finalize_plot("profile_reynolds_rz", show_grid="horizontal")
