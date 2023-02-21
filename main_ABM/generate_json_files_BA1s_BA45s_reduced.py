import json
import os
import numpy as np


fixed_parameters_file = "fixed_symptoms_etc.json"
full_fixed_parameters_file = os.path.join(os.path.dirname(__file__),fixed_parameters_file)
with open(full_fixed_parameters_file, "r") as f:
    fixed_parameters = json.load(f)

#TP_list = [0.85,0.9,0.95, 1.,   1.05, 1.1  ,1.15, 1.2 , 1.25, 1.3, 1.35 ,1.4 , 1.45, 1.5,  1.55, 1.6, 1.65 ,1.7 , 1.75 ,1.8 , 1.85, 1.9 , 1.95,2.0,2.05]
TP_list = [1.05, 1.95]
print(TP_list)


for new_strain_wave_start in [2,3]: # either 2 or 3, for wave 2 or wave 3

    
    # location to save the parameter files
    folder = "reduced_json_BA1_BA45_wave_start_" + str(new_strain_wave_start)
    # simulation output directory
    output_directory = "/scratch/cm37/tpl/reduced_covid_BA1_BA45_wave_start_" + str(new_strain_wave_start) +"_outputs/"


    folder_path = os.path.join(os.path.dirname(__file__),folder)
    if not os.path.exists(folder_path ):
        os.makedirs(folder_path )
    

    for population_type in ["younger","older"]:
        number = 1
        for TP in TP_list:
            param_set = {"folder_suffix": "_SOCRATES_TP"+str(TP) ,
                        "output_directory": output_directory,
                        "t_end": 1000.0,
                        "first_exposure_time":225,
                        "first_exposure_infections":100,
                        "second_exposure_time": 450,
                        "second_exposure_infections":100,
                        "third_exposure_time": 675,
                        "third_exposure_infections": 100,
                        "new_strain_wave_start": new_strain_wave_start, 
                        "baseline_TP": TP, # 6.32 
                        "start_restrictions": -1.0,
                        "finish_restrictions": -1.0,
                        "mobility_restrictions": 1.0,  # aka no actual mobility restrictions
                        "ttiq": "no_ttiq",
                        "contact_matrix": "contact_matrix_SOCRATES_" + population_type + ".csv"}
            for key in fixed_parameters:
                param_set[key] = fixed_parameters[key]
            
            
            file_save_name = "sim_params_" + population_type+ "_" + str(number)+".json"
            fullfilename = os.path.join(folder_path,file_save_name)

            # Serializing json 
            json_object = json.dumps(param_set, indent = 4)
            
            # Writing to sample.json
            with open(fullfilename, "w") as outfile:
                outfile.write(json_object)

            number+=1