#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 1:30:00
#SBATCH --mem=8GB
#SBATCH --array=1-100

module load matlab

matlab -nodisplay -r "sev_mat=[0.5,0.5,0.5;0.25,0.25,0.25;0.1,0.1,0.1];for ii=1:3;clinical_pathways_immunity_relsev2_func('NSW','/scratch/cm37/health/NSW_outputs/scenario14_2000Omicron_Low/sim_number_$SLURM_ARRAY_TASK_ID',sev_mat(ii,:));end;quit()"

