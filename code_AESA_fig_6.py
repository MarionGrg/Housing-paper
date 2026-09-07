# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 21:09:39 2026

@author: mageo
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%% import statistical data

stat_data = pd.read_excel("stat_values_AESA_indiv_3a.xlsx", index_col=0)
PBs = pd.read_excel("AESA_values_for_graph.xlsx", sheet_name='PBs', index_col=0)

categories = stat_data.index.to_list()

stat_norm = {}
for i in range(len(categories)):
    stat_norm[categories[i]] = stat_data.loc[categories[i]]/PBs['economic'][categories[i]]
    
stat_norm = pd.DataFrame(stat_norm)
stat_norm = stat_norm.transpose()

gf_by_econ = PBs['grandfathering']/PBs['economic']
gf_by_econ = gf_by_econ.to_list()
PBs['gf/econ'] = PBs['grandfathering']/PBs['economic']
median = stat_norm['median'].to_list()
perc_1 = stat_norm['1st perc'].to_list()
perc_0_1 = stat_norm['0.1th perc'].to_list()
perc_0_01 = stat_norm['0.01th perc'].to_list()
perc_5 = stat_norm['5th perc'].to_list()
perc_25 = stat_norm['25th perc'].to_list()
perc_75 = stat_norm['75th perc'].to_list()
perc_95 = stat_norm['95th perc'].to_list()

#%%

# climate change
# median normalized > 1
# gf / econ > 1
# green up to 1
# yellow from 1 to gf/econ
# red from gf/econ to median

# FW ecotoxicity
# median normalized > 1
# gf / econ < 1
# green up to gf/econ
# yellow from gf/econ to 1
# red from 1 to median

# terrestrial acidification
# median normalized < 1
# gf / econ < 1 and median < gf/econ
# green up to median
# yellow from gf/econ to 1

# land use
# median normalized < 1
# gf / econ < 1 and median < gf/econ
# green up to median
# yellow from gf/econ to 1

# human tox nc
# median normalized > 1
# gf / econ > 1
# green up to 1
# yellow from 1 to gf/econ
# red from gf/econ to median

# particulate matter
# median normalized > 1
# gf / econ > 1
# green up to 1
# yellow from 1 to gf/econ
# red from gf/econ to median

green_top = [1, gf_by_econ[1], median[2], median[3], 1, 1]
log_green_top = [np.log10(1+50*x) for x in green_top]

hashed_green_bottom = [0, gf_by_econ[1], gf_by_econ[2], gf_by_econ[3], 0, 0]
hashed_green_top = [0, 1, 1, 1, 0, 0]
log_hashed_green_bottom = [np.log10(1+50*x) for x in hashed_green_bottom]
log_hashed_green_top = [np.log10(1+50*x) for x in hashed_green_top]

hashed_red_bottom = [1, 0, 0, 0, 1, 1]
hashed_red_top = [gf_by_econ[0], 0, 0, 0, gf_by_econ[4], gf_by_econ[5]]
log_hashed_red_bottom = [np.log10(1+50*x) for x in hashed_red_bottom]
log_hashed_red_top = [np.log10(1+50*x) for x in hashed_red_top]

red_bottom = [gf_by_econ[0], 1, 0, 0, gf_by_econ[4], gf_by_econ[5]]
red_top = [median[0], median[1], 0, 0, median[4], median[5]]
log_red_bottom = [np.log10(1+50*x) for x in red_bottom]
log_red_top = [np.log10(1+50*x) for x in red_top]

log_perc_1 = [np.log10(1+50*x) for x in perc_1]
log_perc_0_1 = [np.log10(1+50*x) for x in perc_0_1]
log_perc_0_01 = [np.log10(1+50*x) for x in perc_0_01]

#%%


def add_polar_boxplot(ax, theta_center, width,
                      r_min, q1, median, q3, r_max,
                      facecolor="#4C78A8", edgecolor="black",
                      alpha=0.35, lw=1, cap_frac=0.25, zorder=3):
    """
    Draw a boxplot at angle theta_center (radians) on a polar axis `ax`.

    Parameters
    ----------
    ax : matplotlib axis with projection='polar'
    theta_center : float (radians)
        Center angle of the boxplot.
    width : float (radians)
        Angular width of the box (box spans [center - width/2, center + width/2]).
    r_min, q1, median, q3, r_max : floats
        Five-number summary in *radial* units (must satisfy r_min <= q1 <= median <= q3 <= r_max).
    facecolor, edgecolor : colors
        Box (wedge) face & edge colors.
    alpha : float
        Wedge transparency.
    lw : float
        Line width for median, whiskers, and caps.
    cap_frac : float in (0,1)
        Fraction of the angular width used for the whisker end caps.
    zorder : int
        Drawing order.
    """
    th0 = theta_center - width/2
    th1 = theta_center + width/2
    th = np.linspace(th0, th1, 64)

    # --- Box edges (Q1, Q3) as arcs
    ax.plot(th, np.full_like(th, q1), color='black', lw=lw, zorder=zorder)
    ax.plot(th, np.full_like(th, q3), color='black', lw=lw, zorder=zorder)
    ax.plot([th0, th0], [q1, q3], color=edgecolor, lw=lw, zorder=zorder+1)
    ax.plot([th1, th1], [q1, q3], color=edgecolor, lw=lw, zorder=zorder+1)

    # --- Median line across the box (constant radius = median, spanning the wedge)
    ax.plot([th0, th1], [median, median], color=edgecolor, lw=lw, zorder=zorder+1)

    # --- Whiskers: vertical (radial) lines at the center angle
    ax.plot([theta_center, theta_center], [r_min, q1], color=edgecolor, lw=lw, zorder=zorder+1)
    ax.plot([theta_center, theta_center], [q3, r_max], color=edgecolor, lw=lw, zorder=zorder+1)

    # --- Caps at whisker ends (short angular segments around theta_center)
    cap_half = (cap_frac * width) / 2
    ax.plot([theta_center - cap_half, theta_center + cap_half], [r_min, r_min], color=edgecolor, lw=lw, zorder=zorder+1)
    ax.plot([theta_center - cap_half, theta_center + cap_half], [r_max, r_max], color=edgecolor, lw=lw, zorder=zorder+1)


#%%

segments_green = [
    {"theta0": 0,   "width": np.pi/3,  "r": log_green_top[0], "bottom":0,  "color": "olivedrab", "label": "climate change"},
    {"theta0": np.pi/3,  "width": np.pi/3,  "r": log_green_top[1], "bottom":0,  "color": "olivedrab", "label": "freshwater ecotoxicity"},
    {"theta0": 2*np.pi/3, "width": np.pi/3,  "r": log_green_top[2], "bottom":0,  "color": "olivedrab", "label": "terrestrial acidification"},
    {"theta0": 3*np.pi/3, "width": np.pi/3,  "r": log_green_top[3], "bottom":0,  "color": "olivedrab", "label": "land use"},
    {"theta0": 4*np.pi/3, "width": np.pi/3,  "r": log_green_top[4], "bottom":0,  "color": "olivedrab", "label": "human toxicity, non-cancer"},
    {"theta0": 5*np.pi/3, "width": np.pi/3,  "r": log_green_top[5], "bottom":0,  "color": "olivedrab", "label": "particulate matter"},
]

segments_hashed_green = [
    {"theta0": 0,   "width": np.pi/3,  "r": log_hashed_green_top[0]-log_hashed_green_bottom[0], "bottom":log_hashed_green_bottom[0],  "color": "olivedrab", "label": "climate change"},
    {"theta0": np.pi/3,  "width": np.pi/3,  "r": log_hashed_green_top[1]-log_hashed_green_bottom[1], "bottom":log_hashed_green_bottom[1],  "color": "olivedrab", "label": "freshwater ecotoxicity"},
    {"theta0": 2*np.pi/3, "width": np.pi/3,  "r": log_hashed_green_top[2]-log_hashed_green_bottom[2], "bottom":log_hashed_green_bottom[2],  "color": "olivedrab", "label": "terrestrial acidification"},
    {"theta0": 3*np.pi/3, "width": np.pi/3,  "r": log_hashed_green_top[3]-log_hashed_green_bottom[3], "bottom":log_hashed_green_bottom[3],  "color": "olivedrab", "label": "land use"},
    {"theta0": 4*np.pi/3, "width": np.pi/3,  "r": log_hashed_green_top[4]-log_hashed_green_bottom[4], "bottom":log_hashed_green_bottom[4],  "color": "olivedrab", "label": "human toxicity, non-cancer"},
    {"theta0": 5*np.pi/3, "width": np.pi/3,  "r": log_hashed_green_top[5]-log_hashed_green_bottom[5], "bottom":log_hashed_green_bottom[5],  "color": "olivedrab", "label": "particulate matter"},
]


segments_red = [
    {"theta0": 0,   "width": np.pi/3,  "r":log_red_top[0]-log_red_bottom[0] , "bottom":log_red_bottom[0],  "color": "tomato", "label": "climate change"},
    {"theta0": np.pi/3,  "width": np.pi/3,  "r": log_red_top[1]-log_red_bottom[1], "bottom":log_red_bottom[1],  "color": "tomato", "label": "freshwater ecotoxicity"},
    {"theta0": 2*np.pi/3, "width": np.pi/3,  "r": log_red_top[2]-log_red_bottom[2], "bottom":log_red_bottom[2],  "color": "tomato", "label": "terrestrial acidification"},
    {"theta0": 3*np.pi/3, "width": np.pi/3,  "r": log_red_top[3]-log_red_bottom[3], "bottom":log_red_bottom[3],  "color": "tomato", "label": "land use"},
    {"theta0": 4*np.pi/3, "width": np.pi/3,  "r": log_red_top[4]-log_red_bottom[4], "bottom":log_red_bottom[4],  "color": "tomato", "label": "human toxicity, non-cancer"},
    {"theta0": 5*np.pi/3, "width": np.pi/3,  "r": log_red_top[5]-log_red_bottom[5], "bottom":log_red_bottom[5],  "color": "tomato", "label": "particulate matter"},
]

segments_hashed_red = [
    {"theta0": 0,   "width": np.pi/3,  "r":log_hashed_red_top[0]-log_hashed_red_bottom[0] , "bottom":log_hashed_red_bottom[0],  "color": "tomato", "label": "climate change"},
    {"theta0": np.pi/3,  "width": np.pi/3,  "r": log_hashed_red_top[1]-log_hashed_red_bottom[1], "bottom":log_hashed_red_bottom[1],  "color": "tomato", "label": "freshwater ecotoxicity"},
    {"theta0": 2*np.pi/3, "width": np.pi/3,  "r": log_hashed_red_top[2]-log_hashed_red_bottom[2], "bottom":log_hashed_red_bottom[2],  "color": "tomato", "label": "terrestrial acidification"},
    {"theta0": 3*np.pi/3, "width": np.pi/3,  "r": log_hashed_red_top[3]-log_hashed_red_bottom[3], "bottom":log_hashed_red_bottom[3],  "color": "tomato", "label": "land use"},
    {"theta0": 4*np.pi/3, "width": np.pi/3,  "r": log_hashed_red_top[4]-log_hashed_red_bottom[4], "bottom":log_hashed_red_bottom[4],  "color": "tomato", "label": "human toxicity, non-cancer"},
    {"theta0": 5*np.pi/3, "width": np.pi/3,  "r": log_hashed_red_top[5]-log_hashed_red_bottom[5], "bottom":log_hashed_red_bottom[5],  "color": "tomato", "label": "particulate matter"},
]

# adding crosses for 0.01th percentile
min_angles = [np.pi/6, 3*np.pi/6, 5*np.pi/6, 7*np.pi/6, 9*np.pi/6, 11*np.pi/6]

# --- Plot ---
plt.rcParams.update({
    "figure.dpi": 150,
    "axes.titlesize": 14,
    "axes.labelsize": 11
})

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='polar')

# Put 0° at the top and increase clockwise
ax.set_theta_zero_location('N')
ax.set_theta_direction(1)

ax.set_rticks([])       # Radial ticks
ax.set_rlabel_position(90)                # Move radial labels to 90° to avoid overlap

# Draw each segment - green
for seg in segments_green:
    # Polar bar expects the CENTER angle, not the start angle.
    theta_center = seg["theta0"] + seg["width"] / 2.0
    ax.bar(
        x=theta_center,
        height=seg["r"],
        width=seg["width"],
        bottom=seg["bottom"],                
        color=seg["color"],
        edgecolor='white',
        linewidth=1.0,
        alpha=0.95,
        align='center'
    )

# Draw each segment - red
for seg in segments_red:
    # Polar bar expects the CENTER angle, not the start angle.
    theta_center = seg["theta0"] + seg["width"] / 2.0
    ax.bar(
        x=theta_center,
        height=seg["r"],
        width=seg["width"],
        bottom=seg["bottom"],                
        color=seg["color"],
        edgecolor='white',
        linewidth=1.0,
        alpha=0.95,
        align='center'
    )
    
# Draw each segment - hatched green
for seg in segments_hashed_green:
    # Polar bar expects the CENTER angle, not the start angle.
    theta_center = seg["theta0"] + seg["width"] / 2.0
    ax.bar(
        x=theta_center,
        height=seg["r"],
        width=seg["width"],
        bottom=seg["bottom"],                
        color=seg["color"],
        hatch='///',
        edgecolor='gold',
        linewidth=0.4,
        alpha=0.85,
        align='center'
    )    

# Draw each segment - hatched red
for seg in segments_hashed_red:
    # Polar bar expects the CENTER angle, not the start angle.
    theta_center = seg["theta0"] + seg["width"] / 2.0
    ax.bar(
        x=theta_center,
        height=seg["r"],
        width=seg["width"],
        bottom=seg["bottom"],                
        color=seg["color"],
        hatch='///',
        edgecolor='gold',
        linewidth=0.4,
        alpha=0.85,
        align='center'
    )   
    
# plotting crosses for low percentiles
#ax.scatter(min_angles, log_perc_1, marker='x', s=15, c='black')
ax.scatter(min_angles, log_perc_0_1, marker='x', s=15, c='black')
#ax.scatter(min_angles, log_perc_0_01, marker='x', s=15, c='black')


#%%  adding boxplots to the polar axes

# Example five-number summaries for 4 categories
# (r_min, Q1, median, Q3, r_max), with rmin = 5th perc
stats = {
    "cc": (np.log10(1+50*perc_5[0]), np.log10(1+50*perc_25[0]), np.log10(1+50*median[0]), np.log10(1+50*perc_75[0]), np.log10(1+50*perc_95[0])),
    "fw ecotox": (np.log10(1+50*perc_5[1]), np.log10(1+50*perc_25[1]), np.log10(1+50*median[1]), np.log10(1+50*perc_75[1]), np.log10(1+50*perc_95[1])),
    "terrest acidif": (np.log10(1+50*perc_5[2]), np.log10(1+50*perc_25[2]), np.log10(1+50*median[2]), np.log10(1+50*perc_75[2]), np.log10(1+50*perc_95[2])),
    "land use": (np.log10(1+50*perc_5[3]), np.log10(1+50*perc_25[3]), np.log10(1+50*median[3]), np.log10(1+50*perc_75[3]), np.log10(1+50*perc_95[3])),
    "human tox nc": (np.log10(1+50*perc_5[4]), np.log10(1+50*perc_25[4]), np.log10(1+50*median[4]), np.log10(1+50*perc_75[4]), np.log10(1+50*perc_95[4])),
    "particulate matter": (np.log10(1+50*perc_5[5]), np.log10(1+50*perc_25[5]), np.log10(1+50*median[5]), np.log10(1+50*perc_75[5]), np.log10(1+50*perc_95[5])),
}

# Place them evenly around the circle
labels = list(stats.keys())
n = len(labels)
thetas = np.linspace(np.pi/6, 2*np.pi+np.pi/6, n, endpoint=False)
width = np.deg2rad(10)  # 10° box width

for i, (label, (rmin, q1, med, q3, rmax)) in enumerate(stats.items()):
    add_polar_boxplot(ax,
                      theta_center=thetas[i], width=width,
                      r_min=rmin, q1=q1, median=med, q3=q3, r_max=rmax,
                      facecolor='none', edgecolor="black",
                      alpha=0.25, lw=1, cap_frac=0.3, zorder=3)

#%% labels

# adapted to each bar
ax.text(np.pi/6, 4, 'climate\nchange', ha='center', va='bottom', fontsize=10)
ax.text(3*np.pi/6, 6, 'freshwater\necotoxicity\n\n', ha='center', va='bottom', fontsize=10)
ax.text(5*np.pi/6, 3.2, 'terrestrial\nacidification', ha='center', va='bottom', fontsize=10)
ax.text(7*np.pi/6, 3, 'land\n use', ha='center', va='bottom', fontsize=10)
ax.text(9*np.pi/6, 4.5, 'human\ntoxicity\nnon-cancer', ha='center', va='center', fontsize=10)
ax.text(11*np.pi/6, 3.8, 'particulate\nmatter', ha='center', va='bottom', fontsize=10)

# adding scale
ax.set_rticks([np.log10(1+50*1), np.log10(1+50*10), np.log10(1+50*100), np.log10(1+50*1000)])
ax.set_yticklabels(['1', '10', '100', '1000'])
ax.yaxis.set_tick_params(labelsize=8, colors='black')
ax.set_rlabel_position(180)
#ax.set_rmax(5)
ax.plot([np.pi,np.pi], [0, np.log10(1+50*1000)], color='lightgrey', lw=0.5)
circle_angles=np.linspace(0, 2*np.pi, 500)
ax.plot(circle_angles, np.full_like(circle_angles, np.log10(1+50*1000)), color='lightgrey', lw=0.5, alpha=0.5, zorder=0)
ax.plot(circle_angles, np.full_like(circle_angles, np.log10(1+50*100)), color='lightgrey', lw=0.5, alpha=0.5, zorder=0)
ax.plot(circle_angles, np.full_like(circle_angles, np.log10(1+50*10)), color='lightgrey', lw=0.5, alpha=0.5, zorder=0)
ax.plot(circle_angles, np.full_like(circle_angles, np.log10(1+50*1)), color='lightgrey', lw=0.5, alpha=0.5)


#ax.set_title("AESA", pad=20)
ax.set_thetagrids([0,60,120, 180, 240, 300], ['','','','','',''])  # sets both ticks and grid lines
ax.grid(False)
ax.spines['polar'].set_visible(False)
plt.tight_layout()
plt.show()
