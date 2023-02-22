import json
import os


folder = "parameter_files_annual_boosting_1_younger"
folder_path = os.path.join(os.path.dirname(__file__),folder)
if not os.path.exists(folder_path ):
  os.makedirs(folder_path )

# max_daily_allocation is a fraction of daily doses that can go to this group.
# dose 1 first (with oldest first), then dose 2 (with oldest first)

age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']

# primary doses



for total_population in [100000]:
    for population_type in ["younger"]:
        number = 1
        for vaccination_rate in [0.2,0.5]:
            delivery_dose_then_age = {0:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[1],'max_daily_allocation':1},
                            1:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[1],'max_daily_allocation':1},
                            2:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[2],'max_daily_allocation':1},
                            3:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[2],'max_daily_allocation':1}
                            }

            # if vaccination_rate==0:
            #     oldest_group_coverage = 0
            #     delivery_dose_then_age = {0:{'ages':[],'dose_numbers':[],'max_daily_allocation':0}}
            if vaccination_rate < 0.4: #low
                oldest_group_coverage = 0.8
            else:
                oldest_group_coverage = 0.95

            past_booster_fraction = 0.8

            first_boosters = {0:{'ages':age_bands_abm[1:],'dose_numbers':[3],'max_daily_allocation':past_booster_fraction},
                                        1:{'ages':age_bands_abm[1:],'dose_numbers':[1],'max_daily_allocation':1},
                                        2:{'ages':age_bands_abm[1:],'dose_numbers':[2],'max_daily_allocation':1}}
            # booster doses are first regardless of age, with booster_fraction level of daily administered doses
            # after that, new 1st and 2nd doses are given fully if possible

            original_program_time = 26*7*3
            boosters_only_vaccination_start = original_program_time + 26*7 # aka at two years
            boosters_only_vaccination_duration = 13*7# i.e. about 3 months

            boosting_only_group = ['5-15','65+','primary']



            for boosting_group in boosting_only_group:
                if boosting_group == '5-15': # primary rollout to young people
                    second_boosters = {0:{'ages':["5-11","12-15"],'dose_numbers':[1],'max_daily_allocation':1},1:{'ages':["5-11","12-15"],'dose_numbers':[2],'max_daily_allocation':1}}
                elif boosting_group=='65+': # boosting high risk first, with extra just in case there are extra doses available
                    second_boosters = {0:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[3,4],'max_daily_allocation':1},
                    1:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[3,4],'max_daily_allocation':1}}
                elif boosting_group =='primary':
                    second_boosters = delivery_dose_then_age  
                    # {0:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[1,2],'max_daily_allocation':1},
                    #         1:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[1,2],'max_daily_allocation':1}}

                if population_type == 'older':
                    second_boosters_doses =11000 # 12498*total_population/100000 # past_booster_fraction*  = 9998.4 LOL
                    # populations in each age groups for older population distribution
                    # 0-4: 5738
                    # 5-19:  7950, 4548, 4472 = 16970 
                    # 5-15: 7950, 4548 = 12498 
                    # 65+: 5169, 3937, 2599, 3406 = 15111 
                else:
                    second_boosters_doses =11000 # for now, just keeping the same number...
                    # print("need to define boosters available for younger population")
                    # exit(1)

                for year in [2021]:
                    param_set = {'total_population':total_population,
                                    'population_type': population_type,
                                    'total_vaccination_rate':vaccination_rate,
                                    'oldest_group_vax_coverage':oldest_group_coverage,
                                    'original_vax_priority':delivery_dose_then_age,
                                    'booster_fraction':past_booster_fraction,
                                    'first_additional_vax_priority':first_boosters,
                                    'second_additional_vax_priority':second_boosters,
                                    'second_additional_doses_available':second_boosters_doses,
                                    'boosting_group':boosting_group,
                                    'boosters_only_vaccination_start':boosters_only_vaccination_start,
                                    'boosters_only_vaccination_duration':boosters_only_vaccination_duration,
                                    'year': year,
                                    'age_bands' :age_bands_abm,
                                    'folder': folder
                                    }

                    file_save_name = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json"
                    fullfilename = os.path.join(folder_path,file_save_name)

                    # Serializing json 
                    json_object = json.dumps(param_set, indent = 4)
                    
                    # Writing to sample.json
                    with open(fullfilename, "w") as outfile:
                        outfile.write(json_object)

                    number+=1 




for total_population in [100000]:
    for population_type in ["younger"]:
        number = -1
        for vaccination_rate in [0.2,0.5]:
            delivery_dose_then_age = {0:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[1],'max_daily_allocation':1},
                            1:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[1],'max_daily_allocation':1},
                            2:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[2],'max_daily_allocation':1},
                            3:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[2],'max_daily_allocation':1}
                            }

            # if vaccination_rate==0:
            #     oldest_group_coverage = 0
            #     delivery_dose_then_age = {0:{'ages':[],'dose_numbers':[],'max_daily_allocation':0}}
            if vaccination_rate < 0.4: #low
                oldest_group_coverage = 0.8
            else:
                oldest_group_coverage = 0.95

            past_booster_fraction = 0.8

            first_boosters = {0:{'ages':age_bands_abm[1:],'dose_numbers':[3],'max_daily_allocation':past_booster_fraction},
                                        1:{'ages':age_bands_abm[1:],'dose_numbers':[1],'max_daily_allocation':1},
                                        2:{'ages':age_bands_abm[1:],'dose_numbers':[2],'max_daily_allocation':1}}
            # booster doses are first regardless of age, with booster_fraction level of daily administered doses
            # after that, new 1st and 2nd doses are given fully if possible

            original_program_time = 26*7*3
            boosters_only_vaccination_start = 1000000000 # aka never
            boosters_only_vaccination_duration =0

            boosting_group = 'none'
            second_boosters ={}
            second_boosters_doses =0 

            for year in [2021]:
                param_set = {'total_population':total_population,
                                'population_type': population_type,
                                'total_vaccination_rate':vaccination_rate,
                                'oldest_group_vax_coverage':oldest_group_coverage,
                                'original_vax_priority':delivery_dose_then_age,
                                'booster_fraction':past_booster_fraction,
                                'first_additional_vax_priority':first_boosters,
                                'second_additional_vax_priority':second_boosters,
                                'second_additional_doses_available':second_boosters_doses,
                                'boosting_group':boosting_group,
                                'boosters_only_vaccination_start':boosters_only_vaccination_start,
                                'boosters_only_vaccination_duration':boosters_only_vaccination_duration,
                                'year': year,
                                'age_bands' :age_bands_abm,
                                'folder': folder
                                }

                file_save_name = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".json"
                fullfilename = os.path.join(folder_path,file_save_name)

                # Serializing json 
                json_object = json.dumps(param_set, indent = 4)
                
                # Writing to sample.json
                with open(fullfilename, "w") as outfile:
                    outfile.write(json_object)

                number+=1 
