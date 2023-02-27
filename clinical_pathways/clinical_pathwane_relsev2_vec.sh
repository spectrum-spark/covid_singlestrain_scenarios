#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 1:30:00
#SBATCH --mem=16GB
#SBATCH --array=1-100
#SBATCH --job-name=KnitWane

module load matlab

matlab -nodisplay -r "sev_mat=[1,1,1;0.5,0.5,0.5;0.25,0.25,0.25;0.1,0.1,0.1];for ii=1:size(sev_mat,2);clinical_pathways_immunity_relsev2_func('NSW','/scratch/cm37/health/NSW_outputs/$1/sim_number_$SLURM_ARRAY_TASK_ID',sev_mat(ii,:));end;quit()"

