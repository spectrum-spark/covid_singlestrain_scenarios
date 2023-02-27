#!/bin/bash

#Scenarios: 

scenario="scenario"${1}"_2000Omicron_"${2}"_reinfectioncount"
echo "Running scenario "${scenario}

jobid=$(sbatch --parsable --job-name=${scenario} clinical_pathwane_relsev2_vec.sh ${scenario})
echo ${jobid}
jobid_knit=$(sbatch --parsable --job-name="knit_"${scenario} --dependency=afterok:$jobid knit_relsev.script ${scenario})
echo ${jobid_knit}