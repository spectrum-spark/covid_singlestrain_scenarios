from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'sans-serif'})

import matplotlib.pyplot as plt
plt.switch_backend('agg')

import os
import sys
import csv
import pandas as pd
import numpy as np
import json


folder = os.path.join(os.path.dirname(__file__),"..","winter_outputs_t646")

presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","presim_param_files")

def convert_to_array(inputstring):
    # inputstring = inputstring.replace('"','')
    if not bool(inputstring.strip()):
        return []
    else:
        string_array = inputstring.split(";")
        num_array = [float(x) for x in string_array]
        # print(num_array )
        return num_array



for population_type in ["younger","older"]:
    param_list_younger = list(range(1,13))
    param_list_older = list(range(13,25))

    if population_type=="younger":
        population_list = param_list_younger
    else:
        population_list = param_list_older

    # print(population_list)

    for paramNum in population_list:
        subfolder = "abm_simulation_people_params_"+str(paramNum)+"_output_winter_sims_"+population_type+"_init10"

        sim_number_list = [1000]
        for sim_number in sim_number_list:
            list_of_all_people = []
            individuals_filename = "sim_number_"+str(sim_number)+"_individuals.csv"
            individuals_file = os.path.join(folder,subfolder ,individuals_filename )
            # indv_pd_obj = pd.read_csv(individuals_file) # names = ["age", "age bracket", "dose times", "infection times","symptom onset times"]
            # print(indv_pd_obj)
            with open(individuals_file, newline='') as csvfile:
                ind_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                line_count = 0
                
                for row in ind_reader:
                    # print(line_count+1)
                    if line_count == 0:
                        # print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        # print(row)
                        age,age_bracket,dose_times,infection_times,symptom_onset_times = row 
                        new_row = [float(age),int(age_bracket),convert_to_array(dose_times),convert_to_array(infection_times),convert_to_array(symptom_onset_times)]
                        if new_row[-1]!=[]:
                            print(new_row)
                        list_of_all_people.append(new_row)
                        line_count += 1
                        

            # print(list_of_all_people)
            exit(1)



        # filename = "abm_simulation_people_params_"+str(paramNum)+"_output_winter_sims_"+population_type+"_init10"
        # presim_parameters = "abm_pre-simulation_parameters_"+str(paramNum)+".json"
        # presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

        # print(filename)

        # datafilename = filename + ".csv"

        # if population_type =="younger":
        #     plotting_colour =  "lightskyblue"
            
        # elif population_type=="older":
        #     plotting_colour =  "lightcoral"

        # data_file = os.path.join(folder, datafilename)

        # pd_obj = pd.read_csv(data_file)
        # # print(pd_obj)


        # with open(presimfilename, "r") as f:
        #     presim_parameters = json.load(f)
