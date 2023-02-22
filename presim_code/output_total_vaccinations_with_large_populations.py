from create_and_generate_initial_conditions import *
import csv

first_exposure_time =225
second_exposure_time = 450
third_exposure_time = 675
boosters_only_vaccination_start_list = [-1, third_exposure_time+14]
third_vaccination_type_list = ["no further vaccination", "reactive (delayed) vaccination"]

output_file_name = "total_vaccination_over_time.csv"
full_output_file_name = os.path.join(os.path.dirname(__file__),output_file_name )



header =['population size', 'population type','first year vaccination coverage','third wave vaccination type','1.5 year vaccination program primary doses','1.5 year vaccination program booster doses','Further wave 3 primary doses','Further wave 3 booster doses']
# header =['population type','first year vaccination coverage','third wave vaccination type','wave 0 primary doses','wave 0 booster doses','wave 1 primary doses','wave 1 booster doses','wave 2 primary doses','wave 2 booster doses','wave 3 primary doses','wave 3 booster doses']
    
with open(full_output_file_name,  'w', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for total_population_mil in [0.1,0.5,10,100]:
        
        for population_type in ["younger","older"]:
            if total_population_mil==0.1:
                folder_name = "parameter_files_reduced"
            else:
                folder_name = "parameter_files_expanded_pop_sizes"

            for number in range(0,6+1):
                if total_population_mil==0.1:
                    filename =  os.path.join(folder_name,"abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json")
                else:
                    filename =  os.path.join(folder_name,"simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".json")

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

                # read in their csv's instead
                
                if total_population_mil==0.1:
                    vaccination_filename =  os.path.join(folder_name,"abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".csv")
                else:
                    vaccination_filename =  os.path.join(folder_name,"simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".csv")

                vaccination_fullfilename = os.path.join(os.path.dirname(__file__),vaccination_filename)

                vaccinations = {'1.5 year vaccination program primary doses':0,'1.5 year vaccination program booster doses':0,'Further wave 3 primary doses':0,'Further wave 3 booster doses':0}

                with open(vaccination_fullfilename ) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        line_count += 1
                        if line_count == 1:
                            print(f'Column names are {", ".join(row)}')
                            # age_band,num_people,max_vax,time_1,time_2,time_3,time_4,infection,infection_day
                        else:
                            age_band,num_people,max_vax,time_1,time_2,time_3,time_4,infection,infection_day = row 
                            num_people = int(num_people)
                            max_vax = int(max_vax)
                            vax_days = [int(time_1),int(time_2),int(time_3),int(time_4)]
                            if max_vax==0:
                                pass
                            elif max_vax==2:
                                vaccinations['1.5 year vaccination program primary doses'] +=2*num_people
                            elif max_vax==3:
                                vaccinations['1.5 year vaccination program primary doses'] +=2*num_people
                                if vax_days[2]<third_exposure_time:
                                    vaccinations['1.5 year vaccination program booster doses']+=1*num_people
                                else:
                                    vaccinations['Further wave 3 booster doses']+=1*num_people
                            elif max_vax==4:
                                vaccinations['1.5 year vaccination program primary doses'] +=2*num_people
                                vaccinations['1.5 year vaccination program booster doses']+=1*num_people
                                vaccinations['Further wave 3 booster doses']+=1*num_people


                row = [total_population, population_type,total_vaccination_rate, third_vaccination_type, vaccinations['1.5 year vaccination program primary doses'],vaccinations['1.5 year vaccination program booster doses'],vaccinations['Further wave 3 primary doses'],vaccinations['Further wave 3 booster doses']]

                writer.writerow(row)