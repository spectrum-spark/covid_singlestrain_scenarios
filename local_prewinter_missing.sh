#!/bin/sh
#./RunEmbryoSim state_parameters/omicron_update_VE_updated.json pre-winter_embryo_scenarios/embryo_sim_params_1_younger_local.json 10 C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_pre-simulation_parameters_1_output


for diffparams in 13
do
for (( i=1; i<=50; i++ ))
do

 ./RunEmbryoSim state_parameters/omicron_update_VE_updated.json pre-winter_embryo_scenarios/embryo_sim_older_TP2.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_pre-simulation_parameters_${diffparams}_output

 ./RunEmbryoSim state_parameters/omicron_update_VE_updated.json pre-winter_embryo_scenarios/embryo_sim_older_TP2.5.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_pre-simulation_parameters_${diffparams}_output

done
done