import subprocess
import os
import time
import sys 


TP_list = [1.05, 1.95]

SLURM_start = int(sys.argv[1])
SLURM_end = int(sys.argv[2])
population_type = sys.argv[3]
PARAMFILENUM = int(sys.argv[4])
TP_i = int(sys.argv[5])
i = TP_i-1
immune_escape_time = int(sys.argv[6])
bivalent_start_time = int(sys.argv[7])


folder = "/scratch/cm37/tpl/bivalent_boosting/low_coverage_immune_escape_t" + str(immune_escape_time) +"_bivalent_t" + str(bivalent_start_time) +"_outputs/"

TP = TP_list[i]

output_folder = "abm_continuous_simulation_parameters_" + population_type +"_" + str(PARAMFILENUM)+"_SOCRATES_TP"+str(TP)
for SLURM_ARRAY in range(SLURM_start,SLURM_end+1):
    output_file = "sim_number_" + str(SLURM_ARRAY)+".csv"
    file_path = os.path.join(folder, output_folder,output_file)
    if os.path.isfile(file_path):
        continue
    else:
        cmd = "sbatch --parsable --array="+str(SLURM_ARRAY)+" --export=POP="+population_type+",diffparams="+str(PARAMFILENUM)+",TPvers="+str(TP_i)+",BA45start="+str(immune_escape_time)+",bivalent="+str(bivalent_start_time)  +" bivalent_low_coverage_all.script"
        subprocess.call([cmd], shell=True)
