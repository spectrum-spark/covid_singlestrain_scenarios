#!/bin/sh

START=$(date "+%s")

for (( i=1000; i<=1000; i++ ))
do
for (( diffparams=1; diffparams<=1; diffparams++ ))
do
 ./RunWinter state_parameters/omicron_update_VE_updated.json winter_scenarios/winter_sims_younger_init10_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\initial_condition_files abm_simulation_people_params_${diffparams}_output
done
done

END=$(date "+%s")
echo -e "\n"
echo "ran in $((END-START)) seconds"
