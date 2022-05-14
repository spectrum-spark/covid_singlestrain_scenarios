import json
import os
import numpy as np

folder = "winter_scenarios_continuous_double_exposure"
folder_path = os.path.join(os.path.dirname(__file__),folder)
# Check whether the specified folder exists or not
if not os.path.exists(folder_path ):
  # Create a new directory because it does not exist 
  os.makedirs(folder_path )

fixed_parameters_file = "fixed_symptoms_etc.json"
fixed_param_folder = "winter_scenarios_continuous"
full_fixed_parameters_file = os.path.join(os.path.dirname(__file__),fixed_param_folder,fixed_parameters_file)

with open(full_fixed_parameters_file, "r") as f:
    fixed_parameters = json.load(f)




TP_list = np.linspace(1.2,2.9,5)
print(TP_list)

for population_type in ["younger","older"]:
    number = 1
    for TP in TP_list:
        param_set = {"folder_suffix": "_SOCRATES_TP"+str(TP) ,
                    "output_directory": "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_outputs\\",
                    "t_end": 650.0,
                    "seed_exposure": 250.0,
                    "initial_infections": 100,
                    "second_seed_exposure":370.0,
                    "second_initial_infections": 100,
                    "TP": TP,
                    "ttiq": "partial",
                    "contact_matrix": "contact_matrix_SOCRATES_" + population_type + ".csv"}
        for key in fixed_parameters:
            param_set[key] = fixed_parameters[key]
        
        
        file_save_name = "continuous_" + population_type+ "_" + str(number)+"_local.json"
        fullfilename = os.path.join(folder_path,file_save_name)

        # Serializing json 
        json_object = json.dumps(param_set, indent = 4)
        
        # Writing to sample.json
        with open(fullfilename, "w") as outfile:
            outfile.write(json_object)

        number+=1