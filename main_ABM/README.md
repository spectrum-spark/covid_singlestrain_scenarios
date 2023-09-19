# Boosting and hybrid immunity: theoretical populations 

This repository contains the code for the agent-based transmission simulation. It simulates multiple covid waves with multiple rounds of vaccination. 

Note that https://github.com/nlohmann/json is necessary for function.

## 1. Run the "presimulation" files 

See https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-paper/presim_code which generates various parameter files and inputs such as demographics, contact matrices, and vaccination rollout.

The contact matrices need to be copied into this folder (note, they are already here).

## 2. Main results

The main source files are [**main_BA1s_BA45s_cont_intros.cpp**](/main_BA1s_BA45s_cont_intros.cpp), [**main_BA1s_BA45s_cont_intros_many_boosters.cpp**](/main_BA1s_BA45s_cont_intros_many_boosters.cpp), and  [**main_BA1s_BA45s_bivalent_cont_intros.cpp**](/main_BA1s_BA45s_bivalent_cont_intros.cpp).

Run the following to compile the C++ executables: 

`make`

This will produce three executables:

1. `Run_BA1s_BA45s_cont_intros` which is for the majority of simulations
2. `Run_BA1s_BA45s_cont_intros_many_boosters` for the six-monthly/half-yearly boosting simulations
3. `Run_BA1s_BA45s_bivalent_cont_intros` for the use of bivalent doses after 1.5 years. 


### Simulations

To run the simulations, some more set-up files need to be created, starting with running the following:

- [**generate_json_files_annual_boosting_1.py**](/generate_json_files_annual_boosting_1.py) (for the high-vaccination coverage simulations)
- [**generate_json_files_annual_boosting_1_younger.py**](/generate_json_files_annual_boosting_1_younger.py) (for the low-coverage younger population simulations)
- [**generate_json_files_annual_boosting_2.py**](/generate_json_files_annual_boosting_2.py) (for the half-yearly boosting simulations)
- [**generate_json_files_annual_boosting_age_scenarios.py**](/generate_json_files_annual_boosting_age_scenarios.py) (for the age cutoff simulations)

The simulation parameter files will be stored in the 



2. **submit_...all.sh**: This generates the simulations and also produces the clinical outcomes for each individual simulation. Note that this requires the clinical pathways model as well, and directories need to be updated in **submit_..._function.script**
3. **submit_..._matlab_R_all.sh**: This must be run after all the simulations are done. It groups all of the individual simulation outputs together and all the clinical pathway outcomes together. Note that `numsims` may need to be updated as appropriate. Directories need to be updated in **submit_..._matlab_R_function.script**.



### Plotting

Then run the plotting scripts, found in the data_analysis_code/plot_figures/ folder.

1. **plot_infections_annual_boosting...py**

### Submission scripts

See [/example_cluster_submission_files](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-paper/main_ABM/example_cluster_submission_files) for examples of how to run all the different files together. Note that the clinical pathways is run in sequence in the example submission scripts.

After changing appropriate parameters and file locations, the order to run is:

1. **submit_annual_boosting_1_all.sh** (which calls **submit_annual_boosting_1_function.script**): This runs all the individual simulations and also their individual clinical pathways.
2. **submit_annual_boosting_1_matlab_R_all.sh** (which calls **submit_annual_boosting_1_matlab_R_function.script**): this gathers all the individual outputs and pulls them into aggregated files.
3. **submit_annual_boosting_1_plotting.script**: this plots figures
4. (optional) **submit_clinical_gathering.script**: this outputs csv files with clinical pathways data.
