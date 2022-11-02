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

SAMOA_file_name = '/fs04/cm37/prod/Le/covid-abm/Samoa_attackrates.csv'


def plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],filter=False,aspect_ratio = 'equal'):
    if y_limits[1]>80:
        fig, ax = plt.subplots(1,1, figsize=(8,7.75)) # for the second strain
    else:
        fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    # 
    # first, some plotting to get some fake legends...
    legend_points = []
    marker='o'

    # legend_list = ["20\% vaccination coverage, younger population", "50\% vaccination coverage, younger population","80\% vaccination coverage, younger population","20\% vaccination coverage, older population", "50\% vaccination coverage, older population","80\% vaccination coverage, older population"]

    for population_type in population_type_list :
        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

        
        for paramNum in novax_population_list:
            for TP in TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(novax_presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]

                if population_type == "younger":
                    colour = 'white' # lightblue or paleturquoise
                    # outline='dodgerblue'
                    # colour ='lightblue'
                    outline ='lightskyblue'
                    
                    
                else:
                    colour = 'white'
                    # colour = 'pink'
                    outline='salmon'
                # outline='none'
                

                datafilename = filename + ".csv"
                data_file = os.path.join(novax_folder, datafilename)
                pd_obj = pd.read_csv(data_file)

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')
                df_dict = df.to_dict()
                infections_per_sim_before = []
                infections_per_sim_after = []

                scale = 40
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)
                
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]
                if not filter:
                    ax.scatter( percent_infected_before, percent_infected_after,color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)
                else:
                    percent_infected_before_filtered = []
                    percent_infected_after_filtered = []
                    for i in range(len(percent_infected_before)):
                        element = percent_infected_before[i]
                        if element>=20 and element<=80:
                            percent_infected_before_filtered.append(element)
                            percent_infected_after_filtered.append(percent_infected_after[i])
                    ax.scatter( percent_infected_before_filtered, percent_infected_after_filtered,color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)

        for paramNum in population_list:
            for TP in TP_list:

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

                scale = 40
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)
                
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]
                if not filter:
                    ax.scatter( percent_infected_before, percent_infected_after,color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                else:
                    percent_infected_before_filtered = []
                    percent_infected_after_filtered = []
                    for i in range(len(percent_infected_before)):
                        element = percent_infected_before[i]
                        if element>=20 and element<=80:
                            percent_infected_before_filtered.append(element)
                            percent_infected_after_filtered.append(percent_infected_after[i])
                    ax.scatter( percent_infected_before_filtered, percent_infected_after_filtered,color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')

    # SAMOA
    SAMOA_data_file = os.path.join(SAMOA_file_name)
    SAMOA_pd_obj = pd.read_csv(SAMOA_data_file) 

    SAMOA_pd_obj = SAMOA_pd_obj.reset_index()  # make sure indexes pair with number of rows
    colour = 'green'
    for index, row in SAMOA_pd_obj.iterrows():
        if row['AR_second']*100<20: # just removing outliers
            pass
        else:
            ax.scatter( row['AR_first']*100, row['AR_second']*100,color=colour, s=scale, marker= marker, alpha=0.8, edgecolors='none')




    
    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)

    y_ticks = list(range(0,max(y_limits)+1,10))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

    x_ticks = [20,30,40,50,60,70,80]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    ax.set_aspect(aspect_ratio)
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray')
    # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)


    if len(population_type_list)==2:
        ax.legend(legend_points[:4], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.47, 1), loc=1)
        leg = Legend(ax,legend_points[4:], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.47, 0.75), loc=1)
        ax.add_artist(leg)
    else:
        if max(y_limits)!=100:
            ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.47, 1), loc=1)
        else:
            ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.6, 1), loc=1)

    ax.set_ylabel('near-future attack rate (t = 450 to 650)')
    #ax.set_title('past attack rate (before t = 450)')
    ax.set_xlabel('past attack rate (before t = 450)')
    #ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    

    xticks = [15,20,30,40,50,60,70,80,85]
    for x0, x1 in zip(xticks[::2], xticks[1::2]):
        plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]   

    plt.savefig(os.path.join(folder, "SAMOA_with_novax_infections_past_immunity_combined_population_80booster_only_horizontal_" + addition+ ".png") , bbox_inches='tight')
    plt.close()




# different second strain

# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,100],x_limits=[19,81],filter=True)

# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],y_limits = [-1,100],x_limits=[19,81],filter=True)

# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,100],x_limits=[-1,100],filter=False)

plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,100],x_limits=[19,81],filter=True,aspect_ratio='auto')
