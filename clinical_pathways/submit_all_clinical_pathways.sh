#!/bin/bash

jid1=$(sbatch --parsable --array=1-3 --job-name=clinic_path  submit_clinical_functions_winter.script)

sbatch --dependency=afterany:$jid1 --job-name=clinic_path_comb clinical_comb_plot_winter.script