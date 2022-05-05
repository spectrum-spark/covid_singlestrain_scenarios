#!/bin/bash

for POPTYPE in younger
do
for (( PARAMFILENUM=4; PARAMFILENUM<=4; PARAMFILENUM++ ))
do
sbatch --parsable --array=1-25 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} submit_function_winter.script
sleep 1m
done
done