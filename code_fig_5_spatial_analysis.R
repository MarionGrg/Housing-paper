#### Install packages ####
# Define the list of packages required for the script
required_packages <- c("tidyverse", "mapDK", "ggtext", "patchwork")
# 1. Install 'pak' if it is not already installed
if (!require("pak")) install.packages("pak")

# 2. Check which packages are missing from the computer
installed_pkgs <- installed.packages()[, "Package"]
missing_pkgs <- required_packages[!required_packages %in% installed_pkgs]

# 3. Install only the missing packages using pak
if (length(missing_pkgs) > 0) {
    message("Installing missing packages: ", paste(missing_pkgs, collapse = ", "))
    pak::pkg_install(missing_pkgs)
} else {
    message("All required packages are already installed.")
}


#### Import required packages ####
library(tidyverse)
library(mapDK)
library(ggtext)
library(patchwork)

# Load the map data
mapDK()

# municipality - plots Denmark's 98 municipalities
# region - plots Denmark's 5 regions
# rural - plots Denmark's 11 rural areas
# zip - plots Denmark's 598 zip code areas
# polling - plots Denmark's 1385 polling places (as of 2015)
# parish - plots Denmark's 1931 parishes

map_municipality_data <- read.csv("map_municipality_data.csv") %>% as_tibble()
map_municipality_data

# Kommune code data
code_kommune <- readxl::read_xlsx("code_kommune.xlsx")
code_kommune %>% 
    mutate(Kommune = gsub(pattern = "Nordfyn", replacement = "Nordfyns", x = Kommune, ignore.case = T),
           Kommune = gsub(pattern = "Vesthimmerland", replacement = "Vesthimmerlands", x = Kommune, ignore.case = T)) -> code_kommune

code_kommune %>% arrange(Kommune) %>% print(n = Inf)
map_municipality_data %>% 
    select(-X) %>% 
    left_join(code_kommune, by = c("KOM" = "Kode")) %>% 
    rename_with(~ gsub("..", "_", .x, fixed = T)) %>% 
    rename_with(~ gsub(".", "_", .x, fixed = T)) %>% 
    rename_all(tolower) -> map_municipality_data_clean

map_municipality_data_clean %>% glimpse()
kummuner_kort <- mapDK::municipality %>% as_tibble()

# Mapping data
columns_data <- readxl::read_xlsx("columns_to_plot.xlsx")
columns_data <- columns_data %>% rename(column_name = `Column name`)

#### Figure 5A ####
# Energy consumption
min_val_energy_consumption <- min(map_municipality_data_clean$energy_consumption_from_regressions_kwh_m2_)
max_val_energy_consumption <- max(map_municipality_data_clean$energy_consumption_from_regressions_kwh_m2_)
mapDK(values = "energy_consumption_from_regressions_kwh_m2_", id = "kommune", data = map_municipality_data_clean) +
    geom_polygon(data = kummuner_kort, 
                 aes(x = long, y = lat, group = group), 
                 color = scales::alpha("black", 0.3),
                 linewidth = 0.2,
                 fill = NA) +
    labs(
        fill = paste0(
            columns_data$Indicator[columns_data$column_name == "Energy Consumption from Regressions (kWh/m2)"],
            "<br>(",
            gsub(
                pattern = "m2", 
                replacement = "m<sup>2</sup>", 
                columns_data$Unit[columns_data$column_name == "Energy Consumption from Regressions (kWh/m2)"]
            ),
            ")")
    ) +
    scale_fill_gradientn(
        colors = c("blue", "cornsilk", "red"),
        values = scales::rescale(c(0, 0.5, 1)),
        limits = c(min_val_energy_consumption, max_val_energy_consumption),
        breaks = scales::pretty_breaks(n = 6)
    ) + 
    guides(
        fill = guide_colourbar(
            theme = theme(
                legend.key.height = unit(7, "cm")
            ))
    ) +
    theme(legend.title = element_markdown(size = 20, face = "bold"),
          legend.text = element_text(size = 20),
          legend.position = "inside",
          legend.position.inside = c(0.8, 0.7)) -> Fig5A_energy_consumption

#### Figure 5B ####
# Living area per capita
min_val_living_area_cap <- min(map_municipality_data_clean$median_living_area_per_capita)
max_val_living_area_cap <- max(map_municipality_data_clean$median_living_area_per_capita)
mapDK(values = "median_living_area_per_capita", id = "kommune", data = map_municipality_data_clean) +
    geom_polygon(data = kummuner_kort, 
                 aes(x = long, y = lat, group = group), 
                 color = scales::alpha("black", 0.3),
                 linewidth = 0.2,
                 fill = NA) +
    labs(
        fill = paste0(
            columns_data$Indicator[columns_data$column_name == "median_Living_Area_per_Capita"],
            "<br>(",
            gsub(
                pattern = "m2", 
                replacement = "m<sup>2</sup>", 
                columns_data$Unit[columns_data$column_name == "median_Living_Area_per_Capita"]
            ),
            ")")
    ) +
    scale_fill_gradientn(
        colors = c("blue", "cornsilk", "red"),
        values = scales::rescale(c(0, 0.5, 1)),
        limits = c(min_val_living_area_cap, max_val_living_area_cap),
        breaks = scales::pretty_breaks(n = 5)
    )  + 
    guides(
        fill = guide_colourbar(
            theme = theme(
                legend.key.height = unit(7, "cm")
            ))
    ) +
    theme(legend.title = element_markdown(size = 20, face = "bold"),
          legend.text = element_text(size = 20),
          legend.position = "inside",
          legend.position.inside = c(0.8, 0.7)) -> Fig5B_living_area


#### Figure 5C ####
# Climate change, short term combined cap
min_val_cc_st_comb_cap <- min(map_municipality_data_clean$climate_change_short_term_combined_cap)
max_val_cc_st_comb_cap <- max(map_municipality_data_clean$climate_change_short_term_combined_cap)
mapDK(values = "climate_change_short_term_combined_cap", id = "kommune", data = map_municipality_data_clean) +
    geom_polygon(data = kummuner_kort, 
                 aes(x = long, y = lat, group = group), 
                 color = scales::alpha("black", 0.3),
                 linewidth = 0.2,
                 fill = NA) +
    labs(
        fill = paste0(
            columns_data$Indicator[columns_data$column_name == "Climate change, short term-combined-cap"],
            "<br>(",
            gsub(
                pattern = "m2", 
                replacement = "m<sup>2</sup>", 
                columns_data$Unit[columns_data$column_name == "Climate change, short term-combined-cap"]
            ),
            ")")
    ) +
    scale_fill_gradientn(
        colors = c("blue", "cornsilk", "red"),
        values = scales::rescale(c(0, 0.5, 1)),
        limits = c(min_val_cc_st_comb_cap, max_val_cc_st_comb_cap),
        trans = "log10",
        breaks = scales::pretty_breaks(n = 5)
    ) +
    guides(
        fill = guide_colourbar(
            theme = theme(
                legend.key.height = unit(7, "cm")
            ))
    ) +
    theme(legend.title = element_markdown(size = 20, face = "bold"),
          legend.text = element_text(size = 20),
          legend.position = "inside",
          legend.position.inside = c(0.8, 0.7)) -> Fig5C_CC_st_combined_cap


#### Figure 5D ####
# Particulate matter formation combined cap
min_val_pm_form_comb_cap <- min(map_municipality_data_clean$particulate_matter_formation_combined_cap)
max_val_pm_form_comb_cap <- max(map_municipality_data_clean$particulate_matter_formation_combined_cap)
mapDK(values = "particulate_matter_formation_combined_cap", id = "kommune", data = map_municipality_data_clean) +
    geom_polygon(data = kummuner_kort, 
                 aes(x = long, y = lat, group = group), 
                 color = scales::alpha("black", 0.3),
                 linewidth = 0.2,
                 fill = NA) +
    labs(
        fill = paste0(
            columns_data$Indicator[columns_data$column_name == "Particulate matter formation-combined-cap"],
            "<br>(",
            gsub(
                pattern = "m2", 
                replacement = "m<sup>2</sup>", 
                columns_data$Unit[columns_data$column_name == "Particulate matter formation-combined-cap"]
            ),
            ")")
    ) +
    scale_fill_gradientn(
        colors = c("blue", "cornsilk", "red"),
        values = scales::rescale(c(0, 0.5, 1)),
        limits = c(min_val_pm_form_comb_cap, max_val_pm_form_comb_cap),
        trans = "log10",
        breaks = scales::pretty_breaks(n = 6)
    ) +
    guides(
        fill = guide_colourbar(
            theme = theme(
                legend.key.height = unit(7, "cm")
            ))
    ) +
    theme(legend.title = element_markdown(size = 20, face = "bold"),
          legend.text = element_text(size = 20),
          legend.position = "inside",
          legend.position.inside = c(0.8, 0.7)) -> Fig5D_PM_form_combined_cap



ggsave(plot = Fig5A_energy_consumption, filename = "Fig5A.pdf", width = 15, height = 15)
ggsave(plot = Fig5B_living_area, filename = "Fig5B.pdf", width = 15, height = 15)
ggsave(plot = Fig5C_CC_st_combined_cap, filename = "Fig5C.pdf", width = 15, height = 15)
ggsave(plot = Fig5D_PM_form_combined_cap, filename = "Fig5D.pdf", width = 15, height = 15)

