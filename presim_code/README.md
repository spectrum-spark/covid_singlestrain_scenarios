# POPULATION & VACCINATION ROLL-OUT

# Demographic and vaccination roll-out set up

*Note* that all code has be run already and parameter files etc. have been completely included in this folder.

## 1. Demographics

We have two demographies: "younger" and "older" populations. They are based on the averages of the population demographies of various nations in the World Health Organization (WHO) Western Pacific Region (WPR).

Australia, Brunei, Cambodia, China, Cook Islands, Fiji, Japan, Kiribati, Laos, Malaysia, Marshall Islands, Micronesia, Mongolia, Nauru, New Zealand, Niue, Palau, Papua New Guinea, Philippines, Samoa, Singapore, Solomon Islands, South Korea, Tonga, Tuvalu, Vanuatu, Vietnam. 

See the list here: https://www.who.int/westernpacific/about/where-we-work

The population data obtained from https://population.un.org/wpp/DataQuery/ 

This data is [**population/PopulationAgeSex-20220412011050.xlsx**](/population/PopulationAgeSex-20220412011050.xlsx) (note that not all WHO named countries could be found).

We define OADR (old-age dependency ratio) = (total 65+) / (total 20-64) *100

"Older populations" are those with OADR> 15, while "younger populations" have OADR < 12. Countries with OADR in-between are not included.

The data file includes our added columns that calculated the OADR (column AE).

We then run [**population/population_distributions_abm_2021.py**](/population/population_distributions_abm_2021.py)

This creates population output files of the *averaged proportion* of the population in the age bands used for the agent-based model (abm), plus makes plots of the distributions for the paper.

## 2. Contact Matrices

The contact matrices are derived from data numerous sources and collected at http://www.socialcontactdata.org/socrates/ 

The file [**contact_matrices/contact_matrices_SOCRATES_notes.txt**](/contact_matrices/contact_matrices_SOCRATES_notes.txt) contain the parameters used to download the data from SOCRATES. 

Data from the UN (https://population.un.org/wpp/DataQuery/) was used to check which countries are "older" or "younger".

[**contract_matrices_SOCRATES.py**](/contact_matrices_SOCRATES.py) then calculates the averaged contact matrices for "older" and "younger" populations.

Note that the countries used here are not the same as the countries used in the population distribution, due to the limited data available on SOCRATES.

(PREM matrices were not used at time of this work due to a known error in them.)

[**contact_matrces_SOCRATES.py**](/contact_matrices_plot.py) plots the contact matrices used in the simulations.

## 3. Parameter files

First, we run **generate_parameter_files_.....py** to generate the base parameter files for the scenarios with only one additional booster rollout:
- [**generate_parameter_files_annual_boosting_1.py**](/generate_parameter_files_annual_boosting_1.py)
- [**generate_parameter_files_annual_boosting_1_high_coverage_younger.py**](/generate_parameter_files_annual_boosting_1_high_coverage_younger.py)
- [**generate_parameter_files_annual_boosting_1_younger.py**](/generate_parameter_files_annual_boosting_1_younger.py)
- [**generate_parameter_files_annual_boosting_age_scenarios.py**](/generate_parameter_files_annual_boosting_age_scenarios.py)

Parameters that can be changed (hard-coded) include:
- total population size
- "younger" or "older" population type
- vaccination coverage (year 1)
- oldest group coverage (year 1)
- booster fraction (year 1.0 - 1.5)
- dose delivery priorities (first year, first boosters, second boosters)
- output folder
- etc.

Also, make sure to move/have a copy of [dim_age_band.csv](/dim_age_band.csv) inside the created folders with the parameter files

## 4. Vaccination rollout

The populations, vaccination allocation and rollout are produced by running [**run_create_and_generate_initial_conditions_annual_boosting.py**](/run_create_and_generate_initial_conditions_annual_boosting.py), [**run_create_and_generate_initial_conditions_age_scenarios.py**](/run_create_and_generate_initial_conditions_age_scenarios.py) and [**run_half_yearly_boosting.py**](/run_half_yearly_boosting.py). 

These use the functions in [**create_and_generate_initial_conditions.py**](/create_and_generate_initial_conditions.py), plus the parameters generated in the previous sections.

The various plots are calculated using the functions in [**create_and_generate_initial_conditions_plotting.py**](/create_and_generate_initial_conditions_plotting.py).


## 5. Additional

The total vaccinations administered through different time periods can be calculated using [**output_total_vaccinations_annual_boosting_1.py**](/output_total_vaccinations_annual_boosting_1.py), [**output_total_vaccinations_annual_boosting_1_low_coverage.py**](/output_total_vaccinations_annual_boosting_1_low_coverage.py), and [**output_total_vaccinations_annual_boosting_age_scenarios.py**](output_total_vaccinations_annual_boosting_age_scenarios.py).

## 6. Next

After running all these files, the main simulation can begin!

## Notes

Note that "annual_boosting_1" refers to boosting within high-coverage populations (both younger and older). "annual_boosting_1_younger" refers to boosting in the lower-coverage younger populations. All of these have a single boosting program some time between 1.5-3 years.

"annual_boosting_2" refers to 6-monthly boosting in high-coverage populations, with a total of three rollouts during 1.5-3 year time period.
