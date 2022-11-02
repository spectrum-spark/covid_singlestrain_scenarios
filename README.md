# Impact of hybrid immunity on future COVID-19 waves: theoretical populations 

## 1. Run the "presimulation" files 

See https://bitbucket.org/thaople/covid-abm-presim/src/master/ which generates various parameter files and inputs such as demographics, contact matrices, and vaccination rollout.

Copy the contact matrices into this folder.

## 2. Main paper results

Run the following to compile the C++ executable: 

`make -f makefile.main`

### A. Simulations with BA1/2 first wave and BA1/2 second wave

Main source file: `main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses.cpp`


### B. Simulations with BA1/2 first wave and BA4/5-like second wave

Main source file: `main_continuous_simulation_double_exposure_no_ttiq_ibm_4th_doses_newstrain.cpp`


## 3. Supplementary materials

### A. Simulations with BA1/2 first wave and BA1/2 second wave with a worse vaccine

Main source file: `main_continuous_simulation_double_exposure_no_ttiq.cpp`

Run the following to compile the C++ executable: 

`make -f makefile.worsevaccine`

Run the python file `generate_json_files_with_different_TP_vales_and_two_exposures_no_ttiq_450-2.py`, updating the locations of output directories as appropriate. 