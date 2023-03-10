# Boosting and hybrid immunity: theoretical populations 

This repository was created for the WHO work ("prosposal 1") looking at vaccination and boosting. This repository contains the code for the main simulation itself. It simulates multiple covid waves with multiple rounds of vaccination. 


Note that some files are first generated from the code here: https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO/presim_code

Note that https://github.com/nlohmann/json is necessary for function.

## 1. Run the "presimulation" files 

See https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO/presim_code which generates various parameter files and inputs such as demographics, contact matrices, and vaccination rollout.

Copy the contact matrices into this folder (or make a note of where they are and update in the **generate_json_files_.....py** files before running them)

## 2. Main results

Run the following to compile the C++ executables: 

`make`

### Simulations

The main source files are **main_BA1s_BA45s_cont_intros.cpp** and **main_BA1s_BA45s_cont_intros_many_boosters.cpp**

1. Run the python file **generate_json_files_BA1s_BA45s_....py** (there are multiple ones...), updating the locations of output directories as appropriate (which are hardcoded into the file). This creates two folders with numerous different input files.
2. **submit_all_BA1s_BA45s_....sh**: This generates the simulations and also produces the clinical outcomes for each individual simulation. Note that this requires the clinical pathways model as well, and directories need to be updated in **submit_function_BA1s_BA45s.script**
3. **submit_all_BA1s_BA45s_matlab_R_....sh**: This must be run after all the simulations are done. It groups all of the individual simulation outputs together and all the clinical pathway outcomes together. Note that `numsims` may need to be updated as appropriate. Directories need to be updated in **submit_function_BA1s_BA45s_matlab_R_....script**.



### Plotting

Then run the plotting scripts... 

1. **plot_infections_annual_boosting...py**

### Submission scripts

See [/example_cluster_submission_files](https://github.com/spectrum-spark/covid_singlestrain_scenarios/tree/singlestrain-WHO/main_ABM/example_cluster_submission_files) for examples of how to run all the different files together. Note that the clinical pathways is run in sequence in the example submission scripts.

After changing appropriate parameters and file locations, the order to run is:

1. **submit_annual_boosting_1_all.sh** (which calls **submit_annual_boosting_1_function.script**): This runs all the individual simulations and also their individual clinical pathways.
2. **submit_annual_boosting_1_matlab_R_all.sh** (which calls **submit_annual_boosting_1_matlab_R_function.script**): this gathers all the individual outputs and pulls them into aggregated files.
3. **submit_annual_boosting_1_plotting.script**: this plots figures
4. (optional) **submit_clinical_gathering.script**: this outputs csv files with clinical pathways data.
