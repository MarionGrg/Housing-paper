# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 15:53:28 2026

@author: mageo
"""

# clean the workspace
from IPython import get_ipython
get_ipython().magic('reset -sf')
# close all figures
import matplotlib.pyplot as plt
plt.close('all')
import pandas as pd
from matplotlib.lines import Line2D

#%% for plotting
plt.rc('font', size = 12)
plt.rc('axes', titlesize = 14)
plt.rc('axes', labelsize = 14)
plt.rc('xtick', labelsize = 12)
plt.rc('ytick', labelsize = 12)
plt.rc('legend', fontsize = 12)
plt.rc('figure', titlesize = 12)

#%% relative contribution to impact variability

# data import
variability_percentage = pd.read_csv("variability_percentages.csv", sep=',')
variability_percentage.index=variability_percentage['Unnamed: 0'].to_list()
variability_percentage = variability_percentage.drop('Unnamed: 0', axis=1)

# graph
colors_hex = ['#C67D3A', '#BC0046', '#007F85', '#FF8802']   
variability_percentage.plot(kind='barh', stacked=True, color=colors_hex)
plt.grid(axis='x', alpha=0.3) 
plt.xlim(xmin=0, xmax=100)
plt.xlabel("Relative importance of the key components on the impact variability [%]")
legend_txt = ['heating consumption', 'heating impact intensity', 'embodied impact', 'area per capita']
plt.legend(legend_txt, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
plt.tight_layout()

#%% contribution analysis - heating / embodied impacts

# data import
impact_categories_midpoint = variability_percentage.index
contribution_values = pd.read_csv("mean_contribution_values.csv", sep=',')
embodied_mean = contribution_values['mean_embodied']
heating_mean = contribution_values['mean_heating']

# graph
plt.figure(figsize=(9,6.5), layout='constrained')
plt.bar(impact_categories_midpoint, embodied_mean, width=0.7, color= 'cadetblue', alpha=0.65, bottom=[0]*len(impact_categories_midpoint), label='embodied impact')
plt.bar(impact_categories_midpoint, heating_mean, width=0.7, color= 'firebrick', alpha=0.65, bottom=embodied_mean, label='heating impact')
plt.legend()
plt.ylim(ymin=0, ymax=100)
plt.ylabel('Percentage of the total impact [%]')
plt.xticks(impact_categories_midpoint, rotation=45, ha='right')

#%% scatter plots

# data import
# env_impact_clustered_shuffled need to contain: 'Living_Area* (bdg area), impact_categories_midpoint[i]+'-combined-m2'
env_impact_clustered_shuffled_1 = pd.read_csv("env_impact_clustered_shuffled_1.csv", sep=',')
env_impact_clustered_shuffled_2 = pd.read_csv("env_impact_clustered_shuffled_2.csv", sep=',')
env_impact_clustered_shuffled_3 = pd.read_csv("env_impact_clustered_shuffled_3.csv", sep=',')
env_impact_clustered_shuffled = pd.concat([env_impact_clustered_shuffled_1, env_impact_clustered_shuffled_2, env_impact_clustered_shuffled_3], ignore_index=True)

# for the 6 categories plotted
units_midpoint = ['kg CO2 eq', 'CTUe', 'kg SO2 eq', 'm2 ar ld.yr', 'CTUh', 'kg PM2.5 eq']
units_midpoint = pd.DataFrame(units_midpoint)
units_midpoint.index = [impact_categories_midpoint[i] for i in [1,4,16,9,7,14]]

# to plot
heating_types = ['CoalCoke', 'HeatPump', 'FuelGasOil', 'NaturalGas', 'DistrictHeat', 'Electricity', 'WoodPellets', 'Biogas']
list_markers = ['D', '|', 's', 'v', 'x', '_', '+', 'o']
heating_types_visual = ['coal & coke', 'heat pump', 'fuel, gas & oil', 'natural gas', 'district heating', 'electricity', 'wood pellets', 'biogas']
list_colors = ['darkgreen', 'forestgreen', 'limegreen', 'yellowgreen', 'gold', 'orange', 'orangered', 'firebrick', 'rebeccapurple']
list_colors.reverse()
list_labels = ['A2020', 'A2015', 'A2010', 'B', 'C', 'D', 'E', 'F', 'G']
list_labels.reverse()

#%% graphs - impact per m2 as a function of building living area

# ICs to plot: i = 1, 4, 16, 9, 7, 14
for i in [1,4,16,9,7,14]:
    plt.figure(figsize=(9,6.5), layout='constrained')
    for _, row in env_impact_clustered_shuffled.iterrows():
        plt.scatter(
            row['Living_Area'],
            row[impact_categories_midpoint[i]+'-combined-m2'],
            marker=row['marker_graph'],
            facecolors=row['face_color_marker'],
            edgecolors=row['edge_color_graph']
            )
    
    # legend
    markers_legend = [Line2D([0], [0], marker='s', linestyle='', markeredgecolor=c, markerfacecolor=c) for c in list_colors]
    for j in range(len(heating_types)):
        markers_legend.append(Line2D([0], [0], marker = list_markers[j], linestyle='', markeredgecolor='black', markerfacecolor='none'))
    text_legend = list_labels + heating_types_visual
    plt.legend(markers_legend, text_legend, loc=1, ncol=2)
    
    plt.xlim(xmin=0, xmax=800)
    plt.ylim(ymin=0)
    plt.xlabel('Building living area [m2]')
    plt.ylabel(impact_categories_midpoint[i] + ' [' + units_midpoint[0][impact_categories_midpoint[i]] + '/m2/yr]')
    plt.show()


#%% graphs - impact per capita as a function of living area per capita

# loop over the impact categories
for i in [1, 4,16,9,7,14]: #range(len(impact_categories_midpoint)):    
    plt.figure(figsize=(8,5.5), layout='constrained')
    for _, row in env_impact_clustered_shuffled.iterrows():
        plt.scatter(
            row['Living_Area_per_Capita'],
            row[impact_categories_midpoint[i]+'-combined-cap'],
            marker=row['marker_graph'],
            facecolors=row['face_color_marker'],
            edgecolors=row['edge_color_graph']
            )
    
    # legend
    markers_legend = [Line2D([0], [0], marker='s', linestyle='', markeredgecolor=c, markerfacecolor=c) for c in list_colors]
    for j in range(len(heating_types)):
        markers_legend.append(Line2D([0], [0], marker = list_markers[j], linestyle='', markeredgecolor='black', markerfacecolor='none'))
    text_legend = list_labels + heating_types_visual
    plt.legend(markers_legend, text_legend, loc=2, ncol=2)
    
    plt.xlim(xmin=0, xmax=260)
    plt.ylim(ymin=0)
    plt.xlabel('Living area per capita [m2/cap]')
    plt.ylabel(impact_categories_midpoint[i] + ' [' + units_midpoint[0][impact_categories_midpoint[i]] + '/cap/yr]')
    plt.show()
