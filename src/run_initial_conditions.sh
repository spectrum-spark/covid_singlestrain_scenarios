#!/bin/bash
#SBATCH --job-name=initial_generate
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=6G
#SBATCH --cpus-per-task=1
#SBATCH --array=1-20

./RunGenerateInitial state_parameters/omicron_update_VE_updated.json winter_wave_scenarios/sim_params_v1.json $SLURM_ARRAY_TASK_ID  winter_wave_scenarios vax_infect_scenario1