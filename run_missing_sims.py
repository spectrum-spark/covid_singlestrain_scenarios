import subprocess
import os

TP_list = [0.85,0.9,0.95, 1.,   1.05, 1.1  ,1.15, 1.2 , 1.25, 1.3, 1.35 ,1.4 , 1.45, 1.5,  1.55, 1.6,
 1.65 ,1.7 , 1.75 ,1.8 , 1.85, 1.9 , 1.95,2.0,2.05]

WAVESTART_list  = [2,3]

for WAVESTART in WAVESTART_list:

    folder = '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_'+str(WAVESTART)+'_outputs/'

    for population_type in ["younger","older"]:
        for i in range(len(TP_list)):
            TP_i = i+1 # started index at one for some reason OTL
            TP = TP_list[i]
            for PARAMFILENUM in range(0,10):
                output_folder = "abm_continuous_simulation_parameters_" + population_type +"_" + str(PARAMFILENUM)+"_SOCRATES_TP"+str(TP)
                for SLURM_ARRAY in range(1,11):
                    output_file = "sim_number_" + str(SLURM_ARRAY)+".csv"
                    file_path = os.path.join(folder, output_folder,output_file)
                    if os.path.isfile(file_path):
                        continue
                    else:
                        # original
                        # sbatch --parsable --array=1-10 --export=POP=${POPTYPE},diffparams=${PARAMFILENUM},TPvers=${TP_i},BA45start=${WAVESTART} submit_function_BA1s_BA45s.script

                        cmd = "sbatch --parsable --array="+str(SLURM_ARRAY)+" --export=POP="+population_type+",diffparams="+str(PARAMFILENUM)+",TPvers="+str(TP_i)+",BA45start="+str(WAVESTART) +" submit_function_BA1s_BA45s.script"
                        subprocess.call([cmd], shell=True)

                        