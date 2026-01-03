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


plt.rcParams.update({
    "text.usetex": True,              # Use LaTeX for all text rendering
    "image.cmap": "cividis",
    "font.family": "serif",           # Use LaTeX's default font family
    # Use Computer Modern for a LaTeX-like font
    "font.serif": ["Times New Roman"],
    "font.size": 12,                  # Global font size to match LaTeX
    "axes.titlesize": 14,             # Font size for title
    "axes.labelsize": 14,             # Font size for axis labels
    "xtick.labelsize": 12,            # Font size for x-axis ticks
    "ytick.labelsize": 12,            # Font size for y-axis ticks
    "legend.fontsize": 12,             # Font size for legend
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

# Use alpha (transparency) to distinguish locations without adding more colors
# 1.0 is the furthest station (most developed), lower is closer to inlet
STATION_ALPHAS = {25: 0.3, 35: 0.45, 45: 0.6, 55: 0.8, 65: 1.0}


########## Inverse CL velocity ###############
plt.figure()
for m in MODELS:
    plt.plot(
        CL_results[m]['x'],
        CL_results[m]['inv_Uz'],
        color=MODEL_CFG[m]['color'],
        linestyle=MODEL_CFG[m]['ls'],
        linewidth=MODEL_CFG[m]['lw'],
        label=MODEL_CFG[m]['label']
    )
plt.xlabel(r'$z/D$')
plt.ylabel('$U_{exit}/U_{CL}$')
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.title('Centerline Velocity Decay')
plt.legend()
plt.grid(True)
plt.show()

########### velocity profile Uz #########
plt.figure()
for z_D in STATIONS:
    for m in MODELS:
        current_label = MODEL_CFG[m]['label'] if z_D == STATIONS[-1] else ""

        plt.plot(
            PROF_results[m][f'r_zd{z_D}'] / z_D,
            PROF_results[m][f'Uz_zd{z_D}'] / PROF_results[m][f'Uz_zd{z_D}'][0],
            color=MODEL_CFG[m]['color'],
            linestyle=MODEL_CFG[m]['ls'],
            linewidth=MODEL_CFG[m]['lw'],
            alpha=STATION_ALPHAS[z_D],
            label=current_label
        )
plt.xlabel(r'$\eta$')
plt.ylabel(r'$\bar{U_z}/\bar{U}_{z,c}$')
plt.xlim((0, 0.4))
plt.legend()
plt.grid(True)
plt.show()


########### velocity profile Ur #########
plt.figure()
for z_D in STATIONS:
    for m in MODELS:
        current_label = MODEL_CFG[m]['label'] if z_D == STATIONS[-1] else ""

        # Note: Ur is normalized by the centerline AXIAL velocity (Uz,c)
        # to show its relative magnitude to the primary flow.
        plt.plot(
            PROF_results[m][f'r_zd{z_D}'] / z_D,
            PROF_results[m][f'Ur_zd{z_D}'] / PROF_results[m][f'Uz_zd{z_D}'][0],
            color=MODEL_CFG[m]['color'],
            linestyle=MODEL_CFG[m]['ls'],
            linewidth=MODEL_CFG[m]['lw'],
            alpha=STATION_ALPHAS[z_D],
            label=current_label
        )
plt.xlabel(r'$\eta$')
plt.ylabel(r'$\bar{U_r}/\bar{U}_{z,c}$')
plt.xlim((0, 0.4))
plt.legend()
plt.grid(True)
plt.show()

########## CL velocity tilde ( Uzc * z ) = B_u D U_0 ###############
plt.figure()
for m in MODELS:
    plt.plot(
        CL_results[m]['x'],
        CL_results[m]['Uz'] * (CL_results[m]['x']),
        color=MODEL_CFG[m]['color'],
        linestyle=MODEL_CFG[m]['ls'],
        linewidth=MODEL_CFG[m]['lw'],
        label=MODEL_CFG[m]['label']
    )
plt.xlabel(r'$z/D$')
plt.ylabel(r'$\tilde{\bar{U_z}}(\eta = 0)$')
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.title('vel CL decay constant')
plt.legend()
plt.grid(True)
plt.show()


########## reynolds stress zz on CL ###############

plt.figure()
for m in MODELS:
    plt.plot(
        CL_results[m]['x'],
        np.sqrt(CL_results[m]['uu'])/CL_results[m]['Uz'],
        color=MODEL_CFG[m]['color'],
        linestyle=MODEL_CFG[m]['ls'],
        linewidth=MODEL_CFG[m]['lw'],
        label=MODEL_CFG[m]['label']
    )

plt.xlabel(r'$z/D$')
plt.ylabel(r"$\sqrt{\bar{u_z'^2}}/ \bar{U}_{z,c} $")
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.title('reynolds stress zz')
plt.legend()
plt.grid(True)
plt.show()

########## reynolds stress rr on CL ###############

plt.figure()
for m in MODELS:
    plt.plot(
        CL_results[m]['x'],
        np.sqrt(CL_results[m]['vv'])/CL_results[m]['Uz'],
        color=MODEL_CFG[m]['color'],
        linestyle=MODEL_CFG[m]['ls'],
        linewidth=MODEL_CFG[m]['lw'],
        label=MODEL_CFG[m]['label']
    )
plt.xlabel(r'$z/D$')
plt.ylabel(r"$\sqrt{\bar{u_r'^2}}/ \bar{U}_{z,c} $")
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.title('reynolds stress rr')
plt.legend()
plt.grid(True)
plt.show()

########## reynolds stress rr at zd locations ###############

plt.figure()
for z_D in STATIONS:
    for m in MODELS:
        plt.plot(
            PROF_results[m][f'r_zd{z_D}']/z_D,
            PROF_results[m][f'vv_zd{z_D}'] /
            PROF_results[m][f'Uz_zd{z_D}'][0]**2,
            color=MODEL_CFG[m]['color'],
            linestyle=MODEL_CFG[m]['ls'],
            linewidth=MODEL_CFG[m]['lw'],
            alpha=STATION_ALPHAS[z_D],
            label=current_label
        )
plt.xlabel(r'$\eta$')
plt.ylabel(r"$\bar{u'_i u'_j}/ \bar{U}_{z,c}^2 $")
plt.xlim((0, 0.4))
plt.title('reynolds stress rr')
plt.legend()
plt.grid(True)
plt.show()

########## reynolds stress zz at zd locations ###############

plt.figure()
for z_D in STATIONS:
    for m in MODELS:
        plt.plot(
            PROF_results[m][f'r_zd{z_D}']/z_D,
            (PROF_results[m][f'uu_zd{z_D}']) /
            PROF_results[m][f'Uz_zd{z_D}'][0]**2,
            color=MODEL_CFG[m]['color'],
            linestyle=MODEL_CFG[m]['ls'],
            linewidth=MODEL_CFG[m]['lw'],
            alpha=STATION_ALPHAS[z_D],
            label=current_label
        )
plt.xlabel(r'$\eta$')
plt.ylabel(r"$\bar{u'_i u'_j}/ \bar{U}_{z,c}^2 $")
plt.xlim((0, 0.4))
plt.title('reynolds stress zz')
plt.legend()
plt.grid(True)
plt.show()

########## reynolds stress rz at zd locations ###############

plt.figure()
for z_D in STATIONS:
    for m in MODELS:
        plt.plot(
            PROF_results[m][f'r_zd{z_D}']/z_D,
            (PROF_results[m][f'uv_zd{z_D}']) /
            PROF_results[m][f'Uz_zd{z_D}'][0]**2,
            color=MODEL_CFG[m]['color'],
            linestyle=MODEL_CFG[m]['ls'],
            linewidth=MODEL_CFG[m]['lw'],
            alpha=STATION_ALPHAS[z_D],
            label=current_label
        )
plt.xlabel(r'$\eta$')
plt.ylabel(r"$\bar{u'_i u'_j}/ \bar{U}_{z,c}^2 $")
plt.xlim((0, 0.4))
plt.title('reynolds stress rz')
plt.legend()
plt.grid(True)
plt.show()


########## Decay constant Bu ###############
plt.figure()
for m in MODELS:
    plt.plot(
        CL_results[m]['x'],
        CL_results[m]['Uz'] / CL_results[m]['Uz'][0] * (CL_results[m]['x']),
        color=MODEL_CFG[m]['color'],
        linestyle=MODEL_CFG[m]['ls'],
        linewidth=MODEL_CFG[m]['lw'],
        label=MODEL_CFG[m]['label']
    )
plt.xlabel(r'$z/D$')
plt.ylabel('$U_{exit}/U_{CL}$')
plt.xlim((0, 75))
plt.xticks([0, 20, 40, 60])
plt.title('Centerline Velocity Decay')
plt.legend()
plt.grid(True)
plt.show()
