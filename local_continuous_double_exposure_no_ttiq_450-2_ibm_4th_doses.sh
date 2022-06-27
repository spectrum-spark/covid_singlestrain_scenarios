#!/bin/sh

START=$(date "+%s")

for (( i=1; i<=5; i++ ))
do
    for POP in older younger 
    do 
        for (( diffparams=1; diffparams<=6; diffparams++ ))
        do
            for ((TPvers = 16; TPvers<=21;TPvers++))
            do
                ./RunContinuousDoubleExposureNoTTIQibm4thdoses updated_omicron_parameters/omicron_May_2022_updates.json winter_scenarios_continuous_double_exposure_no_ttiq_450-2_ibm_4th_doses/continuous_${POP}_${TPvers}_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\continuous_sim_param_files abm_continuous_simulation_parameters_${POP}_${diffparams}
            done
        done
    done
done





END=$(date "+%s")
echo -e "\n"
echo "ran in $((END-START)) seconds"
