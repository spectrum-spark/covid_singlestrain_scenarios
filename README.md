# Impact of hybrid immunity on future COVID-19 waves: theoretical populations 

## 1. Run the "presimulation" files 

See https://bitbucket.org/thaople/covid-abm-presim/src/master/ which generates various parameter files and inputs such as demographics, contact matrices, and vaccination rollout.

Copy the contact matrices into this folder (or make a note of where they are and update in the `generate_json_files_....` files)

## 2. Main paper results

Run the following to compile the C++ executable: 

`make -f makefile.main`

### A. Simulations with BA1/2 first wave and BA1/2 second wave

Main source file: `main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses.cpp`

Run the python file `generate_json_files_with_different_TP_values_and_two_exposures_no_ttiq_450-2_ibm_4th_doses.py`, updating the locations of output directories as appropriate.

Then run the bash file...

Then run the clinical pathways scripts...

Then run the plotting scripts...


### B. Simulations with BA1/2 first wave and BA4/5-like second wave

Main source file: `main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses_newstrain.cpp`

Run the python file `generate_json_files_no_ttiq_450-2_ibm_4th_doses_newstrain.py`, updating the locations of output directories as appropriate. 

## 3. Supplementary materials

### A. Simulations with BA1/2 first wave and BA1/2 second wave with a worse vaccine

Main source file: `main_continuous_simulation_double_exposure_no_ttiq.cpp`

Run the following to compile the C++ executable: 

`make -f makefile.worsevaccine`

Run the python file `generate_json_files_with_different_TP_values_and_two_exposures_no_ttiq_450-2.py`, updating the locations of output directories as appropriate. 

Run:

1. `submit_all_worse_vaccines.sh`
2. `submit_all_worse_vaccines_no_vax.sh`
3. `submit_all_worse_vaccines_matlab_R.sh`
4. `submit_all_worse_vaccines_no_vax_matlab_R.sh`

