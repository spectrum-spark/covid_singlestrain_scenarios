import json
import os
import numpy as np


fixed_parameters_file = "fixed_symptoms_etc.json"
full_fixed_parameters_file = os.path.join(os.path.dirname(__file__),fixed_parameters_file)
with open(full_fixed_parameters_file, "r") as f:
    fixed_parameters = json.load(f)


original_program_time = 26*7*3

root_parameter_folder =  os.path.join(os.path.dirname(__file__),"bivalent_boosting_jsons" ) # putting all the subfolders in here for neatness
root_output_folder = "/scratch/cm37/tpl/bivalent_boosting/"

immune_escape_times = [original_program_time, original_program_time + 26*7, original_program_time + 52*7] # at 1.5 yrs, 2 yrs, and 2.5 yrs

bivalent_start_times = [original_program_time, original_program_time + 26*7, original_program_time + 52*7] # the earlier times since we never have singular boosting at 2.5 years? hmmm I guess have it all for now?

TP_list = [1.05, 1.95]


###################################################################
##### HIGH COVERAGE YOUNGER & OLDER

for immune_escape_time in immune_escape_times:
    for bivalent_start_time in bivalent_start_times:
        # location to save the parameter files
        folder = "high_coverage_immune_escape_t" + str(immune_escape_time) +"_bivalent_t" + str(bivalent_start_time)
        # simulation output directory
        output_directory =root_output_folder + folder +"_outputs/"

        folder_path = os.path.join(root_parameter_folder,folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for population_type in ["older", "younger"]:
            number = 1
            for TP in TP_list:
                param_set = {"folder_suffix": "_SOCRATES_TP"+str(TP) ,
                            "output_directory": output_directory,
                            "t_end": 1200.0,
                            "start_exposure": 225.0,
                            "regular_exposure_infections": 1,
                            "seed_every_x_days":1.0,
                            "new_strain_wave_start_day":immune_escape_time,
                            "bivalent_start_time":bivalent_start_time,
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

###################################################################
##### LOW COVERAGE YOUNGER
for immune_escape_time in immune_escape_times:
    for bivalent_start_time in bivalent_start_times:
        # location to save the parameter files
        folder = "low_coverage_immune_escape_t" + str(immune_escape_time) +"_bivalent_t" + str(bivalent_start_time)
        # simulation output directory
        output_directory =root_output_folder + folder +"_outputs/"

        folder_path = os.path.join(root_parameter_folder,folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

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
                            "bivalent_start_time":bivalent_start_time,
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

###################################################################
##### HIGH COVERAGE YOUNGER & OLDER 6-monthly boosting
for immune_escape_time in immune_escape_times:
    for bivalent_start_time in bivalent_start_times:
        # location to save the parameter files
        folder = "six_monthly_boosting_immune_escape_t" + str(immune_escape_time) +"_bivalent_t" + str(bivalent_start_time)
        # simulation output directory
        output_directory =root_output_folder + folder +"_outputs/"

        folder_path = os.path.join(root_parameter_folder,folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for population_type in ["older", "younger"]:
            number = 1
            for TP in TP_list:
                param_set = {"folder_suffix": "_SOCRATES_TP"+str(TP) ,
                            "output_directory": output_directory,
                            "t_end": 1200.0,
                            "start_exposure": 225.0,
                            "regular_exposure_infections": 1,
                            "seed_every_x_days":1.0,
                            "new_strain_wave_start_day":immune_escape_time,
                            "bivalent_start_time":bivalent_start_time,
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