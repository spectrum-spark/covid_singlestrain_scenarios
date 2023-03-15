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
    second_booster_fraction = presim_parameters['second_booster_fraction']
    vaccination_start = presim_parameters["boosters_only_vaccination_start"]
    vaccination_duration = presim_parameters["boosters_only_vaccination_duration"]
    boosting_group = presim_parameters['boosting_group']

    simulated_population_by_age_band= population_by_age_distribution(total_population,population_type)

    vax_1_dose_by_age_band, full_vax_by_age_band= primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,presim_parameters['oldest_group_vax_coverage'])

    vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band= booster_and_new_primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band, full_vax_by_age_band,booster_fraction)

    list_of_all_people= vaccination_schedule(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,booster_fraction,original_vax_priority,first_additional_vax_priority)

    ################### : "future" : 
    # NEED THIS FOR HIGH COVERAGE
    if total_vaccination_rate==0.8:
        print("total_vaccination_rate:",total_vaccination_rate)
        
        if boosting_group=='none':
            pass # no second boosting
        else:
            
            list_of_all_people =  vaccination_schedule_boosters(list_of_all_people,second_booster_fraction,second_additional_vax_priority,vaccination_start, vaccination_duration)
    else:
        print("lower coverage not down yet")
        exit(1)

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

    plot_vaccination_distributions_extended_percentage_pretty(simulated_population_by_age_band,list_of_all_people,population_type,output_file,presim_parameters)
    
    plot_vaccination_distributions_time_pretty(list_of_all_people,population_type,output_file,presim_parameters)


for population_type in ["older","younger"]:
    for number in range(0,7+1):
        filename =  os.path.join("parameter_files_annual_boosting_age_scenarios","abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json")
        output_filename="abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)
        simulation_initial_conditions(filename,output_filename)
