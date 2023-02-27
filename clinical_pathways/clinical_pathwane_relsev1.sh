#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 1:30:00
#SBATCH --mem=8GB
#SBATCH --array=1-100

module load matlab

matlab -nodisplay -r "clinical_pathways_immunity_relsev_func('NSW','/scratch/cm37/health/NSW_outputs/scenario1_2000Omicron/sim_number_$SLURM_ARRAY_TASK_ID',0.5,true);quit()"

