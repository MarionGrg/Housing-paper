# Code and data for: "The drivers of (un)sustainable housing: A population-scale Danish life cycle assessment"
## Overview
This repository contains the code and sharable data allowing to reproduce the main figures (Fig. 1 to 6) of the paper: "The drivers of (un)sustainable housing: A population-scale Danish life cycle assessment".

The repository includes 2 Python and one R scripts and all corresponding CSV and Excel files.

## System requirements
The scrips rely on the following packages and libraries:

For **Python** (version 3.13.9):
- `ipython`: version 8.30.0
- `matplotlib`: version 3.10.0
- `pandas`: 2.2.3
- `numpy`: version 2.1.3

For **R**:


## Repository contents
- `code_fig_1_to_4.py` : a Python script to reproduce Fig. 1 to 4
- `code_fig_5_spatial_analysis.R` : a R script to reproduce the maps from Fig. 5
- `code_AESA_fig_6.py` : a Python script to reproduce Fig. 6a
- `README.md`: this file
- Data files:
  * `AESA_values_for_graph.xlsx`
  * `code_kommune 1.xlsx`
  * `columns_to_plot.xlsx`
  * `env_impact_clustered_shuffled_1.csv`
  * `env_impact_clustered_shuffled_2.csv`
  * `env_impact_clustered_shuffled_3.csv`
  * `map_municipality_data.csv`
  * `mean_contribution_values.csv`
  * `stat_values_AESA_indiv_3a.xlsx`
  * `variability_percentages.csv`

## Steps to follow to reproduce the figures

### 1. Download the repository
Download the contents of this repository as a ZIP file on your computer. UnZip the file; you obtain a folder with all the necessary files.

### 2. Run the scripts
#### 2.1. Install the packages
If the required Python and R libraries are not already imported on your computer, import them.

For Python, use the following command: `pip install name_of_the_package` in a Python terminal replacing `name_of_the_package` by the 4 Python libraries mentioned above.   

For R, ???

#### 2.2. Run the first Python script
1. In your Python software, open the file `code_fig_1_to_4.py`.

2. Make sure that your working directory is the folder exported from this repository. You can use the following command replacing `path/to/script/directory` with the relevant path.

```
import os 
os.chdir('path/to/script/directory')
```

3. Run the entire script.

4. Check for outputs, either embedded in your Python software on the plot window or opened as separate windows. 

#### 2.3. Run the R script
1. In your R software, open the file `code_fig_5_spatial_analysis.R`.

2. Set your working directory to the folder exported from this repository. You can use the following command in the R console replacing `path/to/script/directory` with the relevant path.

```r
setwd("path/to/script/directory")
```

3. Run the entire script.
   
4. The script will execute and save the four figures as PDF files in your working directory:

- `Fig5A.pdf`
- `Fig5B.pdf`
- `Fig5C.pdf`
- `Fig5D.pdf`

#### 2.4. Run the second Python script
Repeat the step 2.2 for the file `code_AESA_fig_6.py`.






