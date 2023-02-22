from create_and_generate_initial_conditions import *
import csv




original_program_time = 26*7*3
boosters_only_vaccination_start_list = [original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7  , original_program_time + 52*7 ]
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

boosting_only_group = ['none','5-15','65+','primary']



header =['population size', 'population type','scenario', '1st year vaccination coverage','1.5 year vaccination coverage','3 year vaccination coverage', '1.5 year vaccination program primary doses','1.5 year vaccination program booster doses','Further primary doses (1.5 - 3 years)','Further booster doses (1.5 - 3 years)']


folder_name = "parameter_files_annual_boosting_1_younger"

boosting_group_names = {'none':'no further vaccination', '5-15': 'further primary vaccination pediatric','65+':'further boosting high risk','primary':'further primary vaccination random'}


output_file_name = "low_coverage_total_vaccination_over_time_with_annual_boosting_1.csv"
# todo: need to check that it's all the same regardless of time 

full_output_file_name = os.path.join(os.path.dirname(__file__),output_file_name )

boosting_time = original_program_time + 26*7 # aka at two years

with open(full_output_file_name,  'w', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for population_type in ["younger"]:

        for vaccination_coverage_here in [0.2,0.5]:

            for boosting_group_wanted in boosting_only_group: # getting the order how I like it
            
                for number in range(-1,6+1):
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

                    if vaccination_coverage_here ==total_vaccination_rate and boosting_group== boosting_group_wanted:
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
                                else:
                                    if max_vax >=1:
                                        if vax_days[0]<= original_program_time+1:
                                            vaccinations['1.5 year vaccination program primary doses'] +=1*num_people
                                        else:
                                            vaccinations['Further primary doses (1.5 - 3 years)']+=1*num_people

                                    if max_vax>=2:
                                        if vax_days[1]<= original_program_time+1:
                                            vaccinations['1.5 year vaccination program primary doses'] +=1*num_people
                                        else:
                                            vaccinations['Further primary doses (1.5 - 3 years)']+=1*num_people
                                    if max_vax >=3:
                                        if vax_days[2]<= original_program_time+1:
                                            vaccinations['1.5 year vaccination program booster doses']+=1*num_people
                                        else:
                                            vaccinations['Further booster doses (1.5 - 3 years)']+=1*num_people

                                    if max_vax >=4:
                                        if vax_days[3]<= original_program_time+1:
                                            vaccinations['1.5 year vaccination program booster doses']+=1*num_people
                                        else:
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