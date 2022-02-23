#!/bin/bash
# for STATE in ACT VIC NT SA NSW QLD TAS
# for STATE in NSW
# do 
# for ASC in 33 50
# do
# for RED in 66 
# do 
# for LEVEL in baseline low moderate
# do
for STATE in SA NSW
do 
for ASC in 33 50  
do
for RED in 50 66
do 
for LEVEL in baseline moderate low
do
  echo "${STATE}_${ASC}A_${RED}R_${LEVEL}"
  jid1=$(sbatch --parsable --array=1-20 --job-name=${STATE}_${ASC}A_${RED}R_${LEVEL} --export=STATE_INPUT=${STATE},LEVEL_INPUT=${ASC}A_${RED}R_${LEVEL} submit_function.script)

  sbatch --dependency=afterany:$jid1 --job-name=${STATE}_${SCENARIO} --export=STATE_INPUT=${STATE},SCENARIO_INPUT=long_${ASC}A_${RED}R_${LEVEL} compress_function.script 
done
done
done
done
