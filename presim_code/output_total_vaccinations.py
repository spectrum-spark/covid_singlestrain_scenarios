from create_and_generate_initial_conditions import *

first_exposure_time =225
second_exposure_time = 450
third_exposure_time = 675
boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]
third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"] 

output_file_name = "total_vaccination_over_time.csv"
full_output_file_name = os.path.join(os.path.dirname(__file__),output_file_name )



header =['population type','first year vaccination coverage','third wave vaccination type','1.5 year vaccination program primary doses','1.5 year vaccination program booster doses','Further wave 3 primary doses','Further wave 3 booster doses']
# header =['population type','first year vaccination coverage','third wave vaccination type','wave 0 primary doses','wave 0 booster doses','wave 1 primary doses','wave 1 booster doses','wave 2 primary doses','wave 2 booster doses','wave 3 primary doses','wave 3 booster doses']
    
with open(full_output_file_name,  'w', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for population_type in ["younger","older"]:
        for number in range(0,9+1):
            filename =  os.path.join("parameter_files","abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json")

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

            third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(vaccination_start)]
            if total_vaccination_rate==0 or third_vaccination_type in third_vaccination_types_wanted:
                pass 
            else:
                continue

            simulated_population_by_age_band= population_by_age_distribution(total_population,population_type)

            vax_1_dose_by_age_band, full_vax_by_age_band= primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,presim_parameters['oldest_group_vax_coverage'])

            vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band= booster_and_new_primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band, full_vax_by_age_band,booster_fraction)

            list_of_all_people= vaccination_schedule(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,booster_fraction,original_vax_priority,first_additional_vax_priority)

            list_of_all_people = vaccination_schedule_boosters(list_of_all_people,booster_fraction,second_additional_vax_priority,vaccination_start, vaccination_duration)

            vaccinations = {'1.5 year vaccination program primary doses':0,'1.5 year vaccination program booster doses':0,'Further wave 3 primary doses':0,'Further wave 3 booster doses':0}
            for person in list_of_all_people:
                vax_days = person.vaccination_days.copy()

                if len(vax_days)==0:
                    continue
                elif len(vax_days)==2: 
                    vaccinations['1.5 year vaccination program primary doses'] +=2
                elif len(vax_days)==3:
                    vaccinations['1.5 year vaccination program primary doses'] +=2
                    if vax_days[2]<third_exposure_time:
                        vaccinations['1.5 year vaccination program booster doses']+=1
                    else:
                        vaccinations['Further wave 3 booster doses']+=1
                elif len(vax_days) ==4:
                    vaccinations['1.5 year vaccination program primary doses'] +=2
                    vaccinations['1.5 year vaccination program booster doses']+=1
                    vaccinations['Further wave 3 booster doses']+=1


            row = [population_type,total_vaccination_rate, third_vaccination_type, vaccinations['1.5 year vaccination program primary doses'],vaccinations['1.5 year vaccination program booster doses'],vaccinations['Further wave 3 primary doses'],vaccinations['Further wave 3 booster doses']]
            
            # row = [population_type,total_vaccination_rate, third_vaccination_type, vaccinations['wave 0 primary doses'], vaccinations['wave 0 booster doses'], vaccinations['wave 1 primary doses'], vaccinations['wave 1 booster doses'], vaccinations['wave 2 primary doses'], vaccinations['wave 2 booster doses'], vaccinations['wave 3 primary doses'], vaccinations['wave 3 booster doses']] 


            writer.writerow(row)