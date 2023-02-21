import subprocess
import os

TP_list = [1.05, 1.95]

WAVESTART_list  = [2,3]

for WAVESTART in WAVESTART_list:

    folder = '/scratch/cm37/tpl/reduced_covid_BA1_BA45_wave_start_'+str(WAVESTART)+'_outputs/'

    for population_type in ["younger","older"]:
        for i in range(len(TP_list)):
            TP_i = i+1 # started index at one for some reason OTL
            TP = TP_list[i]
            for PARAMFILENUM in range(0,7):
                output_folder = "abm_continuous_simulation_parameters_" + population_type +"_" + str(PARAMFILENUM)+"_SOCRATES_TP"+str(TP)
                for SLURM_ARRAY in range(1,51):
                    output_file = "sim_number_" + str(SLURM_ARRAY)+".csv"
                    file_path = os.path.join(folder, output_folder,output_file)
                    if os.path.isfile(file_path):
                        continue
                    else:
                        cmd = "sbatch --parsable --array="+str(SLURM_ARRAY)+" --export=POP="+population_type+",diffparams="+str(PARAMFILENUM)+",TPvers="+str(TP_i)+",BA45start="+str(WAVESTART) +" submit_function_BA1s_BA45s_reduced.script"
                        subprocess.call([cmd], shell=True)

                        