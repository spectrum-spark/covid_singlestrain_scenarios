#!/bin/sh

START=$(date "+%s")

for (( i=2; i<=50; i++ ))
do
for (( diffparams=1; diffparams<=12; diffparams++ ))
do
 ./RunWinter state_parameters/omicron_update_VE_updated.json winter_scenarios/winter_sims_younger_init10_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_simulation_people_params_${diffparams}_output
done
for (( diffparams=13; diffparams<=24; diffparams++ ))
do
 ./RunWinter state_parameters/omicron_update_VE_updated.json winter_scenarios/winter_sims_older_init10_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_simulation_people_params_${diffparams}_output
done
done

END=$(date "+%s")
echo -e "\n"
echo $((END-START))