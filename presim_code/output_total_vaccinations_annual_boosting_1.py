from create_and_generate_initial_conditions import *
import csv

original_program_time = 26*7*3
boosters_only_vaccination_start_list = [original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7  , original_program_time + 52*7 ]
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

boosting_only_group = ['none','5-15','65+','random']



header =['population size', 'population type','scenario', '1st year vaccination coverage','1.5 year vaccination coverage','3 year vaccination coverage', '1.5 year vaccination program primary doses','1.5 year vaccination program booster doses','Further primary doses (1.5 - 3 years)','Further booster doses (1.5 - 3 years)']


folder_name = "parameter_files_annual_boosting_1"

boosting_group_names = {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'}

for boosting_time in boosters_only_vaccination_start_list:
   
    output_file_name = "total_vaccination_over_time_with_annual_boosting_1_high_coverage-"+ str(boosting_time)+ ".csv"
    # todo: need to check that it's all the same regardless of time 

    full_output_file_name = os.path.join(os.path.dirname(__file__),output_file_name )

    with open(full_output_file_name,  'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for population_type in ["older","younger"]:

            for boosting_group_wanted in boosting_only_group: # getting the order how I like it
            
                for number in range(0,12+1):
                    filename = os.path.join(folder_name,"abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json")

                    fullfilename = os.path.join(os.path.dirname(__file__),filename)

                    with open(fullfilename, "r") as f:
                        presim_parameters = json.load(f)

                    total_population = presim_parameters["total_population"]
                    # population_type = presim_parameters["population_type"]
                    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                    booster_fraction = presim_parameters["booster_fraction"]
                    original_vax_priority = presim_parameters["original_vax_priority"]
                    first_additional_vax_priority= presim_parameters["first_additional_vax_priority"]
                    second_additional_vax_priority= presim_parameters["second_additional_vax_priority"]
                    second_additional_doses_available = presim_parameters['second_additional_doses_available']
                    vaccination_start = presim_parameters["boosters_only_vaccination_start"]
                    vaccination_duration = presim_parameters["boosters_only_vaccination_duration"]
                    boosting_group = presim_parameters['boosting_group']

                    if vaccination_start == boosting_time or boosting_group=="none":
                        pass 
                    else:
                        continue 
                    if boosting_group== boosting_group_wanted:
                        pass
                    else:
                        continue


                    vaccination_filename =  os.path.join(folder_name,"abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".csv")

                    vaccination_fullfilename = os.path.join(os.path.dirname(__file__),vaccination_filename)

                    vaccinations = { '1.5 year vaccination program primary doses':0,
                                    '1.5 year vaccination program booster doses':0,
                                    'Further primary doses (1.5 - 3 years)':0,
                                    'Further booster doses (1.5 - 3 years)':0}

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
                                    if vax_days[2]<boosting_time:
                                        vaccinations['1.5 year vaccination program booster doses']+=1*num_people
                                    else:
                                        vaccinations['Further booster doses (1.5 - 3 years)']+=1*num_people
                                elif max_vax==4:
                                    vaccinations['1.5 year vaccination program primary doses'] +=2*num_people
                                    vaccinations['1.5 year vaccination program booster doses']+=1*num_people
                                    vaccinations['Further booster doses (1.5 - 3 years)']+=1*num_people

                    # ['population size', 'population type','scenario', '1st year vaccination coverage','1.5 year vaccination coverage','3 year vaccination coverage', '1.5 year vaccination program primary doses','1.5 year vaccination program booster doses','Further primary doses (1.5 - 3 years)','Further booster doses (1.5 - 3 years)']

                    row = [total_population, population_type,boosting_group_names[boosting_group_wanted],
                        str(total_vaccination_rate*100)+"%",
                        str((vaccinations['1.5 year vaccination program primary doses']/2)/total_population*100)+"%", 
                        str(((vaccinations['1.5 year vaccination program primary doses']+vaccinations['Further primary doses (1.5 - 3 years)'])/2)/total_population*100)+"%",
                        vaccinations['1.5 year vaccination program primary doses'],
                        vaccinations['1.5 year vaccination program booster doses'],
                        vaccinations['Further primary doses (1.5 - 3 years)'],
                        vaccinations['Further booster doses (1.5 - 3 years)']
                        ]

                    writer.writerow(row)