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
age_categories = ['[0,5)','[5,12)', '[12,16)', '[16,20)', '[20,25)', '[25,30)', '[30,35)',
    '[35,40)', '[40,45)', '[45,50)', '[50,55)', '[55,60)',
    '[60,65)', '[65,70)', '[70,75)', '[75,80)', '[80,Inf]']
age_bands = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']


days_per_stage = 7*26 # 26 weeks

time_split = 450
days_before = list(range(0,time_split))
days_after = list(range(time_split,650))
R0_ratio= 1.1131953802735288


max_days = 650 #550 #646
date_values = list(range(0,max_days+1,10))
date_names = [str(x) for x in date_values]

# date_values = [363,393,424,454,485,516,546,577,607,638]
# date_names = ["April","May","June","July","Aug","Sept","Oct","Nov","Dec","Jan"]
# date_values = [363,393,424,454,485,516,546]
# date_names = ["April","May","June","July","Aug","Sept","Oct"]

days = list(range(0,max_days+1))
# days = list(range(350,545))
xlim_values= [0,max_days]
max_infections=5000 # 2000
num_infected_per_age_group = 6000

def TP_vs_total_avoided_infection(population_type_list = ["younger","older"]):
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    # first, some plotting to get some fake legends...
    legend_points = []

    for population_type in population_type_list :
        if population_type=="younger":
            legend_points.append(ax.scatter(-100000,-100000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-100000,-100000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-100000,-100000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        if population_type=="older":
            legend_points.append(ax.scatter(-100000,-100000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-100000,-100000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-100000,-100000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

        for TP in TP_list:
            

            # no vax 
            no_vax_filename = "abm_continuous_simulation_parameters_"+population_type+"_1_SOCRATES_TP"+TP
            no_vax_presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_1.json"
            no_vax_presimfilename = os.path.join(no_vax_presim_parameters_folder,no_vax_presim_parameters)
            with open(no_vax_presimfilename, "r") as f:
                presim_parameters = json.load(f)
            # total_population = presim_parameters["total_population"]
            # population_type = presim_parameters["population_type"]

            no_vax_data_file = os.path.join(no_vax_folder, no_vax_filename + ".csv")
            no_vax_pd_obj = pd.read_csv(no_vax_data_file)

            no_vax_new_pd = no_vax_pd_obj.groupby(['day','sim'],as_index=False).n.sum()
            no_vax_df = no_vax_new_pd.pivot(index='day', columns='sim', values='n')
            no_vax_df_dict = no_vax_df.to_dict()
            no_vax_infections_per_sim_before = []
            no_vax_infections_per_sim_after = []
            no_vax_infections_per_sim = []

            for simnum in no_vax_df_dict.keys():
                no_vax_infections_over_time = no_vax_df_dict[simnum]
                no_vax_total_infections_before = sum(list_conversion_nans(no_vax_infections_over_time, days_before))
                no_vax_infections_per_sim_before.append(no_vax_total_infections_before)
                

                no_vax_total_infections_after = sum(list_conversion_nans(no_vax_infections_over_time, days_after))
                no_vax_infections_per_sim_after.append(no_vax_total_infections_after)

                no_vax_infections_per_sim.append(no_vax_total_infections_before+no_vax_total_infections_after)

            for paramNum in population_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if population_type == "younger":
                    if total_vaccination_rate == 0.2:
                        colour = 'lightskyblue'
                    elif total_vaccination_rate == 0.5:
                        colour = 'dodgerblue'
                    elif total_vaccination_rate == 0.8:
                        colour = 'navy'
                else:
                    if total_vaccination_rate == 0.2:
                        colour = 'salmon'
                    elif total_vaccination_rate == 0.5:
                        colour = 'red'
                    elif total_vaccination_rate == 0.8:
                        colour = 'firebrick'

                if booster_fraction == 0.5:
                    continue
                elif booster_fraction ==0.8:
                    marker = "o"
                
                # info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP

                if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                    info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                else:
                    info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))
                
                datafilename = filename + ".csv"
                data_file = os.path.join(folder, datafilename)
                pd_obj = pd.read_csv(data_file)

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')
                df_dict = df.to_dict()
                infections_per_sim_before = []
                infections_per_sim_after = []
                infections_per_sim = []

                scale = 40
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)
                    

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    infections_per_sim.append(total_infections_before+total_infections_after)
                
                total_avoided_infections_pairwise = []
                for inf_i in infections_per_sim:
                    for inf_j in no_vax_infections_per_sim:
                        avoided_difference = inf_j - inf_i
                        total_avoided_infections_pairwise.append(avoided_difference)
                TP_x = [float(TP)]*len(total_avoided_infections_pairwise)
                ax.scatter( TP_x, total_avoided_infections_pairwise,color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')

                # percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                # percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]
                # ax.scatter( percent_infected_before, percent_infected_after,color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


    ax.set_xlim([0.8,2.1])
    ax.set_ylim([-10000,120000])
    
    # ax.set_xlim([15,85])
    # ax.set_ylim([-1,60])


    # y_ticks = [0,10,20,30,40,50,60]
    # ax.set_yticks(y_ticks)
    # ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

    # x_ticks = [20,30,40,50,60,70,80]
    # ax.set_xticks(x_ticks)
    # ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    # ax.set_aspect('equal')
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray')
    # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)


    if len(population_type_list)==2:
        ax.legend(legend_points[:3], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.47, 1), loc=1)
        leg = Legend(ax,legend_points[3:], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.47, 0.8), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points, ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.47, 1), loc=1)

    ax.set_ylabel('total avoided infection numbers')
    
    ax.set_xlabel('transmission potential (R0)')
    
    

    # xticks = [15,20,30,40,50,60,70,80,85]
    # for x0, x1 in zip(xticks[::2], xticks[1::2]):
    #     plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]   

    plt.savefig(os.path.join(folder, "avoided_diffs_TP_vs_total_avoided_infections_" + addition+ ".png") , bbox_inches='tight')
    plt.close()


TP_list = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_rerun_outputs")
no_vax_folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_no_vax_outputs")
population_list = [1,2,3,4,5,6]
no_vax_population_list = [1]
presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files")
no_vax_presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files_no_vax")
SIM_NUMBER = 10
no_vax_SIM_NUMBER = 5


TP_vs_total_avoided_infection(population_type_list = ["younger","older"])
TP_vs_total_avoided_infection(population_type_list = ["younger"])
TP_vs_total_avoided_infection(population_type_list = ["older"])