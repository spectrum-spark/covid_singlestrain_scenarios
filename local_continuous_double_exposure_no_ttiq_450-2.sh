#!/bin/sh

START=$(date "+%s")

for (( i=1; i<=5; i++ ))
do
    for POP in older younger 
    do 
        for (( diffparams=1; diffparams<=6; diffparams++ ))
        do
            for TPvers in 1 2 3 9
            do
                ./RunContinuousDoubleExposureNoTTIQ state_parameters/omicron_update_VE_updated.json winter_scenarios_continuous_double_exposure_no_ttiq_450-2/continuous_${POP}_${TPvers}_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\continuous_sim_param_files abm_continuous_simulation_parameters_${POP}_${diffparams}
            done
        done
    done
done





END=$(date "+%s")
echo -e "\n"
echo "ran in $((END-START)) seconds"
