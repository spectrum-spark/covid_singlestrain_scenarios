#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 00:30:00
#SBATCH --mem=16GB
#SBATCH --array=1-100

module load matlab

matlab -nodisplay -r "clinical_pathways_immunity_relsev_func('NSW','/scratch/cm37/health/NSW_outputs/scenario2_2000Omicron_Med/sim_number_$SLURM_ARRAY_TASK_ID',0.25);quit()"

