# Boosting and hybrid immunity: theoretical populations 

This repository contains the code for the agent-based transmission simulation. It simulates multiple covid waves with multiple rounds of vaccination. 

Note that https://github.com/nlohmann/json is necessary for function.

## 1. Run the "presimulation" files 

See the [**/presim_code**](/presim_code/) folder which generates various parameter files and inputs such as demographics, contact matrices, and vaccination rollout.

The contact matrices need to be copied into this folder (note, they are already here).

## 2. Main results

The main source files are [**main_BA1s_BA45s_cont_intros.cpp**](/main_ABM/main_BA1s_BA45s_cont_intros.cpp), [**main_BA1s_BA45s_cont_intros_many_boosters.cpp**](/main_ABM/main_BA1s_BA45s_cont_intros_many_boosters.cpp), and  [**main_BA1s_BA45s_bivalent_cont_intros.cpp**](/main_ABM/main_BA1s_BA45s_bivalent_cont_intros.cpp).

Run the following to compile the C++ executables: 

`make`

This will produce three executables:

1. `Run_BA1s_BA45s_cont_intros` which is for the majority of simulations
2. `Run_BA1s_BA45s_cont_intros_many_boosters` for the six-monthly/half-yearly boosting simulations
3. `Run_BA1s_BA45s_bivalent_cont_intros` for the use of bivalent doses after 1.5 years. 


### Simulations

To run the simulations, some more set-up files need to be created, starting with running the following:

- [**generate_json_files_annual_boosting_1.py**](/main_ABM/generate_json_files_annual_boosting_1.py) (for the high-vaccination coverage simulations)
- [**generate_json_files_annual_boosting_1_younger.py**](/main_ABM/generate_json_files_annual_boosting_1_younger.py) (for the low-coverage younger population simulations)
- [**generate_json_files_annual_boosting_2.py**](/main_ABM/generate_json_files_annual_boosting_2.py) (for the half-yearly boosting simulations)
- [**generate_json_files_annual_boosting_age_scenarios.py**](/main_ABM/generate_json_files_annual_boosting_age_scenarios.py) (for the age cutoff simulations)

e.g., with commands

`python generate_json_files_annual_boosting_1.py`

`python generate_json_files_annual_boosting_1_younger.py`

and so forth.

The simulation parameter files will be stored in a folder called **main_ABM/simulation_params/** and the overall output folder is **outputs/**

Now, the simulations can be run (from within this folder)

To make it easier, see [run_annual_boosting_1.sh](/main_ABM/run_annual_boosting_1.sh) for an example script for the high-vaccination-coverage simulations. Note that even with only `NUM_SIMS=2`, the simulations take a while. The scripts in the [/example_cluster_submission_files](/main_ABM/example_cluster_submission_files) folder provide an outline as to how to submit 1000 runs to a computational cluster and produce plots (run files 1-4).

Similarly
- [run_annual_boosting_1_younger.sh](/main_ABM/run_annual_boosting_1_younger.sh) for low and medium vaccination-coverage simulations in the younger population
- [run_annual_boosting_2.sh](/main_ABM/run_annual_boosting_2.sh) for additional half-yearly boosting 
- [run_annual_boosting_age_scenarios.sh](/main_ABM/run_annual_boosting_age_scenarios.sh) for lowering the eligibility of boosters (from 65+ down to 5+)
- [run_bivalent_low_coverage_boosting.sh](/main_ABM/run_bivalent_low_coverage_boosting.s.sh) for bivalent doses in the younger population, low and medium vaccination-coverage setting.



### Plotting

The plotting scripts are found in the [data_analysis_code/plot_figures/](/main_ABM/data_analysis_code/plot_figures/) folder.

## Notes

Note that "annual_boosting_1" refers to boosting within high-coverage populations (both younger and older). "annual_boosting_1_younger" refers to boosting in the lower-coverage younger populations. All of these have a single boosting program some time between 1.5-3 years.

"annual_boosting_2" refers to 6-monthly boosting in high-coverage populations, with a total of three rollouts during 1.5-3 year time period.