import os
import csv
import json
import pandas as pd
import numpy as np


output_file_name = "total_median_clinical_outcomes_over_time.csv"
full_output_file_name = '/scratch/cm37/tpl/'+output_file_name 

presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files/'
folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/'
presim_parameters_folder_start_wave_2=presim_parameters_folder
folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/'
presim_parameters_folder_start_wave_3=presim_parameters_folder

####################################################
age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]


first_exposure_time =225
second_exposure_time = 450
third_exposure_time = 675
max_days = 225*4 

param_list = list(range(10))
novax_index = 0
SIM_NUMBER = 10

TP_list = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
TP_low = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2"]
TP_mid = ["1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65"]
TP_high = ["1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
TP_segregated_list = [TP_low,TP_mid,TP_high]

boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]
third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"]

vaccination_coverages_wanted = [0,0.2,0.8]

days_wave_1 = list(range(0,second_exposure_time))
days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
days_wave_3 = list(range(third_exposure_time,max_days))
#####################################################

wavestart_list =  ['start_wave_2','start_wave_3']
folder_start_list = [folder_start_wave_2,folder_start_wave_3]
presim_parameters_folder_start_list = [presim_parameters_folder_start_wave_2,presim_parameters_folder_start_wave_3]

TP_reduced_list =  [TP_low, TP_high]
TP_type_list = ['TP_low','TP_high']

header = ['population type','first year vaccination coverage','third wave vaccination type','transmission potential level','immune escape starts in wave', 'time period (days inclusive)', "age","total_median_infections", "total_median_symptomatic_infections",	"total_median_admissions","total_median_ward_occupancy","total_median_ICU_admissions",	"total_median_ICU_occupancy","total_median_deaths"]

age_bands_clinical =  [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80]
components_clinical = ["daily_total_infections", "daily_symptomatic_infections","daily_admissions","ward_occupancy","daily_ICU_admissions","ICU_occupancy","daily_deaths"]

# with open(full_output_file_name,  'w', newline='') as f:
    # create the csv writer
    # writer = csv.writer(f)

    # write the header
    # writer.writerow(header)

mega_DF_list = []

for population_type in ["younger","older"]:
    for wavestart, folder_start, presim_parameters_folder_start in zip(wavestart_list,folder_start_list,presim_parameters_folder_start_list):
        for TP_type, local_TP_list in zip(TP_type_list,TP_reduced_list):
            for paramNum in param_list:
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"

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
                if total_vaccination_rate==0 or third_vaccination_type in third_vaccination_types_wanted:
                    pass 
                else:
                    continue

                if total_vaccination_rate not in vaccination_coverages_wanted:
                    continue
                else:
                    pass 
                
                # 'time period (days inclusive)', "age","total_median_infections", "total_median_symptomatic_infections",	"total_median_admissions","total_median_ward_occupancy","total_median_ICU_admissions",	"total_median_ICU_occupancy","total_median_deaths"

                wave_names = [str(days_wave_1[0])+"-"+str(days_wave_1[-1]),str(days_wave_2[0])+"-"+str(days_wave_2[-1]),str(days_wave_3[0])+"-"+str(days_wave_3[-1])]

                # collected_daily_values = {wave_names[0]:{},wave_names[1]:{},wave_names[2]:{}}
                # for wave in wave_names:
                #     for age in age_bands_clinical:
                #         collected_daily_values[wave][age] = {}
                #         for component in components_clinical:
                #             collected_daily_values[wave][age][component] = []

                list_of_clinical_dfs = []

                for TP in local_TP_list:
                    filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP

                    clinical_filename = "_full_outcomes_dataframe.csv"
                    clinical_file = os.path.join(folder_start,filename,clinical_filename)

                    if os.path.isfile(clinical_file):
                        pass
                    else:
                        print(clinical_file +" DOES NOT EXIST!")
                        continue


                    clinical_pd_obj = pd.read_csv(clinical_file)

                    def wave_time_period(value):
                        if value in days_wave_1:
                            return wave_names[0]
                        elif value in days_wave_2:
                            return  wave_names[1]
                        else: # there *may* actually a bug here, it should be days_in_wave_3 ; since the days *could* extend beyond 900 (max days, not sure)
                            return  wave_names[2]

                    clinical_pd_obj.insert(0,'time period','NA')
                    
                    clinical_pd_obj['time period'] = clinical_pd_obj['day'].map(wave_time_period)

                    clinical_pd_obj = clinical_pd_obj.drop('day', axis=1)

                    clinical_pd_obj = clinical_pd_obj.groupby(['time period','age','iteration']).agg({'daily_total_infections': "sum",'daily_symptomatic_infections':"sum",'daily_admissions':"sum",'ward_occupancy':'max','daily_ICU_admissions':'sum','ICU_occupancy':'max','daily_deaths':'sum'}).reset_index()

                    clinical_pd_obj.rename(columns = {'daily_total_infections':'total_infections', 'daily_symptomatic_infections':'total_symptomatic_infections','daily_admissions':'total_admissions',	'ward_occupancy':'maximum_ward_occupancy','daily_ICU_admissions':'total_ICU_admissions','ICU_occupancy':'maximum_ICU_occupancy','daily_deaths':'total_deaths'}, inplace = True)


                    	

                    # print(clinical_pd_obj.head())
                    print(list(clinical_pd_obj.columns))
                    
                    list_of_clinical_dfs.append(clinical_pd_obj)
                
                combined_clinical_DF = pd.concat(list_of_clinical_dfs)

                # print(combined_clinical_DF.head())
                print(list(combined_clinical_DF.columns))

                combined_clinical_DF = combined_clinical_DF.drop('iteration',axis=1)

                combined_clinical_DF = combined_clinical_DF.groupby(['time period','age']).median().reset_index()

                combined_clinical_DF.rename(columns = {'total_infections':'median_total_infections', 'total_symptomatic_infections':'median_total_symptomatic_infections','total_admissions':'median_total_admissions',	'maximum_ward_occupancy':'median_maximum_ward_occupancy','total_ICU_admissions':'median_total_ICU_admissions','maximum_ICU_occupancy':'median_maximum_ICU_occupancy','total_deaths':'median_total_deaths'}, inplace = True)

                # print(combined_clinical_DF.head())

                combined_clinical_DF.insert(0,'immune escape starts in wave',wavestart)
                combined_clinical_DF.insert(0,'transmission potential level',TP_type)
                combined_clinical_DF.insert(0,'third wave vaccination type',third_vaccination_type)
                combined_clinical_DF.insert(0,'first year vaccination coverage',total_vaccination_rate)
                combined_clinical_DF.insert(0,'population type',population_type)


                print(list(combined_clinical_DF.columns))

                    
                # ['population type','first year vaccination coverage','third wave vaccination type','transmission potential level','immune escape starts in wave', 'time period (days inclusive)', "age","total_median_infections", "total_median_symptomatic_infections",	"total_median_admissions","total_median_ward_occupancy","total_median_ICU_admissions",	"total_median_ICU_occupancy","total_median_deaths"]

                mega_DF_list.append(combined_clinical_DF)

# row = [population_type,total_vaccination_rate, third_vaccination_type, ]
# writer.writerow(row)


mega_DF = pd.concat(mega_DF_list)

mega_DF.to_csv(full_output_file_name,index=False)

