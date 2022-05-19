#!/bin/sh

START=$(date "+%s")

for (( i=2; i<=2; i++ ))
do
    for POP in older younger 
    do 
        for diffparams in 1 6
        do
            for TPvers in 1 5
            do
                ./RunContinuousFirstAndContExposure state_parameters/omicron_update_VE_updated.json winter_scenarios_continuous_first_then_cont_exposure/continuous_${POP}_${TPvers}_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\continuous_sim_param_files abm_continuous_simulation_parameters_${POP}_${diffparams}
            done
        done
    done
done





END=$(date "+%s")
echo -e "\n"
echo "ran in $((END-START)) seconds"
