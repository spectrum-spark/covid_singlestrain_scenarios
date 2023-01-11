import subprocess
import os

TP_list = [1.05, 1.95]

original_program_time = 26*7*3

immune_escape_times = [original_program_time + 26*7] 

TOTAL_SIMS = 20


for immune_escape_time in immune_escape_times:

    folder = "/scratch/cm37/tpl/annual_boosting_1_younger_immune_escape_t" + str(immune_escape_time) +"_outputs/"

    for population_type in ["younger"]:
        for i in range(len(TP_list)):
            TP_i = i+1 # started index at one for some reason OTL
            TP = TP_list[i]
            for PARAMFILENUM in range(1,6+1):

                output_folder = "abm_continuous_simulation_parameters_" + population_type +"_" + str(PARAMFILENUM)+"_SOCRATES_TP"+str(TP)
                for SLURM_ARRAY in range(1,TOTAL_SIMS +1):
                    output_file = "sim_number_" + str(SLURM_ARRAY)+".csv"
                    file_path = os.path.join(folder, output_folder,output_file)
                    if os.path.isfile(file_path):
                        continue
                    else:
                        cmd = "sbatch --parsable --array="+str(SLURM_ARRAY)+" --export=POP="+population_type+",diffparams="+str(PARAMFILENUM)+",TPvers="+str(TP_i)+",BA45start="+str(immune_escape_time) +" submit_annual_boosting_1_younger_function.script"
                        subprocess.call([cmd], shell=True)

                        