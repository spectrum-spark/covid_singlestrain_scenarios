import json
import os
import numpy as np


fixed_parameters_file = "fixed_symptoms_etc.json"
full_fixed_parameters_file = os.path.join(os.path.dirname(__file__),fixed_parameters_file)
with open(full_fixed_parameters_file, "r") as f:
    fixed_parameters = json.load(f)

TP_list = [1.05, 1.95]
print(TP_list)

original_program_time = 26*7*3

immune_escape_times = [original_program_time + 26*7]

print(immune_escape_times)

for immune_escape_time in immune_escape_times:
    
    # location to save the parameter files
    folder = "annual_boosting_1_younger_immune_escape_t" + str(immune_escape_time)
    folder_path = os.path.join(os.path.dirname(__file__), "simulation_params",folder)
    if not os.path.exists(folder_path ):
        os.makedirs(folder_path )

    # simulation output directory
    output_directory = os.path.join(os.path.dirname(__file__),"..","outputs",folder+"/")
    if not os.path.exists(output_directory ):
        os.makedirs(output_directory )
    
    for population_type in ["younger"]:
        number = 1
        for TP in TP_list:
            param_set = {"folder_suffix": "_SOCRATES_TP"+str(TP) ,
                        "output_directory": output_directory,
                        "t_end": 1200.0,
                        "start_exposure": 225.0,
                        "regular_exposure_infections": 1,
                        "seed_every_x_days":1.0,
                        "new_strain_wave_start_day":immune_escape_time,
                        "baseline_TP": TP,
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