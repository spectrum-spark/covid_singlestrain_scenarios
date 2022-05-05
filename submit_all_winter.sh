#!/bin/bash

for POPTYPE in younger
do
for (( PARAMFILENUM=1; PARAMFILENUM<=12; PARAMFILENUM++ ))
do
jid1=$(sbatch --parsable --array=1-100 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} submit_function_winter.script)

sbatch --dependency=afterany:$jid1 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} compress_function_winter.script

done
done

#for POPTYPE in older
#do
#for (( PARAMFILENUM=13; PARAMFILENUM<=24; PARAMFILENUM++ ))
#do
#jid1=$(sbatch --parsable --array=1-100 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} submit_function_winter.script)
#
#sbatch --dependency=afterany:$jid1 --job-name=winter --export=POPULATION_INPUT=${POPTYPE},PARAM_FILE=${PARAMFILENUM} compress_function_winter.script
#
#done
#done
