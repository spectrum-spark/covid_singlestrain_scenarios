# Impact of hybrid immunity on future COVID-19 waves: theoretical populations 

## 1. Run the "presimulation" files 

See https://bitbucket.org/thaople/covid-abm-presim/src/master/ which generates various parameter files and inputs such as demographics, contact matrices, and vaccination rollout.

Copy the contact matrices into this folder (or make a note of where they are and update in the **generate_json_files_.....py** files)

## 2. Main paper results

Run the following to compile the C++ executables: 

`make -f makefile.main`

### A. Simulations with BA1/2 first wave and BA1/2 second wave

The main source file is **main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses.cpp**. The simulations for the scenarios with a BA1/2 first and second wave are produced with the following steps:

1. Run the python file **generate_json_files_with_different_TP_values_and_two_exposures_no_ttiq_450-2_ibm_4th_doses.py**, updating the locations of output directories as appropriate (which are hardcoded into the file). This creates two folders with numerous different input files.
2. Run the bash file...
3. Run the clinical pathways scripts...


### B. Simulations with BA1/2 first wave and BA4/5-like second wave

Main source file: **main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses_newstrain.cpp**

Run the python file **generate_json_files_no_ttiq_450-2_ibm_4th_doses_newstrain.py**, updating the locations of output directories as appropriate. 

### Plotting

Then run the plotting scripts... 

1. **plot_infections_with_no_vax.py**: produces plots with near future attack rate and deaths and ICU admissions given past immunity. Set the correct output locations for `folder`, `presim_parameters_folder`, `novax_folder` and `novax_presim_parameters_folder`

2. **plot_avoided_differences.py**

## 3. Supplementary materials

### A. Simulations with BA1/2 first wave and BA1/2 second wave with a worse vaccine

The main source file is **main_continuous_simulation_double_exposure_no_ttiq.cpp**.

Run the following to compile the C++ executable: 

`make -f makefile.worsevaccine`



Run:

1. Run the python file **generate_json_files_with_different_TP_values_and_two_exposures_no_ttiq_450-2.py**, updating the locations of output directories as appropriate. 
2. **submit_all_worse_vaccines.sh**: This generates the simulations and also produces the clinical outcomes for each individual simulation. Note that this requires the clinical pathways model as well, and directories need to be updated in **submit_function_worse_vaccine.script** and **submit_function_worse_vaccines_no_vax.script**
3. **submit_all_worse_vaccines_matlab_R.sh**: This must be run after all the simulations are done. It groups all of the individual simulation outputs together and all the clinical pathway outcomes together. Note that `numsims` may need to be updated as appropriate. Directories need to be updated in **submit_function_worse_vaccine_matlab_R.script** and **submit_function_worse_vaccines_no_vax_matlab_R.script**.
4. Run the plotting code **plot_infections_with_no_vax.py** with correct parameters for `folder`, `presim_parameters_folder`, `novax_folder` and `novax_presim_parameters_folder`.
5. Profit

