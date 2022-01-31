#!/bin/bash

for STATE in QLD ACT VIC NT SA NSW
do 
for LEVEL in baseline low high
do
  echo "${STATE}_${LEVEL}"
  sbatch --job-name=${STATE}_${LEVEL} --export=STATE_INPUT=${STATE},LEVEL_INPUT=${LEVEL} submit_function.script 
done
done