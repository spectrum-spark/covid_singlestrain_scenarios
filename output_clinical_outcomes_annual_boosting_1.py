import os
import csv
import json
import pandas as pd
import numpy as np

###########################################################################################
age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]
days_per_stage = 7*26 # 26 weeks
TP_list = ["1.05", "1.95"]
TP_low = ["1.05"]
TP_high = ["1.95"]
TP_reduced_list =  [TP_low, TP_high]
TP_type_list = ['TP_low','TP_high']


SIM_NUMBER = 100

first_exposure_time =225
max_days = 52*3*7 # 3 years 

original_program_time = 26*7*3
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

age_bands_clinical =  [0,10,20,30,40,50,60,70,80]
age_bands_clinical_names =  ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]

header = ['population size', 'population type', 'scenario','1st year vaccination coverage','transmission potential level','boosting starts','immune escape starts', 'time period (days inclusive)', "total_mean_infections_all_ages", "total_mean_symptomatic_infections_all_ages","total_mean_admissions_all_ages","total_mean_ward_occupancy_all_ages","total_mean_ICU_admissions_all_ages","total_mean_ICU_occupancy_all_ages","total_mean_deaths_ages_all_ages"]

for age_range in age_bands_clinical_names:
    header.append("total_mean_deaths_ages_"+age_range)

print(header)

components_clinical = ["daily_total_infections", "daily_symptomatic_infections","daily_admissions","ward_occupancy","daily_ICU_admissions","ICU_occupancy","daily_deaths"]
###########################################################################################

param_list = list(range(0,12+1))
boosters_only_vaccination_start_list = [original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7  , original_program_time + 52*7 ]

vaccination_coverage_wanted = 0.8


immune_escape_times = [original_program_time, original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7 , original_program_time + 52*7] 

boosting_only_group = ['none','5-15','65+','random']
boosting_group_names = {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'}

###########################################################################################
presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'

days_list = [ list(range(original_program_time ,max_days)) , list(range(0,max_days))]
days_list_name = ["_1.5-3years",""]

for days_all, days_name in zip(days_list,days_list_name):

    mean_output_file_name =  "high_coverage_mean_clinical_outcomes_totals"+days_name+".csv"
    iterated_output_file_name = "high_coverage_ALL_clinical_outcomes_totals"+days_name+".csv"

    mean_full_output_file_name = '/scratch/cm37/tpl/'+mean_output_file_name 
    iterated_full_output_file_name = '/scratch/cm37/tpl/'+iterated_output_file_name


    mega_DF_list_mean = []
    mega_DF_list_iterated = []

    for TP_type, TP_val in zip(TP_type_list,TP_list):

        for population_type in ["older","younger"]:

            for boosting_group_wanted in boosting_only_group: # getting the order how I like it

                for immune_escape_time in immune_escape_times:
                    folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"

                    if boosting_group_wanted!="none":
                        local_boosting_list = boosters_only_vaccination_start_list
                    else:
                        local_boosting_list = [100000000]

                    for boosting_time_wanted in local_boosting_list:

                        for paramNum in param_list:          
                            presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"

                            presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                            with open(presimfilename, "r") as f:
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

                            if (boosting_group_wanted=="none" and boosting_group=="none") or (boosting_group== boosting_group_wanted and vaccination_start ==boosting_time_wanted): # just getting the order right...
                                pass 
                            else:
                                continue 

                            filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP_val

                            clinical_filename = "_full_outcomes_dataframe.csv"
                            clinical_file = os.path.join(folder,filename,clinical_filename)

                            if os.path.isfile(clinical_file):
                                pass
                            else:
                                print(clinical_file +" DOES NOT EXIST!")
                                continue


                            clinical_pd_obj = pd.read_csv(clinical_file)

                            clinical_pd_obj = clinical_pd_obj[clinical_pd_obj['day'] <= days_all[-1]]

                            clinical_pd_obj = clinical_pd_obj.drop('day', axis=1)

                            clinical_pd_obj = clinical_pd_obj.groupby(['age','iteration']).agg({'daily_total_infections': "sum",'daily_symptomatic_infections':"sum",'daily_admissions':"sum",'ward_occupancy':'sum','daily_ICU_admissions':'sum','ICU_occupancy':'sum','daily_deaths':'sum'}).reset_index()

                            # for all the others by individual:

                            simplified_clinical_pd = clinical_pd_obj.groupby(['iteration']).agg({'daily_total_infections': "sum",'daily_symptomatic_infections':"sum",'daily_admissions':"sum",'ward_occupancy':'sum','daily_ICU_admissions':'sum','ICU_occupancy':'sum','daily_deaths':'sum'}).reset_index() # these should now be all ages

                            # [... 'time period (days inclusive)', "total_mean_infections_all_ages", "total_mean_symptomatic_infections_all_ages","total_mean_admissions_all_ages","total_mean_ward_occupancy_all_ages","total_mean_ICU_admissions_all_ages","total_mean_ICU_occupancy_all_ages"]

                            simplified_clinical_pd.rename(columns = {'daily_total_infections':'total_infections_all_ages',
                                                                    'daily_symptomatic_infections':'total_symptomatic_infections_all_ages',
                                                                    'daily_admissions':'total_admissions_all_ages',	
                                                                    'ward_occupancy':'total_ward_occupancy_all_ages',
                                                                    'daily_ICU_admissions':'total_ICU_admissions_all_ages',
                                                                    'ICU_occupancy':'total_ICU_occupancy_all_ages',
                                                                    'daily_deaths':'total_deaths_all_ages'}, 
                                                                    inplace = True)
                            # print(simplified_clinical_pd)
                            print(list(simplified_clinical_pd.columns))

                            # for deaths by iteration and age
                            deaths_only = clinical_pd_obj[['age', 'iteration','daily_deaths']]
                            print(deaths_only)

                            deaths_only = pd.pivot_table(deaths_only, index=['iteration'], columns=['age'],values="daily_deaths")
                            

                            
                            deaths_only.reset_index(inplace=True ) #  drop=False, 
                            column_order = ['iteration']
                            for age in age_bands_clinical:
                                column_order.append(str(age))
                            deaths_only.reindex(column_order, axis=1) 

                            rename_dict = {age_bands_clinical[i]:"total_deaths_ages_"+age_bands_clinical_names[i] for i in range(len(age_bands_clinical_names))}

                            print(rename_dict)

                            deaths_only.rename(columns=rename_dict,inplace = True)
                            
                            print(deaths_only)

                            simplified_clinical_pd =  pd.merge(simplified_clinical_pd, deaths_only, on='iteration', how='left')

                            print(simplified_clinical_pd )
                            print(list(simplified_clinical_pd.columns))
                            
                            iterated_clinical_DF = simplified_clinical_pd
                            
                            
                            # ['population size', 'population type', 'scenario','1st year vaccination coverage','transmission potential level','boosting starts','immune escape starts', 'time period (days inclusive)', ...

                            one_year = 52*7

                            iterated_clinical_DF.insert(0,'time period',str(round(days_all[0]/one_year,1))+" - "+str(round(days_all[-1]/one_year,1))+" years")
                            iterated_clinical_DF.insert(0,'immune escape starts',str(round(immune_escape_time/one_year,2))+" (year)")
                            if boosting_group_wanted=="none":
                                iterated_clinical_DF.insert(0,'boosting starts',"never")
                            else:
                                iterated_clinical_DF.insert(0,'boosting starts',str(round(vaccination_start/one_year,2))+" (year)")
                            iterated_clinical_DF.insert(0,'transmission potential level',TP_type)
                            iterated_clinical_DF.insert(0,'1st year vaccination coverage',str(total_vaccination_rate*100)+"%")
                            iterated_clinical_DF.insert(0,'scenario',boosting_group_names[boosting_group_wanted])
                            iterated_clinical_DF.insert(0,'population type',population_type)
                            iterated_clinical_DF.insert(0,'population size',total_population)

                            print(list(iterated_clinical_DF.columns))

                            mega_DF_list_iterated.append(iterated_clinical_DF)


                            # mega_DF_list_mean = []
                            combined_clinical_DF = iterated_clinical_DF.drop('iteration',axis=1) 

                            combined_columns = list(combined_clinical_DF.columns)
                            print("combined_columns:", combined_columns )

                            combined_clinical_DF = combined_clinical_DF.groupby(['population size', 'population type', 'scenario','1st year vaccination coverage','transmission potential level','boosting starts','immune escape starts', 'time period']).mean().reset_index()

                        
                            print(combined_clinical_DF)


                            old_columns_to_rename = [ 'total_infections_all_ages', 'total_symptomatic_infections_all_ages', 'total_admissions_all_ages', 'total_ward_occupancy_all_ages', 'total_ICU_admissions_all_ages', 'total_ICU_occupancy_all_ages', 'total_deaths_all_ages', 'total_deaths_ages_0-9', 'total_deaths_ages_10-19', 'total_deaths_ages_20-29', 'total_deaths_ages_30-39', 'total_deaths_ages_40-49', 'total_deaths_ages_50-59', 'total_deaths_ages_60-69', 'total_deaths_ages_70-79', 'total_deaths_ages_80+']
                            new_names =["total_mean_infections_all_ages", "total_mean_symptomatic_infections_all_ages","total_mean_admissions_all_ages","total_mean_ward_occupancy_all_ages","total_mean_ICU_admissions_all_ages","total_mean_ICU_occupancy_all_ages","total_mean_deaths_ages_all_ages"]

                            for age_range in age_bands_clinical_names:
                                new_names.append("total_mean_deaths_ages_"+age_range)
                            

                            combined_clinical_DF.rename(columns = {old_columns_to_rename[i]:new_names[i] for i in range(len(old_columns_to_rename))}, inplace = True)

                            print(combined_clinical_DF.head())
                            print("list(combined_clinical_DF.columns):",list(combined_clinical_DF.columns))

                            mega_DF_list_mean.append(combined_clinical_DF)

                            

    mega_DF_iterated = pd.concat(mega_DF_list_iterated)

    mega_DF_iterated.to_csv(iterated_full_output_file_name ,index=False)

    mega_DF_mean = pd.concat(mega_DF_list_mean)

    mega_DF_mean.to_csv(mean_full_output_file_name ,index=False)
