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

    ##############
    TEMP_population = 0.5*(10**6) # aka 500k

    simulated_population_by_age_band= population_by_age_distribution(TEMP_population ,population_type)

    vax_1_dose_by_age_band, full_vax_by_age_band= primary_vaccination_allocation(TEMP_population ,total_vaccination_rate,simulated_population_by_age_band,presim_parameters['oldest_group_vax_coverage'])

    vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band= booster_and_new_primary_vaccination_allocation(TEMP_population ,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band, full_vax_by_age_band,booster_fraction)

    list_of_all_people= vaccination_schedule(TEMP_population ,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,booster_fraction,original_vax_priority,first_additional_vax_priority)

    list_of_all_people = vaccination_schedule_boosters(list_of_all_people,booster_fraction,second_additional_vax_priority,vaccination_start, vaccination_duration)

    ##########################################
    # adjust!
    population_multiplier = int(total_population / TEMP_population) # should be integer

    output_folder = presim_parameters["folder"]
    output_file =  os.path.join(os.path.dirname(__file__),output_folder,output_filename)

    folder_path = os.path.join(os.path.dirname(__file__),output_folder)
    
    if not os.path.exists(folder_path ): # Check whether the specified folder exists or not
        os.makedirs(folder_path ) # Create a new directory because it does not exist 

    # output vaccination schedule needed for the agent-based model simulation
    # output_schedule_extended(list_of_all_people,output_file+".csv")

    header =['age_band','num_people','max_vax','time_1','time_2','time_3', 'time_4','infection','infection_day']

    dict_collected_details = {}

    for person in list_of_all_people:
        vax_days = person.vaccination_days.copy()
        while len(vax_days)<4:
            vax_days.append(-1)
        person_details = (age_band_id[person.age_band],person.max_vax,vax_days[0],vax_days[1],vax_days[2], vax_days[3],int(person.infected),person.infected_day) 
        if person_details in dict_collected_details :
            dict_collected_details[person_details] = dict_collected_details[person_details] +1
        else:
            dict_collected_details[person_details] = 1

    total_people = 0
    with open(output_file+".csv", 'w', newline='') as f:
    # create the csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for person_details, num_people in dict_collected_details.items():
            row =  [person_details[0],int(num_people*population_multiplier),person_details[1],person_details[2],person_details[3],person_details[4],person_details[5],person_details[6],person_details[7]] 
            writer.writerow(row)

            total_people+= int(num_people*population_multiplier)


    print("total_people: ",total_people)


    list_of_all_people = list_of_all_people *population_multiplier
    simulated_population_by_age_band = [x*population_multiplier for x in simulated_population_by_age_band]

    print("len(list_of_all_people): ", len(list_of_all_people))

    ##########################################

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


#####################
# FOR CLUSTER:

print(sys.argv)

total_population_mil = float(sys.argv[1])
if total_population_mil==0.5:
    pass
else:
    total_population_mil = int(total_population_mil)
population_type = sys.argv[2]
number = int(sys.argv[3])


filename =  "/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_expanded_pop_sizes/simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".json"
output_filename="/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_expanded_pop_sizes/simulation_parameters_"  + str(total_population_mil) +"mil_" +  population_type+ "_" + str(number)
simulation_initial_conditions(filename,output_filename)


