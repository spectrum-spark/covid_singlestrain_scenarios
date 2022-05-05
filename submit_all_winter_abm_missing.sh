#!/bin/bash

for POPTYPE in younger
do

for PARAMFILENUM in 1
do
sbatch --parsable --array=9,18,24,26,27,28,30,31,33,34,38-40,42,43,45,46,48,50,53,54,56-59,61-65,67-69,72,74-76,78-80,82,83,84-86,88-92,94-98 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} submit_function_winter.script
done

for PARAMFILENUM in 2
do
sbatch --parsable --array=1-3,5-11,13,14,16-20,22,24,25,27-34,36-39,41,42,45-58,60-66,68-80,82,84,86-100 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} submit_function_winter.script
done


done
