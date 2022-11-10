#!/bin/bash

for WAVESTART in 2
do
for POPTYPE in younger
do
for (( PARAMFILENUM=0; PARAMFILENUM<=1; PARAMFILENUM++ ))
do
for ((TP_i = 1; TP_i<=1;TP_i++))
do
sbatch --parsable --array=1 --export=POP=${POPTYPE},diffparams=${PARAMFILENUM},TPvers=${TP_i},BA45start=${WAVESTART} submit_function_BA1s_BA45s.script
done
done
done
done

