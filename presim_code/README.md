# REACTIVE VACCINATION (extended time)

# Demographic and vaccination roll-out set up

## 1. Demographics

We have two demographies: "younger" and "older" populations. They are based on the averages of the population demographies of various nations in the World Health Organization (WHO) Western Pacific Region (WPR).

Australia, Brunei, Cambodia, China, Cook Islands, Fiji, Japan, Kiribati, Laos, Malaysia, Marshall Islands, Micronesia, Mongolia, Nauru, New Zealand, Niue, Palau, Papua New Guinea, Philippines, Samoa, Singapore, Solomon Islands, South Korea, Tonga, Tuvalu, Vanuatu, Vietnam. 

See the list here https://www.who.int/westernpacific/about/where-we-work

The population data obtained from https://population.un.org/wpp/DataQuery/ 

This data is **population/PopulationAgeSex-20220412011050.xlsx** (note that not all WHO named countries could be found)

We define OADR (old-age dependency ratio) = (total 65+) / (total 20-64) *100

"Older populations" are those with OADR> 15, while "younger populations" have OADR < 12. Countries with OADR in-between are not included.

The data file includes our added columns that calculated the OADR (column AE).

We then run **population/population_distributions_abm_2021.py**

This creates population output files of the *averaged proportion* of the population in the age bands used for the agent-based model (abm), plus makes plots of the distributions for the paper.

## 2. Contact Matrices

The contact matrices are derived from data numerous sources and collected at http://www.socialcontactdata.org/socrates/ 

The file **contact_matrices/contact_matrices_SOCRATES_notes.txt** contain the parameters used to download the data from SOCRATES. 

Data from the UN (https://population.un.org/wpp/DataQuery/)is used to check which countries are "older" or "younger".

**contract_matrices_SOCRATES.py** then calculates the averaged contact matrices for "older" and "younger" populations.

Note that the countries used here are not the same as the countries used in the population distribution, due to the limited data available on SOCRATES.

(PREM matrices were not used at time of this work due to a known error in them.)

**contact_matrces_SOCRATES.py** plots the contact matrices used in the simulations for the paper.

## 3. Parameter files

First, we run **generate_parameter_files_.....py** to generate the base parameter files:

Parameters that can be changed (hard-coded) include:
- total population size
- "younger" or "older" population type
- vaccination coverage (first year)
- oldest group coverage
- booster fraction (first half of the second year)
- dose delivery priorities (first year, first boosters, second boosters)
- output folder
- other things...

Also, make sure to move/have a copy of dim_age_band.csv inside the created folders with the parameter files

## 4. Vaccination rollout

The populations, vaccination allocation and rollout are calculated using the functions in **create_and_generate_initial_conditions.py**, using the parameters generated in the previous sections.

The various plots are calculated using the functions in **create_and_generate_initial_conditions_plotting.py** (including the plots for the paper).

We call these functions in the appropriate order in **run_create_and_generate_initial_conditions.py** 

## Next

After running all these files, the main simulation can begin!
