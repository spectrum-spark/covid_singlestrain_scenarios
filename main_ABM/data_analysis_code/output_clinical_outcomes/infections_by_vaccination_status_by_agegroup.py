# Gets the infections during 1.5-3 years by vaccination status (vaccinated or unvaccinated) for the high-coverage scenarios

import os
import pandas as pd
import json
import numpy as np
import csv


age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_R_file = ["[0,5)","[5,12)","[12,16)",'[16,20)', '[20,25)', '[25,30)', '[30,35)', '[35,40)', '[40,45)', '[45,50)', '[50,55)', '[55,60)', '[60,65)', '[65,70)', '[70,75)', '[75,80)', '[80,Inf]']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]


def get_vaccinated_unvaccinated_numbers_by_age_groups(folder_name,population_type,number):
    vaccination_filename =  os.path.join(folder_name,"abm_continuous_simulation_parameters_" + population_type+ "_" + str(number)+".csv")

    vaccination_fullfilename = os.path.join(os.path.dirname(__file__),vaccination_filename)

    # answers_dict = {age_band:{'vaccinated':0,'unvaccinated':0} for age_band in age_bands_abm}
    answers_list = [[age_band,0,0] for age_band in age_bands_abm ]

    with open(vaccination_fullfilename ) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                # print(f'Column names are {", ".join(row)}')
                # age_band,num_people,max_vax,time_1,time_2,time_3,time_4,infection,infection_day
                pass
            else:
                age_band,num_people,max_vax,time_1,time_2,time_3,time_4,infection,infection_day = row 
                age_band = int(age_band) # numbers 1-17
                num_people = int(num_people)
                max_vax = int(max_vax)

                if max_vax==0:
                    answers_list[age_band-1][2]+= num_people
                else:
                    answers_list[age_band-1][1]+= num_people
    
    df = pd.DataFrame(answers_list,  columns=["age_band","vaccinated","unvaccinated"])

    # print(df)

    return df




original_program_time = 26*7*3
one_year = 52*7
max_days = 52*3*7 # 3 years 
days_list = list(range(original_program_time ,max_days))

TP_high = "1.95"

# annual boosting 1
param_list = [0,4,5,6] # 2.0 year boosting scenarios (for no boosting, and boosting to different groups)
boosting_time = original_program_time + 26*7 # 2.0 year boosting only

TP_list = ["1.05", "1.95"]
TP_type_list = ['TP_low','TP_high']


boosting_only_group =  ['none','5-15','65+','random']
boosting_group_names = {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'}

boosters_only_vaccination_start_list = [original_program_time + 26*7 ] # 2.0 year boosting only

for immune_escape_time in [original_program_time, original_program_time + 52*7]:

    folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_1_immune_escape_t" + str(immune_escape_time)))

    presim_parameters_folder  = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "presim_code","parameter_files_annual_boosting_1"))

    for population_type in ["older", "younger"]:

        for paramNum in param_list:

            presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
            presimfilename = os.path.join(presim_parameters_folder,presim_parameters)
            with open(presimfilename, "r") as f:
                presim_parameters = json.load(f)

            boosting_group = presim_parameters['boosting_group']
            sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

            if boosting_group=='none' or  boosting_time == sims_boosting_time:
                pass
            else:
                continue
            
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

            # get the number of vaccinated and unvaccinated individuals in the different age categories
            df_vaccinated_numbers = get_vaccinated_unvaccinated_numbers_by_age_groups(presim_parameters_folder,population_type,paramNum)

            for TP_type, TP_val in zip(TP_type_list,TP_list):
                print(f"immune escape starts {str(round(immune_escape_time/one_year,2))} (year)")
                if boosting_group=="none":
                    print("boosting starts: never")
                else:
                    print("boosting starts: "+str(round(vaccination_start/one_year,2))+" (year)")
                print(f"1st year vaccination coverage: {str(total_vaccination_rate*100)}%, transmission potential level: {TP_type}, scenario: {boosting_group_names[boosting_group]}, population type: {population_type}, population size: {total_population}")

                

                # open the R-output combined file
                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP_val
                print(filename)

                datafilename = filename + ".csv"

                data_file = os.path.join(folder, datafilename)

                if os.path.isfile(data_file):
                    pass
                else:
                    print(data_file)
                    print("This file ^ doesn't exist????")
                    continue

                pd_obj = pd.read_csv(data_file)
                # print(pd_obj)
                pd_obj = pd_obj[pd_obj['day'] >= original_program_time] # get the day >= 1.5 years
                pd_obj['vaccine'] = np.where(pd_obj['vaccine'] == 'Unvaccinated', 'Unvaccinated', 'Vaccinated') # collapse vaccine to either Unvaccinated or Vaccinated

                # currently includes asymptomatic infections too. Uncomment line below to include on symptomatic infections:
                # pd_obj = pd_obj[pd_obj['symptomatic'] == 1]

                # Collapse the day, etc, leaving only age bracket, vaccine and sim, with n summed 
                new_pd = pd_obj.groupby(['bracket','vaccine','sim'],as_index=False).n.sum()

                def age_band_relabelling(row):
                    age_index= age_bands_R_file.index(row['bracket'])
                    return age_bands_abm[age_index]
                
                new_pd['age_band'] = new_pd.apply(age_band_relabelling, axis=1)
                new_pd = new_pd.drop(['bracket'], axis=1)

                

                # vaccinated group

                vac_obj = new_pd[new_pd['vaccine'] =="Vaccinated"]
                vac_obj = vac_obj.drop(['vaccine','sim'], axis=1)
                
                new_pd_median = vac_obj.groupby(['age_band']).median().reset_index()
                new_pd_median.rename(columns={'n':'vaccinated_median'},inplace=True)
                

                new_pd_quantile = vac_obj.groupby(['age_band']).quantile(0.025).reset_index()
                new_pd_quantile.rename(columns={'n':'vaccinated_quantile0025'},inplace=True)

                new_pd_quantile2 = vac_obj.groupby(['age_band']).quantile(0.975).reset_index()
                new_pd_quantile2.rename(columns={'n':'vaccinated_quantile0975'},inplace=True)

                df_merged = df_vaccinated_numbers.merge(new_pd_median, on='age_band', how='outer')
                df_merged = df_merged.merge(new_pd_quantile, on='age_band', how='outer')
                df_merged = df_merged.merge(new_pd_quantile2, on='age_band', how='outer')
                

                # unvaccinated group
                vac_obj = new_pd[new_pd['vaccine'] =="Unvaccinated"]
                vac_obj = vac_obj.drop(['vaccine','sim'], axis=1)
                
                new_pd_median = vac_obj.groupby(['age_band']).median().reset_index()
                
                new_pd_median.rename(columns={'n':'unvaccinated_median'},inplace=True)
                

                new_pd_quantile = vac_obj.groupby(['age_band']).quantile(0.025).reset_index()
                new_pd_quantile.rename(columns={'n':'unvaccinated_quantile0025'},inplace=True)

                new_pd_quantile2 = vac_obj.groupby(['age_band']).quantile(0.975).reset_index()
                new_pd_quantile2.rename(columns={'n':'unvaccinated_quantile0975'},inplace=True)

                df_merged = df_merged.merge(new_pd_median, on='age_band', how='outer')
                df_merged = df_merged.merge(new_pd_quantile, on='age_band', how='outer')
                df_merged = df_merged.merge(new_pd_quantile2, on='age_band', how='outer')
                

                # add in the percentage version as formatted text
                def formatted_percentage_vaccinated(row):
                    if row['vaccinated']!=0:
                        return f"\\num{{{round(row['vaccinated_median']/row['vaccinated']*100,1)}}}\\% (\\num{{{round(row['vaccinated_quantile0025']/row['vaccinated']*100,1)}}}\\%, \\num{{{round(row['vaccinated_quantile0975']/row['vaccinated']*100,1)}}}\\%)"
                    else:
                        return 0
                def formatted_percentage_unvaccinated(row):
                    return f"\\num{{{round(row['unvaccinated_median']/row['unvaccinated']*100,1)}}}\\% (\\num{{{round(row['unvaccinated_quantile0025']/row['unvaccinated']*100,1)}}}\\%, \\num{{{round(row['unvaccinated_quantile0975']/row['unvaccinated']*100,1)}}}\\%)"
                
                df_merged['vaccinated_infections'] = df_merged.apply(formatted_percentage_vaccinated, axis=1)
                df_merged['unvaccinated_infections'] = df_merged.apply(formatted_percentage_unvaccinated, axis=1)

                print(df_merged.to_string()) # NOTE THAT ALL RESULTS JUST PRINT

                # df_merged.to_csv()

                