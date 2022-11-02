#!/bin/bash

for POPTYPE in younger older
do
for (( PARAMFILENUM=1; PARAMFILENUM<=6; PARAMFILENUM++ ))
do
for ((TP_i = 1; TP_i<=25;TP_i++))
do
sbatch --parsable --array=1-10 --export=POP=${POPTYPE},diffparams=${PARAMFILENUM},TPvers=${TP_i} submit_function_worse_vaccine.script
done
done
done

