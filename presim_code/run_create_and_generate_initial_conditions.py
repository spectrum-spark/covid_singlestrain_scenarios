# actually runs the functions from the following files:
from create_and_generate_initial_conditions import *
from create_and_generate_initial_conditions_plotting import *
import sys

def simulation_initial_conditions(filename,output_filename):
    fullfilename = os.path.join(os.path.dirname(__file__),filename)

    with open(fullfilename, "r") as f:
        presim_parameters = json.load(f)

    total_population = presim_parameters["total_population"]
    population_type = presim_parameters["population_type"]
    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
    booster_fraction = presim_parameters["booster_fraction"]
    original_vax_priority = presim_parameters["original_vax_priority"]
    first_additional_vax_priority= presim_parameters["first_additional_vax_priority"]
    second_additional_vax_priority= presim_parameters["second_additional_vax_priority"]
    vaccination_start = presim_parameters["boosters_only_vaccination_start"]
    vaccination_duration = presim_parameters["boosters_only_vaccination_duration"]

    simulated_population_by_age_band= population_by_age_distribution(total_population,population_type)

    vax_1_dose_by_age_band, full_vax_by_age_band= primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,presim_parameters['oldest_group_vax_coverage'])

    vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band= booster_and_new_primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band, full_vax_by_age_band,booster_fraction)

    list_of_all_people= vaccination_schedule(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,booster_fraction,original_vax_priority,first_additional_vax_priority)

    list_of_all_people = vaccination_schedule_boosters(list_of_all_people,booster_fraction,second_additional_vax_priority,vaccination_start, vaccination_duration)

    output_folder = presim_parameters["folder"]
    output_file =  os.path.join(os.path.dirname(__file__),output_folder,output_filename)

    folder_path = os.path.join(os.path.dirname(__file__),output_folder)
    
    if not os.path.exists(folder_path ): # Check whether the specified folder exists or not
        os.makedirs(folder_path ) # Create a new directory because it does not exist 

    # output vaccination schedule needed for the agent-based model simulation
    output_schedule_extended(list_of_all_people,output_file+".csv")

    # # age distribution plots
    # # plot_age_distribution(simulated_population_by_age_band,output_file, population_type)
    # plot_age_distribution_pretty(simulated_population_by_age_band,output_file, population_type)

    # # vaccination-related plots
    # # plot_vaccination_distributions(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,list_of_all_people,population_type,output_file,presim_parameters)
    # # plot_vaccination_distributions_poster(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,list_of_all_people,population_type,output_file,presim_parameters)

    # plot_vaccination_distributions_percentage_pretty(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,population_type,output_file,presim_parameters)

    # plot_vaccination_status_distributions_pretty(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,population_type,output_file,presim_parameters)

    # main plotting here!>>>

    # plot_vaccination_distributions_extended_percentage_pretty(simulated_population_by_age_band,list_of_all_people,population_type,output_file,presim_parameters)
    
    # plot_vaccination_distributions_time_pretty(list_of_all_people,population_type,output_file,presim_parameters)


for population_type in ["older","younger"]:
    for number in range(0,9+1):
        filename =  os.path.join("parameter_files","abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json")
        output_filename="abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)
        simulation_initial_conditions(filename,output_filename)


# for population_type in ["younger","older"]:
#     for number in range(0,6+1):
#         filename =  os.path.join("parameter_files_reduced","abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json")
#         output_filename="abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)
#         simulation_initial_conditions(filename,output_filename)

# for total_population_mil in [0.5,10,100]:
#     for population_type in ["younger","older"]:
#         for number in range(0,6+1):
#             filename =  os.path.join("parameter_files_expanded_pop_sizes", "simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".json")
#             output_filename="simulation_parameters_"  + str(total_population_mil) +"mil_" +  population_type+ "_" + str(number)
#             simulation_initial_conditions(filename,output_filename)


# for total_population_mil in [0.5]:
#     for population_type in ["younger","older"]:
#         for number in range(0,6+1):
#             filename =  os.path.join("parameter_files_expanded_pop_sizes", "simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".json")
#             output_filename="simulation_parameters_"  + str(total_population_mil) +"mil_" +  population_type+ "_" + str(number)
#             simulation_initial_conditions(filename,output_filename)

#####################
# FOR CLUSTER:

# print(sys.argv)

# total_population_mil = float(sys.argv[1])
# if total_population_mil==0.5:
#     pass
# else:
#     total_population_mil = int(total_population_mil)
# population_type = sys.argv[2]
# number = int(sys.argv[3])


# check_if_file_exists = "/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_expanded_pop_sizes/simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".csv"

# if os.path.isfile(check_if_file_exists):
#     print("file already exists:",check_if_file_exists)
#     exit(0)


# filename =  "/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_expanded_pop_sizes/simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".json"
# output_filename="/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_expanded_pop_sizes/simulation_parameters_"  + str(total_population_mil) +"mil_" +  population_type+ "_" + str(number)
# simulation_initial_conditions(filename,output_filename)