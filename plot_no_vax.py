# clinical pathways 
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



def plot_infections_over_time_no_vax(population_type_list = ["younger","older"]):
    fig, ax = plt.subplots(1,1, figsize=(10,4)) # 16:9

    for population_type in population_type_list:

        for paramNum in population_list:
            for TP in TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                print(filename)

                datafilename = filename + ".csv"

                data_file = os.path.join(folder, datafilename)

                pd_obj = pd.read_csv(data_file)
                # print(pd_obj)


                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)


                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                # no vaccination and no booster fraction

                # if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                #     info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                # else:
                #     info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')

                # df.plot(legend=False)

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

                df_dict = df.to_dict()

                

                # colormap = plt.cm.get_cmap('inferno')
                #num_plots = len(list(df_dict.keys()))
                #ax.set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 1, num_plots))))

                #pre_infections = []


                if population_type == "younger":
                    colour = 'dodgerblue'
                else:
                    colour = 'red'

                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    infections_over_time_list = list_conversion_nans(infections_over_time, days)
                    ax.plot(days,infections_over_time_list,alpha=0.05,color=colour)#"black") # for poster: alpha = 0.025, alpha = 0.1 for the others
                    #pre_infections.append(sum(infections_over_time_list[:400]))

    ax.set_ylim([0,max_infections])
    ax.set_xlim([0,max_days])
    ax.grid(color='lightgray', linestyle='dashed')

    ax.set_xlabel('time (days)')
    ax.set_ylabel('number of infections')
    # ax.set_title('winter covid wave with ' + str(np.mean(pre_infections)) + " mean first-wave infections pre t=400")

    # ax.set_xticks(date_values)
    # ax.set_xticklabels(date_names)

    # ax.text(0.2,0.8,info_text,fontsize='large', multialignment ='left', ha='center', va='center', transform=ax.transAxes)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]                

    plt.savefig(os.path.join(folder, "no_vax_infections_over_time_" + addition +".png") , bbox_inches='tight')
    plt.close()




def plot_before_vs_after_infections_no_vax(population_type_list = ["younger","older"],hor_or_ver = "horizontal"):
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    legend_points = []
    marker= 'o'
    legend_list = []
    for population_type in population_type_list:
        if population_type == "younger":
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        legend_list.append(population_type+" population")

        for paramNum in population_list:
            for TP in TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                # total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                # booster_fraction = presim_parameters["booster_fraction"]

                if population_type == "younger":
                    colour = 'dodgerblue'
                else:
                    colour = 'red'

                # info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP

                # if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                #     info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                # else:
                #     info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))
                
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
                if hor_or_ver =="vertical":
                    ax.scatter(percent_infected_after, percent_infected_before, color=colour, s=scale, marker= marker, alpha=0.8, edgecolors='none')
                elif hor_or_ver=="horizontal":
                    ax.scatter(percent_infected_before,percent_infected_after,  color=colour, s=scale, marker= marker, alpha=0.8, edgecolors='none')
                else:
                    print("wrong hor_or_ver:",hor_or_ver)
                    exit(1)

    if hor_or_ver =="vertical":
        ax.set_ylim([15,85])
        ax.set_xlim([-1,60])
        x_ticks = [0,10,20,30,40,50,60]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])
        y_ticks = [20,30,40,50,60,70,80]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

        ax.legend(legend_points,legend_list,bbox_to_anchor=(1, 1), loc=1)

        ax.set_xlabel('near-future attack rate (t = 450 to 650)')
        ax.set_title('near-future attack rate (t = 450 to 650)')
        ax.set_ylabel('past attack rate (before t = 450)')
        ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
        ax.invert_yaxis()

        yticks = [15,20,30,40,50,60,70,80,85]
        for y0, y1 in zip(yticks[::2], yticks[1::2]):
            plt.axhspan(y0, y1, color='black', alpha=0.1, zorder=0)

    elif hor_or_ver=="horizontal":
        ax.set_xlim([15,85])
        ax.set_ylim([-1,60])
        y_ticks = [0,10,20,30,40,50,60]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y)+"\%" for y in y_ticks])
        x_ticks = [20,30,40,50,60,70,80]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        ax.legend(legend_points,legend_list,bbox_to_anchor=(0.47, 1), loc=1)

        ax.set_ylabel('near-future attack rate (t = 450 to 650)')
        #ax.set_title('past attack rate (before t = 450)')
        ax.set_xlabel('past attack rate (before t = 450)')
        #ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
        

        xticks = [15,20,30,40,50,60,70,80,85]
        for x0, x1 in zip(xticks[::2], xticks[1::2]):
            plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

    ax.set_aspect('equal')
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray')

    

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]     

    plt.savefig(os.path.join(folder, "no_vax_infections_vs_past_immunity_"+hor_or_ver+"_"+ addition+ ".png") , bbox_inches='tight') 
    plt.close()
        

TP_list = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_no_vax_outputs")
population_list = [1]
presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files_no_vax")
SIM_NUMBER = 5

plot_infections_over_time_no_vax(population_type_list = ["younger","older"])
plot_infections_over_time_no_vax(population_type_list = ["younger"])
plot_infections_over_time_no_vax(population_type_list = ["older"])

plot_before_vs_after_infections_no_vax(population_type_list = ["younger","older"],hor_or_ver = "horizontal")
plot_before_vs_after_infections_no_vax(population_type_list = ["younger"],hor_or_ver = "horizontal")
plot_before_vs_after_infections_no_vax(population_type_list = ["older"],hor_or_ver =  "horizontal")

plot_before_vs_after_infections_no_vax(population_type_list = ["younger","older"],hor_or_ver = "vertical")
plot_before_vs_after_infections_no_vax(population_type_list = ["younger"],hor_or_ver = "vertical")
plot_before_vs_after_infections_no_vax(population_type_list = ["older"],hor_or_ver = "vertical")