import os
import csv
import json
import pandas as pd
import numpy as np

age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]

first_exposure_time =225
second_exposure_time = 450
third_exposure_time = 675
max_days = 225*4 

param_list = list(range(6+1))
novax_index = 0
SIM_NUMBER = 50

TP_low = ["1.05"]
TP_high = ["1.95"]

boosters_only_vaccination_start_list = [-1,third_exposure_time+14]
third_vaccination_type_list = ["no further vaccination", "reactive (delayed) vaccination"]
third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"]

vaccination_coverages_wanted = [0,0.2,0.5, 0.8]

days_all = list(range(0,max_days))

# days_wave_1 = list(range(0,second_exposure_time))
# days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
# days_wave_3 = list(range(third_exposure_time,max_days))

# age_bands_clinical =  [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80]
age_bands_clinical =  [0,10,20,30,40,50,60,70,80]
age_bands_clinical_names =  ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]


components_clinical = ["daily_total_infections", "daily_symptomatic_infections","daily_admissions","ward_occupancy","daily_ICU_admissions","ICU_occupancy","daily_deaths"]

total_population_mil_list = [0.1, 0.5,10,100]

for total_population_mil in  [0.1, 0.5]:

    mean_output_file_name = "mean_clinical_outcomes_totals_"+ str(total_population_mil) +"mil.csv"
    iterated_output_file_name = "ALL_clinical_outcomes_totals_"+ str(total_population_mil) +"mil.csv"

    mean_full_output_file_name = '/scratch/cm37/tpl/'+mean_output_file_name 
    iterated_full_output_file_name = '/scratch/cm37/tpl/'+iterated_output_file_name

    if total_population_mil==0.1:
        presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_reduced/'
        folder_start_wave_2='/scratch/cm37/tpl/reduced_cont_intros_covid_BA1_BA45_wave_start_2_outputs/'
        folder_start_wave_3= '/scratch/cm37/tpl/reduced_cont_intros_covid_BA1_BA45_wave_start_3_outputs/'
    else:
        presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_expanded_pop_sizes/'
        folder_start_wave_2='/scratch/cm37/tpl/reduced_cont_intros_covid_BA1_BA45_wave_start_2_'+str(total_population_mil) +'mil_outputs/'
        folder_start_wave_3= '/scratch/cm37/tpl/reduced_cont_intros_covid_BA1_BA45_wave_start_3_'+str(total_population_mil) +'mil_outputs/'


    ####################################################

    wavestart_list =  ['start_wave_2','start_wave_3']
    folder_start_list = [folder_start_wave_2,folder_start_wave_3]
    presim_parameters_folder_start_list = [presim_parameters_folder,presim_parameters_folder]

    TP_reduced_list =  [TP_low, TP_high]
    TP_type_list = ['TP_low','TP_high']

    header = ['population size', 'population type','first year vaccination coverage','third wave vaccination type','transmission potential level','immune escape starts in wave', 'time period (days inclusive)', "total_mean_infections_all_ages", "total_mean_symptomatic_infections_all_ages","total_mean_admissions_all_ages","total_mean_ward_occupancy_all_ages","total_mean_ICU_admissions_all_ages","total_mean_ICU_occupancy_all_ages","total_mean_deaths_ages_all_ages"]

    for age_range in age_bands_clinical_names:
        header.append("total_mean_deaths_ages_"+age_range)

    print(header)


    

    mega_DF_list_mean = []
    mega_DF_list_iterated = []

    for population_type in ["younger","older"]:
        for wavestart, folder_start, presim_parameters_folder_start in zip(wavestart_list,folder_start_list,presim_parameters_folder_start_list):
            for TP_type, local_TP_list in zip(TP_type_list,TP_reduced_list):
                for paramNum in param_list:
                    if total_population_mil==0.1:
                        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                    else:
                        presim_parameters = "simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(paramNum)+".json"

                    presimfilename = os.path.join(presim_parameters_folder_start,presim_parameters)

                    with open(presimfilename, "r") as f:
                        presim_parameters = json.load(f)
                    total_population = presim_parameters["total_population"]
                    population_type = presim_parameters["population_type"]
                    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                    booster_fraction = presim_parameters["booster_fraction"]

                    if booster_fraction == 0.5:
                        continue

                    boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                    third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(boosters_only_vaccination_start)]

                    list_of_clinical_dfs = []

                    for TP in local_TP_list: # a list of one, lol
                        if total_population_mil==0.1:
                            filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                        else:
                            filename =  "simulation_parameters_" + str(total_population_mil) +"mil_" + population_type+ "_" + str(paramNum)+"_SOCRATES_TP"+TP

                        clinical_filename = "_full_outcomes_dataframe.csv"
                        clinical_file = os.path.join(folder_start,filename,clinical_filename)

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

                        # ['population size', 'population type','first year vaccination coverage','third wave vaccination type','transmission potential level','immune escape starts in wave', 'time period (days inclusive)', "total_mean_infections_all_ages", "total_mean_symptomatic_infections_all_ages","total_mean_admissions_all_ages","total_mean_ward_occupancy_all_ages","total_mean_ICU_admissions_all_ages","total_mean_ICU_occupancy_all_ages"]

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
                        
                        list_of_clinical_dfs.append(simplified_clinical_pd)
                    
                    iterated_clinical_DF = pd.concat(list_of_clinical_dfs)
                    print(list(iterated_clinical_DF.columns))

                    


                    # ['population size', 'population type','first year vaccination coverage','third wave vaccination type','transmission potential level','immune escape starts in wave', 'time period (days inclusive)'

                    iterated_clinical_DF.insert(0,'time period',str(days_all[0])+"-"+str(days_all[-1]))
                    iterated_clinical_DF.insert(0,'immune escape starts in wave',wavestart)
                    iterated_clinical_DF.insert(0,'transmission potential level',TP_type)
                    iterated_clinical_DF.insert(0,'third wave vaccination type',third_vaccination_type)
                    iterated_clinical_DF.insert(0,'first year vaccination coverage',total_vaccination_rate)
                    iterated_clinical_DF.insert(0,'population type',population_type)
                    iterated_clinical_DF.insert(0,'population size',total_population)

                    print(list(iterated_clinical_DF.columns))

                    mega_DF_list_iterated.append(iterated_clinical_DF)


                    # mega_DF_list_mean = []
                    combined_clinical_DF = iterated_clinical_DF.drop('iteration',axis=1) 

                    combined_columns = list(combined_clinical_DF.columns)
                    print("combined_columns:", combined_columns )

                    combined_clinical_DF = combined_clinical_DF.groupby(['population size','population type','first year vaccination coverage','third wave vaccination type','transmission potential level','immune escape starts in wave','time period']).mean().reset_index()

                    # combined_clinical_DF = combined_clinical_DF.agg({column:'mean' for column in combined_columns})
                    print(combined_clinical_DF)

                    # 'population size', 'population type', 'first year vaccination coverage', 'third wave vaccination type', 'transmission potential level', 'immune escape starts in wave', 'time period',

                    old_columns_to_rename = [ 'total_infections_all_ages', 'total_symptomatic_infections_all_ages', 'total_admissions_all_ages', 'total_ward_occupancy_all_ages', 'total_ICU_admissions_all_ages', 'total_ICU_occupancy_all_ages', 'total_deaths_all_ages', 'total_deaths_ages_0-9', 'total_deaths_ages_10-19', 'total_deaths_ages_20-29', 'total_deaths_ages_30-39', 'total_deaths_ages_40-49', 'total_deaths_ages_50-59', 'total_deaths_ages_60-69', 'total_deaths_ages_70-79', 'total_deaths_ages_80+']
                    new_names =["total_mean_infections_all_ages", "total_mean_symptomatic_infections_all_ages","total_mean_admissions_all_ages","total_mean_ward_occupancy_all_ages","total_mean_ICU_admissions_all_ages","total_mean_ICU_occupancy_all_ages","total_mean_deaths_ages_all_ages"]

                    for age_range in age_bands_clinical_names:
                        new_names.append("total_mean_deaths_ages_"+age_range)
                    

                    combined_clinical_DF.rename(columns = {old_columns_to_rename[i]:new_names[i] for i in range(len(old_columns_to_rename))}, inplace = True)

                    print(combined_clinical_DF.head())
                    print("list(combined_clinical_DF.columns):",list(combined_clinical_DF.columns))

                    mega_DF_list_mean.append(combined_clinical_DF)

                    

    # row = [population_type,total_vaccination_rate, third_vaccination_type, ]
    # writer.writerow(row)


    mega_DF_iterated = pd.concat(mega_DF_list_iterated)

    mega_DF_iterated.to_csv(iterated_full_output_file_name ,index=False)

    mega_DF_mean = pd.concat(mega_DF_list_mean)

    mega_DF_mean.to_csv(mean_full_output_file_name ,index=False)
