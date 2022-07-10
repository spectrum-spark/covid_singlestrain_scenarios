#!/bin/sh

START=$(date "+%s")

for (( i=10; i<=10; i++ ))
do
    for POP in younger older
    do 
        for (( diffparams=1; diffparams<=6; diffparams++ ))
        do
            for ((TPvers = 1; TPvers<=25;TPvers++))
            do
                ./RunContinuousDoubleExposureNoTTIQibm4thdoses updated_omicron_parameters/omicron_May_2022_updates.json winter_scenarios_continuous_double_exposure_no_ttiq_450-2_ibm_4th_doses_rerun/continuous_${POP}_${TPvers}_local.json $i C:\\Users\\thaophuongl\\covid-abm-presim\\continuous_sim_param_files abm_continuous_simulation_parameters_${POP}_${diffparams}
            done
        done
    done
done


END=$(date "+%s")
echo -e "\n"
echo "ran in $((END-START)) seconds"
