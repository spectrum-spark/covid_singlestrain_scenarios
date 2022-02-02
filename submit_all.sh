#!/bin/bash
module load gcc/10.2.0
for STATE in ACT VIC NT SA NSW QLD TAS
do 
for LEVEL in baseline low high
do
  echo "${STATE}_${LEVEL}"
  sbatch --job-name=${STATE}_${LEVEL} --export=STATE_INPUT=${STATE},LEVEL_INPUT=${LEVEL} submit_function.script 
done
done
