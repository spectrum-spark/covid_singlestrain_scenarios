#!/bin/bash

for POPTYPE in younger older
do
for (( PARAMFILENUM=1; PARAMFILENUM<=6; PARAMFILENUM++ ))
do
for ((TP_i = 1; TP_i<=25;TP_i++))
do
sbatch --parsable --export=POP=${POPTYPE},diffparams=${PARAMFILENUM},TPvers=${TP_i} submit_function_matlab_R.script
done
done
done

for POPTYPE in younger older
do
for PARAMFILENUM in 1
do
for ((TP_i = 1; TP_i<=25;TP_i++))
do
sbatch --parsable --export=POP=${POPTYPE},diffparams=${PARAMFILENUM},TPvers=${TP_i} submit_function_no_vax_matlab_R.script
done
done
done
