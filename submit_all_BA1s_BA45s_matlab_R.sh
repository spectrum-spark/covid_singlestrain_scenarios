#!/bin/bash

for WAVESTART in 2 3
do
for POPTYPE in younger older
do
for (( PARAMFILENUM=0; PARAMFILENUM<=9; PARAMFILENUM++ ))
do
for ((TP_i = 1; TP_i<=25;TP_i++))
do
sbatch --parsable --export=POP=${POPTYPE},diffparams=${PARAMFILENUM},TPvers=${TP_i},BA45start = ${WAVESTART} submit_function_BA1s_BA45s_matlab_R.script
done
done
done
done


