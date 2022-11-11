# Reactive vaccination and hybrid immunity: theoretical populations 

This repository was created for the WHO work ("prosposal 1") looking at reactive vaccination. This repository contains the code for the main simulation itself. It simulates three covid waves with four rounds of vaccination. 


Note that some files are first generated from the code here: https://bitbucket.org/thaople/covid-abm-presim/src/WHO/. The code for the immunity model can be found here............

## 1. Run the "presimulation" files 

See https://bitbucket.org/thaople/covid-abm-presim/src/WHO/ which generates various parameter files and inputs such as demographics, contact matrices, and vaccination rollout.

Copy the contact matrices into this folder (or make a note of where they are and update in the **generate_json_files_.....py** files before running them)

## 2. Main paper results

Run the following to compile the C++ executables: 

`make`

### Simulations

The main source file is **main_BA1s_BA45s.cpp**.

1. Run the python file **generate_json_files_BA1s_BA45s.py**, updating the locations of output directories as appropriate (which are hardcoded into the file). This creates two folders with numerous different input files.
2. **submit_all_BA1s_BA45s.sh**: This generates the simulations and also produces the clinical outcomes for each individual simulation. Note that this requires the clinical pathways model as well, and directories need to be updated in **submit_function_BA1s_BA45s.script**
3. **submit_all_BA1s_BA45s_matlab_R.sh**: This must be run after all the simulations are done. It groups all of the individual simulation outputs together and all the clinical pathway outcomes together. Note that `numsims` may need to be updated as appropriate. Directories need to be updated in **submit_function_BA1s_BA45s_matlab_R.script**.



### Plotting

Then run the plotting scripts... 

1. **plot_infections_with_no_vax.py**: produces a plot of the number of infections over time for some simulations plus plots with near future attack rate and deaths and ICU admissions given past immunity. Set the correct output locations for `folder`, `presim_parameters_folder`, `novax_folder` and `novax_presim_parameters_folder`
2. **plot_avoided_differences.py**: produces the plots of the avoided difference between infections and deaths. Set the correct output locations for `folder`, `presim_parameters_folder`, `novax_folder` and `novax_presim_parameters_folder`.

