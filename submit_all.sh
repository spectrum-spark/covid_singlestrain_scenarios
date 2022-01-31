#!/bin/bash

for STATE in QLD ACT VIC NT SA NSW
do 
for LEVEL in baseline low high
do
  echo "${STATE}_${LEVEL}"
  sbatch submit_function.script --job-name=${STATE}_${LEVEL} --export=STATE_INPUT=${STATE},LEVEL_INPUT=${LEVEL},
done
done