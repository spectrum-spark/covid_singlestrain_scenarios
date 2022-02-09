#!/bin/bash
# for STATE in SA TAS ACT NT QLD VIC NSW
# do 
# for SCENARIO in jan28 bp15_jan28 bn15_jan28 
# do
#   echo "${STATE}_${SCENARIO}"
#   sbatch --job-name=${STATE}_${SCENARIO} --export=STATE_INPUT=${STATE},SCENARIO_INPUT=${SCENARIO} compress_function.script 
# done
# done


# for STATE in SA TAS ACT NT QLD VIC NSW
# do 
# for SCENARIO in jan28 bp15_jan28 bn15_jan28 
# do

for STATE in NSW
do 
for ASC in 33 50
do
for RED in 50 
do 
for LEVEL in baseline low moderate
do
# for STATE in NSW
# do 
# for SCENARIO in high_jan28_50final low_jan28_50final baseline_jan28_50final
# do
  # echo "${STATE}_${SCENARIO}"
  echo "${STATE}_${ASC}A_${RED}R_${LEVEL}"
  sbatch --job-name=${STATE}_${SCENARIO} --export=STATE_INPUT=${STATE},SCENARIO_INPUT=${ASC}A_${RED}R_${LEVEL} compress_function.script 
done
done
done
done

