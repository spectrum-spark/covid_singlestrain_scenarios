#!/bin/bash

for POPTYPE in younger
do
for PARAMFILENUM in 1 13
do
sbatch --parsable --array=1-25 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} submit_function_winter.script
done
done