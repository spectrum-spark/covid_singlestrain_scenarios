#!/bin/bash
# for STATE in ACT VIC NT SA NSW QLD TAS
for STATE in NSW
do 
for ASC in 33 50
do
for RED in 66 
do 
for LEVEL in baseline low moderate
do
  echo "${STATE}_${ASC}A_${RED}R_${LEVEL}"
  sbatch --job-name=${STATE}_${ASC}A_${RED}R_${LEVEL} --export=STATE_INPUT=${STATE},LEVEL_INPUT=${ASC}A_${RED}R_${LEVEL} submit_function.script 
done
done
done
done
