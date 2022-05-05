#!/bin/sh
for diffparams in 1 5 9
do
for (( i=2; i<=30; i++ ))
do

 ./RunEmbryoSim state_parameters/omicron_update_VE_updated.json pre-winter_embryo_scenarios/embryo_sim_params_1_younger_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_pre-simulation_parameters_${diffparams}_output

  ./RunEmbryoSim state_parameters/omicron_update_VE_updated.json pre-winter_embryo_scenarios/embryo_sim_params_2_younger_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_pre-simulation_parameters_${diffparams}_output

done
done
for diffparams in 13 17 21
do
for (( i=2; i<=30; i++ ))
do

 ./RunEmbryoSim state_parameters/omicron_update_VE_updated.json pre-winter_embryo_scenarios/embryo_sim_params_1_older_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_pre-simulation_parameters_${diffparams}_output

  ./RunEmbryoSim state_parameters/omicron_update_VE_updated.json pre-winter_embryo_scenarios/embryo_sim_params_2_older_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_pre-simulation_parameters_${diffparams}_output

done
done
