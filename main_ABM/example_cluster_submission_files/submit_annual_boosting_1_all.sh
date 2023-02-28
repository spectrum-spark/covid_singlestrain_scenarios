#!/bin/bash

for WAVESTART in 546 637 728 819 910
do
for POPTYPE in older younger
do
for (( PARAMFILENUM=0; PARAMFILENUM<=12; PARAMFILENUM++ ))
do
for ((TP_i = 1; TP_i<=2;TP_i++))
do
sbatch --parsable --array=51-100 --export=POP=${POPTYPE},diffparams=${PARAMFILENUM},TPvers=${TP_i},BA45start=${WAVESTART} submit_annual_boosting_1_function.script
sleep 30
done
done
done
done

