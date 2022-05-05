#!/bin/bash

for POPTYPE in younger
do
for (( PARAMFILENUM=2; PARAMFILENUM<=2; PARAMFILENUM++ ))
do
sbatch --parsable --array=1-25 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} submit_function_winter.script
sleep 1m
done
done