import json
import os


folder = "parameter_files_expanded_pop_sizes"
folder_path = os.path.join(os.path.dirname(__file__),folder)
if not os.path.exists(folder_path ):
  os.makedirs(folder_path )

# max_daily_allocation is a fraction of daily doses that can go to this group.
# dose 1 first (with oldest first), then dose 2 (with oldest first)

age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']

# primary doses

for total_population_mil in [0.5,10,100]:
    for population_type in ["younger","older"]:
        number = 0
        for vaccination_rate in [0, 0.2, 0.5,0.8]:
            delivery_dose_then_age = {0:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[1],'max_daily_allocation':1},
                            1:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[1],'max_daily_allocation':1},
                            2:{'ages':['65-69', '70-74', '75-79', '80+'],'dose_numbers':[2],'max_daily_allocation':1},
                            3:{'ages':["5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64'],'dose_numbers':[2],'max_daily_allocation':1}
                            }

            if vaccination_rate==0:
                oldest_group_coverage = 0
                delivery_dose_then_age = {0:{'ages':[],'dose_numbers':[],'max_daily_allocation':0}}
            elif vaccination_rate < 0.4: #low
                oldest_group_coverage = 0.8
            else:
                oldest_group_coverage = 0.95
            
            for booster_fraction in [0.8]:

                first_boosters = {0:{'ages':age_bands_abm[1:],'dose_numbers':[3],'max_daily_allocation':booster_fraction},
                                            1:{'ages':age_bands_abm[1:],'dose_numbers':[1],'max_daily_allocation':1},
                                            2:{'ages':age_bands_abm[1:],'dose_numbers':[2],'max_daily_allocation':1}}
                # booster doses are first regardless of age, with booster_fraction level of daily administered doses
                # after that, new 1st and 2nd doses are given fully if possible

                if vaccination_rate==0:
                    first_boosters  = {0:{'ages':[],'dose_numbers':[],'max_daily_allocation':0}}
                    second_boosters  = {0:{'ages':[],'dose_numbers':[],'max_daily_allocation':0}}

                    boosters_only_vaccination_start_list = [-1]
                    boosters_only_vaccination_duration_list = [-1]
                else:
                    third_exposure_date = 675
                    boosters_only_vaccination_start_list = [-1, third_exposure_date+14]
                    boosters_only_vaccination_duration_list = [-1, 5*30]

                for boosters_index in range(len(boosters_only_vaccination_start_list)):

                    if vaccination_rate!=0 and boosters_only_vaccination_start_list[boosters_index] == -1:
                        second_boosters  = {0:{'ages':[],'dose_numbers':[],'max_daily_allocation':0}} # aka a situation where no further vaccination is done
                    else:
                        second_boosters = {0:{'ages':age_bands_abm[1:],'dose_numbers':[3,4],'max_daily_allocation':1}}
                        # 80% of vaccinated people get another booster, no new primary doses are given out, and there is no prioritisation of booster number

                    for year in [2021]:
                        param_set = {'total_population':total_population_mil*10**6,
                                        'population_type': population_type,
                                        'total_vaccination_rate':vaccination_rate,
                                        'oldest_group_vax_coverage':oldest_group_coverage,
                                        'original_vax_priority':delivery_dose_then_age,
                                        'booster_fraction':booster_fraction,
                                        'first_additional_vax_priority':first_boosters,
                                        'second_additional_vax_priority':second_boosters,
                                        'boosters_only_vaccination_start':boosters_only_vaccination_start_list[boosters_index],
                                        'boosters_only_vaccination_duration':boosters_only_vaccination_duration_list[boosters_index],
                                        'year': year,
                                        'age_bands' :age_bands_abm,
                                        'folder': folder
                                        }

                        file_save_name = "simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(number)+".json"
                        fullfilename = os.path.join(folder_path,file_save_name)

                        # Serializing json 
                        json_object = json.dumps(param_set, indent = 4)
                        
                        # Writing to sample.json
                        with open(fullfilename, "w") as outfile:
                            outfile.write(json_object)

                        number+=1 

