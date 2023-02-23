import os
import csv
import json
import pandas as pd
import numpy as np

###########################################################################################
age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]
days_per_stage = 7*26 # 26 weeks
TP_list = [ "1.95"]
TP_high = ["1.95"]
TP_reduced_list =  [TP_high]
TP_type_list = ['TP_high']


SIM_NUMBER = 100

first_exposure_time =225
max_days = 52*3*7 # 3 years 

original_program_time = 26*7*3
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

age_bands_clinical =  [0,10,20,30,40,50,60,70,80]
age_bands_clinical_names =  ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]



components_clinical = ["daily_total_infections", "daily_symptomatic_infections","daily_admissions","ward_occupancy","daily_ICU_admissions","ICU_occupancy","daily_deaths"]
###########################################################################################

vaccination_coverage_wanted = 0.8

immune_escape_times = [original_program_time, original_program_time + 52*7] 

scenario = "high risk boosting"
boosting_starts = 637

###########################################################################################
# presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'

days_list = [ list(range(original_program_time ,max_days)) ]#, list(range(0,max_days))]
days_list_name = ["_1.5-3years"]#,""]

for quantile_val in [0.025,0.975]:

    header = ['population size', 'population type', 'scenario','1st year vaccination coverage','transmission potential level','boosting starts','immune escape starts', 'time period (days inclusive)', "total_quantile_"+str(quantile_val)+"_infections_all_ages", "total_quantile_"+str(quantile_val)+"_symptomatic_infections_all_ages","total_quantile_"+str(quantile_val)+"_admissions_all_ages","total_quantile_"+str(quantile_val)+"_ward_occupancy_all_ages","total_quantile_"+str(quantile_val)+"_ICU_admissions_all_ages","total_quantile_"+str(quantile_val)+"_ICU_occupancy_all_ages","total_quantile_"+str(quantile_val)+"_deaths_ages_all_ages"]

    for age_range in age_bands_clinical_names:
        header.append("total_quantile_"+str(quantile_val)+"_deaths_ages_"+age_range)

    print(header)

    for days_all, days_name in zip(days_list,days_list_name):

        quantile_output_file_name =  "many_boosters_high_coverage_quantile_"+str(quantile_val)+"_clinical_outcomes_totals"+days_name+".csv"
        iterated_output_file_name = "many_boosters_high_coverage_ALL_clinical_outcomes_totals"+days_name+".csv"

        quantile_full_output_file_name = '/scratch/cm37/tpl/'+quantile_output_file_name 
        iterated_full_output_file_name = '/scratch/cm37/tpl/'+iterated_output_file_name


        mega_DF_list_quantile = []
        mega_DF_list_iterated = []

        for TP_type, TP_val in zip(TP_type_list,TP_list):

            for population_type in ["older","younger"]:

                

                for immune_escape_time in immune_escape_times:
                    folder = "/scratch/cm37/tpl/annual_boosting_2_immune_escape_t" + str(immune_escape_time) +"_outputs/"

                    total_population =100000
                    total_vaccination_rate = 0.8
                    vaccination_start = boosting_starts

                    

                    filename = "abm_continuous_simulation_parameters_"+population_type+"_SOCRATES_TP"+TP_val

                    clinical_filename = "_full_outcomes_dataframe.csv"
                    clinical_file = os.path.join(folder,filename,clinical_filename)

                    if os.path.isfile(clinical_file):
                        pass
                    else:
                        print(clinical_file +" DOES NOT EXIST!")
                        continue


                    clinical_pd_obj = pd.read_csv(clinical_file)

                    clinical_pd_obj = clinical_pd_obj[clinical_pd_obj['day'].isin(days_all)]

                    clinical_pd_obj = clinical_pd_obj.drop('day', axis=1)

                    clinical_pd_obj = clinical_pd_obj.groupby(['age','iteration']).agg({'daily_total_infections': "sum",'daily_symptomatic_infections':"sum",'daily_admissions':"sum",'ward_occupancy':'sum','daily_ICU_admissions':'sum','ICU_occupancy':'sum','daily_deaths':'sum'}).reset_index()

                    # for all the others by individual:

                    simplified_clinical_pd = clinical_pd_obj.groupby(['iteration']).agg({'daily_total_infections': "sum",'daily_symptomatic_infections':"sum",'daily_admissions':"sum",'ward_occupancy':'sum','daily_ICU_admissions':'sum','ICU_occupancy':'sum','daily_deaths':'sum'}).reset_index() # these should now be all ages

                    # [... 'time period (days inclusive)', "total_quantile_infections_all_ages", "total_quantile_symptomatic_infections_all_ages","total_quantile_admissions_all_ages","total_quantile_ward_occupancy_all_ages","total_quantile_ICU_admissions_all_ages","total_quantile_ICU_occupancy_all_ages"]

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
                    iterated_clinical_DF.insert(0,'boosting starts',str(round(vaccination_start/one_year,2))+" (year)")
                    iterated_clinical_DF.insert(0,'transmission potential level',TP_type)
                    iterated_clinical_DF.insert(0,'1st year vaccination coverage',str(total_vaccination_rate*100)+"%")
                    iterated_clinical_DF.insert(0,'scenario',scenario)
                    iterated_clinical_DF.insert(0,'population type',population_type)
                    iterated_clinical_DF.insert(0,'population size',total_population)

                    print(list(iterated_clinical_DF.columns))

                    mega_DF_list_iterated.append(iterated_clinical_DF)


                    # mega_DF_list_quantile = []
                    combined_clinical_DF = iterated_clinical_DF.drop('iteration',axis=1) 

                    combined_columns = list(combined_clinical_DF.columns)
                    print("combined_columns:", combined_columns )

                    combined_clinical_DF = combined_clinical_DF.groupby(['population size', 'population type', 'scenario','1st year vaccination coverage','transmission potential level','boosting starts','immune escape starts', 'time period']).quantile(quantile_val).reset_index()

                
                    print(combined_clinical_DF)


                    old_columns_to_rename = [ 'total_infections_all_ages', 'total_symptomatic_infections_all_ages', 'total_admissions_all_ages', 'total_ward_occupancy_all_ages', 'total_ICU_admissions_all_ages', 'total_ICU_occupancy_all_ages', 'total_deaths_all_ages', 'total_deaths_ages_0-9', 'total_deaths_ages_10-19', 'total_deaths_ages_20-29', 'total_deaths_ages_30-39', 'total_deaths_ages_40-49', 'total_deaths_ages_50-59', 'total_deaths_ages_60-69', 'total_deaths_ages_70-79', 'total_deaths_ages_80+']
                    new_names =["total_quantile_"+str(quantile_val)+"_infections_all_ages", "total_quantile_"+str(quantile_val)+"_symptomatic_infections_all_ages","total_quantile_"+str(quantile_val)+"_admissions_all_ages","total_quantile_"+str(quantile_val)+"_ward_occupancy_all_ages","total_quantile_"+str(quantile_val)+"_ICU_admissions_all_ages","total_quantile_"+str(quantile_val)+"_ICU_occupancy_all_ages","total_quantile_"+str(quantile_val)+"_deaths_ages_all_ages"]

                    for age_range in age_bands_clinical_names:
                        new_names.append("total_quantile_"+str(quantile_val)+"_deaths_ages_"+age_range)
                    

                    combined_clinical_DF.rename(columns = {old_columns_to_rename[i]:new_names[i] for i in range(len(old_columns_to_rename))}, inplace = True)

                    print(combined_clinical_DF.head())
                    print("list(combined_clinical_DF.columns):",list(combined_clinical_DF.columns))

                    mega_DF_list_quantile.append(combined_clinical_DF)

                                

        # mega_DF_iterated = pd.concat(mega_DF_list_iterated)

        # mega_DF_iterated.to_csv(iterated_full_output_file_name ,index=False)

        mega_DF_quantile = pd.concat(mega_DF_list_quantile)

        mega_DF_quantile.to_csv(quantile_full_output_file_name ,index=False)
