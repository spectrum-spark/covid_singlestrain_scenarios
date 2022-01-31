#!/bin/bash
for STATE in ACT VIC NT SA NSW
do 
for SCENARIO in jan28 bp15_jan28 bn15_jan28 
do
  echo "${STATE}_${SCENARIO}"
  sbatch --job-name=${STATE}_${SCENARIO} --export=STATE_INPUT=${STATE},SCENARIO_INPUT=${SCENARIO} compress_function.script 
done
done

for STATE in ACT VIC NT SA NSW
do 
for SCENARIO in jan28 bp15_jan28 bn15_jan28 
do
  echo "${STATE}_${SCENARIO}"
  sbatch --job-name=${STATE}_${SCENARIO} --export=STATE_INPUT=${STATE},SCENARIO_INPUT=${SCENARIO}_Christmas05 compress_function.script 
done
done
