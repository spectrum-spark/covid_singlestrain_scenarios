import os
import pandas as pd
import json
import scipy.io
import numpy as np
import csv
import matplotlib.font_manager
from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'sans-serif'})
# from matplotlib import rcParams
# rcParams['font.sans-serif'] = ['Bahnschrift Light']
from matplotlib.legend import Legend
import matplotlib.pyplot as plt
plt.switch_backend('agg')


def list_conversion_nans(dictionary, xvalues):
    new_list = []
    for x in xvalues:
        try:
            if np.isnan(dictionary[x]):
                new_list.append(0)
                
            else:
                new_list.append(dictionary[x])
        except:
            new_list.append(0)
    return new_list

def convert_to_array(inputstring):
    # inputstring = inputstring.replace('"','')
    if not bool(inputstring.strip()):
        return []
    else:
        string_array = inputstring.split(";")
        num_array = [float(x) for x in string_array]
        # print(num_array )
        return num_array

age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]

days_per_stage = 7*26 # 26 weeks

time_split = 450
days_before = list(range(0,time_split))
days_after = list(range(time_split,650))
R0_ratio= 1.1131953802735288


TP_list = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
population_list = list(range(1,6+1))
novax_population_list = [1]
SIM_NUMBER = 10


# CLUSTER NEW STRAIN
folder = '/scratch/cm37/tpl/covid_no_ttiq_450-2_ibm_4th_doses_newstrainBA45like_outputs/'
presim_parameters_folder  = '/fs02/cm37/prod/Le/covid-abm-presim/continuous_sim_param_files/'
novax_folder = '/scratch/cm37/tpl/covid_no_ttiq_450-2_ibm_4th_doses_newstrainBA45like_no_vax_outputs/'
novax_presim_parameters_folder =  '/fs02/cm37/prod/Le/covid-abm-presim/continuous_sim_param_files_no_vax/'


folder = os.path.join(os.path.dirname(__file__),"..","covid_no_ttiq_450-2_ibm_4th_doses_newstrainBA45like_outputs")
presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files")
novax_folder = os.path.join(os.path.dirname(__file__),"..","covid_no_ttiq_450-2_ibm_4th_doses_newstrainBA45like_no_vax_outputs")
novax_presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files_no_vax")



def clinical_pathways_investigation(ICU_or_death,OG="",population_type_list = ["younger","older"]):

    for population_type in population_type_list:

        print("No vaccination ==============================")

        for paramNum in novax_population_list:
            for TP in TP_list:



                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(novax_presim_parameters_folder,presim_parameters)

                print(filename)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                
                datafilename = filename + ".csv"
                data_file = os.path.join(novax_folder, datafilename)

                if os.path.isfile(data_file):
                    pass
                else:
                    continue

                pd_obj = pd.read_csv(data_file)

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')
                df_dict = df.to_dict()
                infections_per_sim_before = []
                infections_per_sim_after = []

                severe_disease_after = []

                # daily_deaths_after = []
                # daily_ICU_admissions_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
                clinical_pd_obj = pd.read_csv(clinical_file)

                scale = 40
                aug_num = 5
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    # infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    for aug in range(aug_num):
                        infections_per_sim_before.append(total_infections_before)
                        
                        new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==simnum*aug_num+aug) & (clinical_pd_obj['day']>time_split)]
                        
                        if ICU_or_death == 'death':
                            daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                            severe_disease_after.append(daily_deaths)

                            if (daily_deaths==0):
                                print("no deaths after!")
                                print("total infections after: ",total_infections_after)
                                print("number of ICU addmission:",sum(new_pd_ICU['daily_ICU_admissions'].to_list()))
                                old_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==simnum*aug_num+aug)]
                                old_daily_deaths = sum(old_pd_ICU['daily_deaths'].to_list())
                                print("number of deaths all: ",old_daily_deaths)

                        elif ICU_or_death =='ICU':
                            daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                            severe_disease_after.append(daily_ICU_admissions)

                    # daily_deaths_after.append(daily_deaths)
                    # daily_ICU_admissions_after.append(daily_ICU_admissions)
                #print(severe_disease_after)
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                

                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                # percent_daily_deaths_after = [x/total_population*100 for x in daily_deaths_after]
                # percent_daily_ICU_admissions_after = [x/total_population*100 for x in daily_ICU_admissions_after]
                

                # ax.scatter(percent_infected_before, severe_disease_after, color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)
                # max_y = max(max_y,max( severe_disease_after))
               
        print("With vaccination ==============================")

        for paramNum in population_list:
            for TP in TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                print(filename)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if booster_fraction == 0.5:
                    continue
                


                if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                    info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                else:
                    info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))
                
                datafilename = filename + ".csv"
                data_file = os.path.join(folder, datafilename)

                if os.path.isfile(data_file):
                    pass
                else:
                    continue

                pd_obj = pd.read_csv(data_file)

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')
                df_dict = df.to_dict()
                infections_per_sim_before = []
                infections_per_sim_after = []

                severe_disease_after = []

                # daily_deaths_after = []
                # daily_ICU_admissions_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
                clinical_pd_obj = pd.read_csv(clinical_file)

                scale = 40
                aug_num = 5
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    # infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    for aug in range(1,aug_num+1):
                        infections_per_sim_before.append(total_infections_before)
                        print((simnum-1)*aug_num+aug)

                        
                        new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day']>time_split)]
                        
                        

                        if ICU_or_death == 'death':
                            daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                            severe_disease_after.append(daily_deaths)


                            if (daily_deaths==0):
                                print("no deaths after!")
                                print(simnum*aug_num+aug)
                                print(clinical_pd_obj.loc[(clinical_pd_obj['iteration']==simnum*aug_num+aug)])
                                print("total infections after: ",total_infections_after)
                                old_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==simnum*aug_num+aug) & (clinical_pd_obj['day']<=time_split)]
                                old_daily_deaths = sum(old_pd_ICU['daily_deaths'].to_list())
                                print("number of deaths BEFORE: ",old_daily_deaths)
                                old_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==simnum*aug_num+aug)]
                                old_daily_deaths = sum(old_pd_ICU['daily_deaths'].to_list())
                                print("number of deaths all: ",old_daily_deaths)

                        elif ICU_or_death =='ICU':
                            daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                            severe_disease_after.append(daily_ICU_admissions)

                    # daily_deaths_after.append(daily_deaths)
                    # daily_ICU_admissions_after.append(daily_ICU_admissions)
                #print(severe_disease_after)
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                

                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                # percent_daily_deaths_after = [x/total_population*100 for x in daily_deaths_after]
                # percent_daily_ICU_admissions_after = [x/total_population*100 for x in daily_ICU_admissions_after]
                
                
                # ax.scatter(percent_infected_before, severe_disease_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                # max_y = max(max_y,max( severe_disease_after))
                
    #print(max_y)
    
       


# different second strain

# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"])
clinical_pathways_investigation('death',OG="",population_type_list = ["older"])


# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list =["younger"])
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["older"])

