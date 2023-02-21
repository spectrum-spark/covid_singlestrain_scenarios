import subprocess
import os
import time

TP_list = [1.05, 1.95]

WAVESTART_list  = [2,3]

total_population_mil_list = [0.5,10,100]

total_population_mil= 100


submit_counts = 0
unlatched = True
for WAVESTART in WAVESTART_list:

    folder = "/scratch/cm37/tpl/reduced_cont_intros_covid_BA1_BA45_wave_start_" + str(WAVESTART) +"_"  + str(total_population_mil) +"mil"+"_outputs/"

    for population_type in ["younger","older"]:
        for i in range(len(TP_list)):
            TP_i = i+1 # started index at one for some reason OTL
            TP = TP_list[i]
            for PARAMFILENUM in range(0,7):
                output_folder = "simulation_parameters_"+str(total_population_mil) +"mil_" + population_type +"_" + str(PARAMFILENUM)+"_SOCRATES_TP"+str(TP)
                for SLURM_ARRAY in range(1,51):
                    output_file = "sim_number_" + str(SLURM_ARRAY)+".csv"
                    file_path = os.path.join(folder, output_folder,output_file)
                    if os.path.isfile(file_path):
                        continue
                    else:
                        print(file_path)

                        cmd = "sbatch --parsable --array="+str(SLURM_ARRAY)+" --export=totalpopulationmil="+str(total_population_mil)+",POP="+population_type+",diffparams="+str(PARAMFILENUM)+",TPvers="+str(TP_i)+",BA45start="+str(WAVESTART) +" submit_function_BA1s_BA45s_reduced_cont_intros_expanded_pop.script"
                        subprocess.call([cmd], shell=True)

                        submit_counts=submit_counts+1
                        time.sleep(60)
                        unlatched = True

                    if submit_counts>0 and submit_counts%50 ==0 and unlatched:
                        time.sleep(60*15)
                        unlatched = False

                        