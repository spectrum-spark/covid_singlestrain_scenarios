import json
import os
import numpy as np

# folder = "winter_scenarios_continuous_double_exposure_no_ttiq_450-2_no_vax"
folder = "winter_scenarios_continuous_double_exposure_no_ttiq_450-2_no_vax_cluster"
folder_path = os.path.join(os.path.dirname(__file__),folder)
# Check whether the specified folder exists or not
if not os.path.exists(folder_path ):
  # Create a new directory because it does not exist 
  os.makedirs(folder_path )

fixed_parameters_file = "fixed_symptoms_etc.json"
full_fixed_parameters_file = os.path.join(os.path.dirname(__file__),fixed_parameters_file)

with open(full_fixed_parameters_file, "r") as f:
    fixed_parameters = json.load(f)


# TP_list = np.linspace(1.1,1.5,5)
# TP_list=np.append(TP_list,[0.8,0.9,1.0,1.6])
# TP_list = np.sort(TP_list)

TP_list = [0.85,0.9,0.95,1.0,1.05, 1.1,1.15, 1.2,1.25, 1.3,1.35,1.4, 1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2.0,2.05]
print(TP_list)



for population_type in ["younger","older"]:
    number = 1
    for TP in TP_list:
        param_set = {"folder_suffix": "_SOCRATES_TP"+str(TP) ,
                    # "output_directory": "C:\\Users\\thaophuongl\\covid_continuous_simulations_double_exposure_no_ttiq_450-2_no_vax_outputs\\",
                    "output_directory":"/scratch/cm37/tpl/covid_continuous_simulations_double_exposure_no_ttiq_450-2_no_vax_outputs/",
                    "t_end": 700.0,
                    "seed_exposure": 225.0,
                    "initial_infections": 100,
                    "second_seed_exposure":450.0,
                    "second_initial_infections": 100,
                    "TP": TP,
                    "ttiq": "no_ttiq",
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