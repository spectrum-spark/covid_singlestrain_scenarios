#!/bin/bash
for STATE in ACT VIC NT SA NSW QLD TAS
# for STATE in TAS
do 
for LEVEL in baseline low high
# for LEVEL in high low
do
  echo "${STATE}_${LEVEL}"
  sbatch --job-name=${STATE}_${LEVEL} --export=STATE_INPUT=${STATE},LEVEL_INPUT=${LEVEL} submit_function.script 
done
done
