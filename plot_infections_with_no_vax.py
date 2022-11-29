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
import matplotlib.animation
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

# time_split = 450
# days_before = list(range(0,time_split))
# days_after = list(range(time_split,650))
R0_ratio= 1.1131953802735288


TP_list = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
TP_low = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2"]
TP_mid = ["1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65"]
TP_high = ["1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
TP_segregated_list = [TP_low,TP_mid,TP_high]

param_list = list(range(10))
novax_index = 0
SIM_NUMBER = 10

max_days = 225*4 
first_exposure_time =225
second_exposure_time = 450
third_exposure_time = 675

boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]

date_values = list(range(0,max_days+1,10))
date_names = [str(x) for x in date_values]

days = list(range(0,max_days+1))


def plot_combined_infections_over_time_80_booster(younger_or_older=["younger"],line_color="black"):
    
    max_infections=5000 

    fig, ax = plt.subplots(1,1, figsize=(10,4)) # 16:9

    legend_points = []
    marker='o'

    for population_type in younger_or_older:

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

        for paramNum in param_list:
            for TP in TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                print(filename)

                datafilename = filename + ".csv"

                data_file = os.path.join(folder, datafilename)

                if os.path.isfile(data_file):
                    pass
                else:
                    continue

                pd_obj = pd.read_csv(data_file)
                # print(pd_obj)
                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)

                # total_population = presim_parameters["total_population"]
                # population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if booster_fraction==0.5:
                    continue

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
                if line_color=="black":
                    plot_colour = "black"
                elif line_color=="coloured":
                    if population_type == "younger":
                        if total_vaccination_rate == 0.2:
                            plot_colour = 'lightskyblue'
                        elif total_vaccination_rate == 0.5:
                            plot_colour = 'dodgerblue'
                        elif total_vaccination_rate == 0.8:
                            plot_colour = 'navy'
                        elif total_vaccination_rate==0:
                            plot_colour = "white"
                    else:
                        if total_vaccination_rate == 0.2:
                            plot_colour = 'salmon'
                        elif total_vaccination_rate == 0.5:
                            plot_colour = 'red'
                        elif total_vaccination_rate == 0.8:
                            plot_colour = 'firebrick'
                        elif total_vaccination_rate==0:
                            plot_colour = "white"
                else:
                    plot_colour = "black"

                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    infections_over_time_list = list_conversion_nans(infections_over_time, days)
                    ax.plot(days,infections_over_time_list,alpha=0.1,color=plot_colour) 

    ax.set_ylim([0,max_infections])
    ax.set_xlim([0,max_days])
    ax.grid(color='gray', linestyle='dashed')

    ax.axvline(x =first_exposure_time, color = 'white')
    ax.axvline(x =second_exposure_time, color = 'white')
    ax.axvline(x =third_exposure_time, color = 'white')

    ax.set_facecolor('#3b3b3b')


    if len(younger_or_older)==2:
        ax.legend(legend_points[:4], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.28, 1), loc=1)
        leg = Legend(ax,legend_points[4:], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.28, 0.75), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=younger_or_older[0] +" population",bbox_to_anchor=(0.28, 1), loc=1)

    ax.set_xlabel('time (days)')
    ax.set_ylabel('number of infections')
    
    plt.savefig(os.path.join(folder, "Infections_over_time_"+"_".join(younger_or_older)+ ".png") , bbox_inches='tight')
    plt.close()


def plot_separated_infections_over_time(younger_or_older=["younger"]):
    
    max_infections=5000 
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    plot_save =["no_more_vax","early_vax","reactive_vax"]

    # TP_segregated_list = [TP_low,TP_mid,TP_high]
    

    for i_third_vax in range(len(third_vaccination_type_list)):
        third_vaccination_type_here = third_vaccination_type_list[i_third_vax]

        for local_TP_list in TP_segregated_list:

            fig, ax = plt.subplots(1,1, figsize=(10,4)) # 16:9

            legend_points = []
            marker='o'

            for population_type in younger_or_older:

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

                for paramNum in param_list:
                    for TP in local_TP_list:

                        
                        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                        presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                        with open(presimfilename, "r") as f:
                            presim_parameters = json.load(f)

                        # total_population = presim_parameters["total_population"]
                        # population_type = presim_parameters["population_type"]
                        total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                        booster_fraction = presim_parameters["booster_fraction"]

                        if booster_fraction==0.5:
                            continue

                        boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                        third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(boosters_only_vaccination_start)]
                        if total_vaccination_rate==0 or third_vaccination_type == third_vaccination_type_here:
                            pass 
                        else:
                            continue 
                        
                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
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

                        if population_type == "younger":
                            if total_vaccination_rate == 0.2:
                                plot_colour = 'lightskyblue'
                            elif total_vaccination_rate == 0.5:
                                plot_colour = 'dodgerblue'
                            elif total_vaccination_rate == 0.8:
                                plot_colour = 'navy'
                            elif total_vaccination_rate==0:
                                plot_colour = "white"
                        else:
                            if total_vaccination_rate == 0.2:
                                plot_colour = 'salmon'
                            elif total_vaccination_rate == 0.5:
                                plot_colour = 'red'
                            elif total_vaccination_rate == 0.8:
                                plot_colour = 'firebrick'
                            elif total_vaccination_rate==0:
                                plot_colour = "white"

                        for simnum in df_dict.keys():
                            infections_over_time = df_dict[simnum]
                            infections_over_time_list = list_conversion_nans(infections_over_time, days)
                            ax.plot(days,infections_over_time_list,alpha=1,color=plot_colour)  # alpha = 1

            ax.set_ylim([0,max_infections])
            ax.set_xlim([0,max_days])
            ax.grid(color='gray', linestyle='dashed')

            ax.axvline(x =first_exposure_time, color = 'white')
            ax.axvline(x =second_exposure_time, color = 'white')
            ax.axvline(x =third_exposure_time, color = 'white')

            ax.set_facecolor('#3b3b3b')


            if len(younger_or_older)==2:
                ax.legend(legend_points[:4], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.28, 1), loc=1)
                leg = Legend(ax,legend_points[4:], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.28, 0.75), loc=1)
                ax.add_artist(leg)
            else:
                leg = ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=younger_or_older[0] +" population",bbox_to_anchor=(0.28, 1), loc=1,facecolor='white', framealpha=1)
                leg._legend_box.align = "left"


            ax.set_xlabel('time (days)')
            ax.set_ylabel('number of infections')
            
            plt.savefig(os.path.join(folder, "separate_infections_over_time_"+"_".join(younger_or_older)+ "_"+plot_save[i_third_vax]+ "_maxTP_"+str(max(local_TP_list)) + ".png") , bbox_inches='tight')
            plt.close()



def plot_ribbon_infections_over_time(younger_or_older=["younger"]):
    
    max_infections=5000 
    local_days = list(range(first_exposure_time,max_days+1))
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    plot_save =["no_more_vax","early_vax","reactive_vax"]

    # TP_segregated_list = [TP_low,TP_mid,TP_high]
    

    for i_third_vax in range(len(third_vaccination_type_list)):
        third_vaccination_type_here = third_vaccination_type_list[i_third_vax]

        for local_TP_list in TP_segregated_list:

            fig, ax = plt.subplots(1,1, figsize=(10,4)) # 16:9

            legend_points = []
            marker='o'

            for population_type in younger_or_older:

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

                all_curves_over_local_days = {0:[], 0.2: [],0.5:[],0.8 :[]}
                

                for paramNum in param_list:


                    for TP in local_TP_list:

                        
                        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                        presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                        with open(presimfilename, "r") as f:
                            presim_parameters = json.load(f)

                        # total_population = presim_parameters["total_population"]
                        # population_type = presim_parameters["population_type"]
                        total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                        booster_fraction = presim_parameters["booster_fraction"]

                        if booster_fraction==0.5:
                            continue

                        boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                        third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(boosters_only_vaccination_start)]
                        if total_vaccination_rate==0 or third_vaccination_type == third_vaccination_type_here:
                            pass 
                        else:
                            continue 
                        
                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
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

                        

                        for simnum in df_dict.keys():
                            infections_over_time = df_dict[simnum]
                            infections_over_time_list = list_conversion_nans(infections_over_time, local_days)
                            all_curves_over_local_days[total_vaccination_rate].append(infections_over_time_list)

                            # ax.plot(local_days,infections_over_time_list,alpha=1,color=plot_colour)
                upper_ribbon = {'0':[], '0.2': [],'0.5':[],'0.8':[]} # for different vaccination coverages 
                lower_ribbon = {'0':[],'0.2': [],'0.5':[],'0.8':[]}
                median_line = {'0':[],'0.2': [],'0.5':[],'0.8':[]}

                for vax in [0,0.2,0.5,0.8]:
                    upper_ribbon[vax] = [max([all_curves_over_local_days[vax][simnum][i] for simnum in range(len(all_curves_over_local_days[vax]))]) for i in range(len(local_days))]
                    lower_ribbon[vax] = [min([all_curves_over_local_days[vax][simnum][i] for simnum in range(len(all_curves_over_local_days[vax]))]) for i in range(len(local_days))]
                    median_line[vax] = [np.median([all_curves_over_local_days[vax][simnum][i] for simnum in range(len(all_curves_over_local_days[vax]))]) for i in range(len(local_days))]
                for vax in [0,0.2,0.5,0.8]:
                    if population_type == "younger":
                        if vax == 0.2:
                            plot_colour = 'lightskyblue'
                        elif vax == 0.5:
                            plot_colour = 'dodgerblue'
                        elif vax == 0.8:
                            plot_colour = 'navy'
                        elif vax==0:
                            plot_colour = "white"
                    else:
                        if vax == 0.2:
                            plot_colour = 'salmon'
                        elif vax == 0.5:
                            plot_colour = 'red'
                        elif vax == 0.8:
                            plot_colour = 'firebrick'
                        elif vax==0:
                            plot_colour = "white"
                    ax.fill_between(local_days,upper_ribbon[vax],lower_ribbon[vax],facecolor=plot_colour,alpha=0.5)
                    # ax.plot(local_days,median_line[vax],color = plot_colour,linestyle='solid')
                for vax in [0,0.2,0.5,0.8]:
                    if population_type == "younger":
                        if vax == 0.2:
                            plot_colour = 'lightskyblue'
                        elif vax == 0.5:
                            plot_colour = 'dodgerblue'
                        elif vax == 0.8:
                            plot_colour = 'navy'
                        elif vax==0:
                            plot_colour = "white"
                    else:
                        if vax == 0.2:
                            plot_colour = 'salmon'
                        elif vax == 0.5:
                            plot_colour = 'red'
                        elif vax == 0.8:
                            plot_colour = 'firebrick'
                        elif vax==0:
                            plot_colour = "white"
                    # ax.fill_between(local_days,upper_ribbon[vax],lower_ribbon[vax],facecolor=plot_colour,alpha=0.5)
                    ax.plot(local_days,median_line[vax],color = plot_colour,linestyle='solid')



            ax.set_ylim([0,max_infections])
            ax.set_xlim([min(local_days),max_days])
            ax.grid(color='#878787', linestyle=(0, (5, 1)))

            ax.axvline(x =first_exposure_time, color = 'white')
            ax.axvline(x =second_exposure_time, color = 'white')
            ax.axvline(x =third_exposure_time, color = 'white')

            ax.set_facecolor('silver')


            if len(younger_or_older)==2:
                ax.legend(legend_points[:4], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.28, 1), loc=1)
                leg = Legend(ax,legend_points[4:], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.28, 0.75), loc=1)
                ax.add_artist(leg)
            else:
                leg = ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=younger_or_older[0] +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
                leg._legend_box.align = "left"


            ax.set_xlabel('time (days)')
            ax.set_ylabel('number of infections')
            
            plt.savefig(os.path.join(folder, "ribbon_infections_over_time_"+"_".join(younger_or_older)+ "_"+plot_save[i_third_vax]+ "_maxTP_"+str(max(local_TP_list)) + ".png") , bbox_inches='tight')
            plt.close()




def plot_violin_infections_over_time(younger_or_older=["younger"]):

    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    plot_save =["no_more_vax","early_vax","reactive_vax"]

    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days+1))

    # TP_segregated_list = [TP_low,TP_mid,TP_high]
    

    for i_third_vax in range(len(third_vaccination_type_list)):
        third_vaccination_type_here = third_vaccination_type_list[i_third_vax]

        for local_TP_list in TP_segregated_list:

            fig, ax = plt.subplots(1,1, figsize=(4,4)) # 16:9

            legend_points = []
            marker='o'
            

            for population_type in younger_or_older:

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

                all_attack_rates_wave_1 = {0:[], 0.2: [],0.5:[],0.8 :[]}
                all_attack_rates_wave_2 = {0:[], 0.2: [],0.5:[],0.8 :[]}
                all_attack_rates_wave_3 = {0:[], 0.2: [],0.5:[],0.8 :[]}

                for paramNum in param_list:
                    for TP in local_TP_list:

                        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                        presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                        with open(presimfilename, "r") as f:
                            presim_parameters = json.load(f)

                        total_population = presim_parameters["total_population"]
                        # population_type = presim_parameters["population_type"]
                        total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                        booster_fraction = presim_parameters["booster_fraction"]

                        if booster_fraction==0.5:
                            continue

                        boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                        third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(boosters_only_vaccination_start)]
                        if total_vaccination_rate==0 or third_vaccination_type == third_vaccination_type_here:
                            pass 
                        else:
                            continue 
                        
                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
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

                        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                        df = new_pd.pivot(index='day', columns='sim', values='n')

                        df_dict = df.to_dict()

                        infections_per_sim_wave_1 = []
                        infections_per_sim_wave_2 = []
                        infections_per_sim_wave_3 = []

                        

                        scale = 40
                        for simnum in df_dict.keys():
                            infections_over_time = df_dict[simnum]
                            total_infections_wave_1 = sum(list_conversion_nans(infections_over_time, days_wave_1))
                            infections_per_sim_wave_1.append(total_infections_wave_1)


                            total_infections_wave_2 = sum(list_conversion_nans(infections_over_time, days_wave_2))
                            infections_per_sim_wave_2.append(total_infections_wave_2)

                            total_infections_wave_3 = sum(list_conversion_nans(infections_over_time, days_wave_3))
                            infections_per_sim_wave_3.append(total_infections_wave_3)
                        
                        percent_infected_wave_1 = [x/total_population*100 for x in infections_per_sim_wave_1]
                        percent_infected_wave_2 = [x/total_population*100 for x in infections_per_sim_wave_2]
                        percent_infected_wave_3 = [x/total_population*100 for x in infections_per_sim_wave_3]

                        all_attack_rates_wave_1[total_vaccination_rate].extend(percent_infected_wave_1)
                        all_attack_rates_wave_2[total_vaccination_rate].extend(percent_infected_wave_2)
                        all_attack_rates_wave_3[total_vaccination_rate].extend(percent_infected_wave_3)

                
                
                median_line = {0:[],0.2: [],0.5:[],0.8:[]}

                for vax in [0,0.2,0.5,0.8]:
                    median_line[vax] = [np.median(all_attack_rates_wave_1[vax]),np.median(all_attack_rates_wave_2[vax]),np.median(all_attack_rates_wave_3[vax])]

                print(median_line)
                
                for vax in [0,0.2,0.5,0.8]:
                    outline = 'none'
                    if population_type == "younger":
                        if vax == 0.2:
                            plot_colour = 'lightskyblue'
                            outline= 'lightskyblue'
                        elif vax == 0.5:
                            plot_colour = 'dodgerblue'
                            outline = 'dodgerblue'
                        elif vax == 0.8:
                            plot_colour = 'navy'
                            outline = 'navy'
                        elif vax==0:
                            plot_colour = "white"
                            outline ='lightskyblue'
                    else:
                        if vax == 0.2:
                            plot_colour = 'salmon'
                            outline = 'salmon'
                        elif vax == 0.5:
                            plot_colour = 'red'
                            outline = 'red'
                        elif vax == 0.8:
                            plot_colour = 'firebrick'
                            outline = 'firebrick'
                        elif vax==0:
                            plot_colour = "white"
                            outline='salmon'
                    data_to_plot = [all_attack_rates_wave_1[vax],all_attack_rates_wave_2[vax],all_attack_rates_wave_3[vax]]
                    parts = ax.violinplot(data_to_plot, showmeans=False, showmedians=False, showextrema=False)
                    

                    for pc in parts['bodies']:
                        pc.set_facecolor(plot_colour)
                        pc.set_edgecolor(outline)
                        pc.set_alpha(0.7)
                    

                for vax in [0,0.2,0.5,0.8]:
                    if population_type == "younger":
                        if vax == 0.2:
                            plot_colour = 'lightskyblue'
                        elif vax == 0.5:
                            plot_colour = 'dodgerblue'
                        elif vax == 0.8:
                            plot_colour = 'navy'
                        elif vax==0:
                            plot_colour = "white"
                    else:
                        if vax == 0.2:
                            plot_colour = 'salmon'
                        elif vax == 0.5:
                            plot_colour = 'red'
                        elif vax == 0.8:
                            plot_colour = 'firebrick'
                        elif vax==0:
                            plot_colour = "white"
                    ax.plot([1,2,3],median_line[vax],color = plot_colour,linestyle='solid')


            ax.set_ylabel('Attack rate')
            y_ticks = list(range(0,160+1,10))
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

            

            ax.set_ylim(0,160)
            # ax.set_xlim([min(local_days),max_days])
            ax.grid(color='#878787', linestyle=(0, (5, 1)))
            ax.set_facecolor('silver')
            ax.set_axisbelow(True)

            # ax.axvline(x =first_exposure_time, color = 'white')
            # ax.axvline(x =second_exposure_time, color = 'white')
            # ax.axvline(x =third_exposure_time, color = 'white')

            def set_axis_style(ax, labels):
                ax.xaxis.set_tick_params(direction='out')
                ax.xaxis.set_ticks_position('bottom')
                ax.set_xticks(np.arange(1, len(labels) + 1), labels=labels)
                ax.set_xlim(0.25, len(labels) + 0.75)
                # ax.set_xlabel('Wave')

            labels = ["Wave 1", "Wave 2", "Wave 3"]
            set_axis_style(ax, labels)

            if len(younger_or_older)==2:
                ax.legend(legend_points[:4], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.28, 1), loc=1)
                leg = Legend(ax,legend_points[4:], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.28, 0.75), loc=1)
                ax.add_artist(leg)
            else:
                leg = ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=younger_or_older[0] +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
                leg._legend_box.align = "left"


            
            
            
            plt.savefig(os.path.join(folder, "violin_infections_over_time_"+"_".join(younger_or_older)+ "_"+plot_save[i_third_vax]+ "_maxTP_"+str(max(local_TP_list)) + ".png") , bbox_inches='tight')
            plt.close()


def plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],filter=False,aspect_ratio = 'equal',past_waves=[1],future_waves=[2],third_stage_vaccination = "none"):
    # third_stage_vaccination = "none", "early","reactive"

    if past_waves == [1]:
        days_before = list(range(0,second_exposure_time ))
    elif past_waves ==[1,2]:
        days_before = list(range(0,third_exposure_time ))
    elif past_waves ==[2]:
        days_before = list(range(second_exposure_time,third_exposure_time))
    else:
        print("wrong past wave entry")
        exit(1)

    if past_waves[-1]==1 and future_waves==[2]:
        days_after = list(range(second_exposure_time ,third_exposure_time))
    elif past_waves[-1]==2 and future_waves==[3]:
        days_after = list(range(third_exposure_time,max_days+1))
    else:
        print("past wave / future wave parameters still under construction")
        exit(1)


    if future_waves ==[2]:
        list_of_param_list = [param_list]
    elif future_waves==[3]:
        # then, need THREE sets of figures, not just one, for each type of vaccination 
        # boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]

        list_of_param_list = [[0,1,4,7],[0,2,5,8],[0,3,6,9]]
        third_vaccination_type = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
        plot_save =["no_more_vax","early_vax","reactive_vax"]
    
    for i_third_vax in range(len(list_of_param_list)):
        param_list_i = list_of_param_list[i_third_vax]

        if y_limits[1]>80:
            fig, ax = plt.subplots(1,1, figsize=(8,7.75)) # for the second strain
        else:
            fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        
        # first, some plotting to get some fake legends...
        legend_points = []
        marker='o'

        for population_type in population_type_list :
            if (past_waves==[1] and future_waves==[2]) or (past_waves==[1,2] and future_waves==[3]):
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
            
            for paramNum in param_list_i:
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

                    if booster_fraction == 0.5:
                        continue
                    elif booster_fraction ==0.8:
                        marker = "o"

                    
                    boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']

                    if (past_waves==[1] and future_waves==[2]) or (past_waves==[1,2] and future_waves==[3]):
                        outline = 'none'
                        if population_type == "younger":
                            if total_vaccination_rate == 0.2:
                                colour = 'lightskyblue'
                            elif total_vaccination_rate == 0.5:
                                colour = 'dodgerblue'
                            elif total_vaccination_rate == 0.8:
                                colour = 'navy'
                            elif total_vaccination_rate==0:
                                colour = 'white' 
                                outline ='lightskyblue'
                        else:
                            if total_vaccination_rate == 0.2:
                                colour = 'salmon'
                            elif total_vaccination_rate == 0.5:
                                colour = 'red'
                            elif total_vaccination_rate == 0.8:
                                colour = 'firebrick'
                            elif total_vaccination_rate==0:
                                colour = 'white'
                                outline='salmon'
                    
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
                        ax.scatter( percent_infected_before, percent_infected_after,color=colour, s=scale,  marker= marker, alpha=0.8, edgecolors=outline)
                    else:
                        percent_infected_before_filtered = []
                        percent_infected_after_filtered = []
                        for i in range(len(percent_infected_before)):
                            element = percent_infected_before[i]
                            if element>=20 and element<=80:
                                percent_infected_before_filtered.append(element)
                                percent_infected_after_filtered.append(percent_infected_after[i])
                        ax.scatter( percent_infected_before_filtered, percent_infected_after_filtered,color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)

        # ax.plot([20, 80], [20, 80],linestyle='--',color="black")
        
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)

        y_ticks = list(range(0,max(y_limits)+1,10))
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

        x_ticks = list(range(0,max(x_limits)+1,10))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        ax.set_aspect(aspect_ratio)
        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        if past_waves==[1] and future_waves==[2]:
            if len(population_type_list)==2:
                ax.legend(legend_points[:4], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.47, 1), loc=1)
                leg = Legend(ax,legend_points[4:], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.47, 0.75), loc=1)
                ax.add_artist(leg)
            else:
                if max(y_limits)!=100:
                    ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.47, 1), loc=1)
                else:
                    ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.6, 1), loc=1)
        elif (past_waves==[1,2] and future_waves==[3]):
            ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population with " + third_vaccination_type[i_third_vax],bbox_to_anchor=(0.6, 1), loc=1)

        ax.set_ylabel('near-future attack rate (t = ' + str(days_after[0])+' to ' + str(days_after[-1]+1)+')')
        ax.set_xlabel('past attack rate (before t = '+str(days_before[-1]+1) +')')
        

        # xticks = [15,20,30,40,50,60,70,80,85]
        xticks = x_ticks
        for x0, x1 in zip(xticks[::2], xticks[1::2]):
            plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

        # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

        if len(population_type_list)==2:
            addition = "combined"
        else:
            addition = population_type_list[0]   

        if (past_waves==[1,2] and future_waves==[3]):
            plt.savefig(os.path.join(folder, "past_immunity_80booster_only_" + addition+ "_pastwaves_" + "_".join(map(str, past_waves)) +"_futurewaves_" +"_".join(map(str, future_waves))+"_" +plot_save[i_third_vax] +".png") , bbox_inches='tight')
            
        else:
            plt.savefig(os.path.join(folder, "past_immunity_80booster_only_" + addition+ "_pastwaves_" + "_".join(map(str, past_waves)) +"_futurewaves_" +"_".join(map(str, future_waves)) +".png") , bbox_inches='tight')
        plt.close()





def plot_attack_rates_3D(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],z_limits = [-1,60]):
    
    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days+1))

    #need THREE sets of figures, not just one, for each type of vaccination 
    # boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]
    list_of_param_list = [[0,1,4,7],[0,2,5,8],[0,3,6,9]]
    third_vaccination_type = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    plot_save =["no_more_vax","early_vax","reactive_vax"]

    
    
    for i_third_vax in range(len(list_of_param_list)):
        param_list_i = list_of_param_list[i_third_vax]

        fig = plt.figure(figsize=(6,6.75))
        ax = fig.add_subplot(projection='3d')
        
        # first, some plotting to get some fake legends...
        legend_points = []
        marker='o'

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
            
            for paramNum in param_list_i:
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

                    # all booster fractions should be 0.8
                    # if booster_fraction == 0.5:
                    #     continue
                    # elif booster_fraction ==0.8:
                    #     marker = "o"

                    boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                    outline = 'none'
                    if population_type == "younger":
                        if total_vaccination_rate == 0.2:
                            colour = 'lightskyblue'
                        elif total_vaccination_rate == 0.5:
                            colour = 'dodgerblue'
                        elif total_vaccination_rate == 0.8:
                            colour = 'navy'
                        elif total_vaccination_rate==0:
                            colour = 'white' 
                            outline ='lightskyblue'
                    else:
                        if total_vaccination_rate == 0.2:
                            colour = 'salmon'
                        elif total_vaccination_rate == 0.5:
                            colour = 'red'
                        elif total_vaccination_rate == 0.8:
                            colour = 'firebrick'
                        elif total_vaccination_rate==0:
                            colour = 'white'
                            outline='salmon'
                    
                    datafilename = filename + ".csv"
                    data_file = os.path.join(folder, datafilename)
                    pd_obj = pd.read_csv(data_file)

                    new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                    df = new_pd.pivot(index='day', columns='sim', values='n')
                    df_dict = df.to_dict()
                    infections_per_sim_wave_1 = []
                    infections_per_sim_wave_2 = []
                    infections_per_sim_wave_3 = []

                    scale = 40
                    for simnum in df_dict.keys():
                        infections_over_time = df_dict[simnum]
                        total_infections_wave_1 = sum(list_conversion_nans(infections_over_time, days_wave_1))
                        infections_per_sim_wave_1.append(total_infections_wave_1)

                        total_infections_wave_2 = sum(list_conversion_nans(infections_over_time, days_wave_2))
                        infections_per_sim_wave_2.append(total_infections_wave_2)

                        total_infections_wave_3 = sum(list_conversion_nans(infections_over_time, days_wave_3))
                        infections_per_sim_wave_3.append(total_infections_wave_3)
                    
                    percent_infected_wave_1 = [x/total_population*100 for x in infections_per_sim_wave_1]
                    percent_infected_wave_2 = [x/total_population*100 for x in infections_per_sim_wave_2]
                    percent_infected_wave_3 = [x/total_population*100 for x in infections_per_sim_wave_3]

                    ax.scatter(percent_infected_wave_1,percent_infected_wave_2, percent_infected_wave_3, color=colour, s=scale,  marker= marker, alpha=0.8, edgecolors=outline)
                    
        
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)
        ax.set_zlim(z_limits)

        y_ticks = list(range(0,max(y_limits)+1,10))
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

        x_ticks =  list(range(0,max(x_limits)+1,10))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        z_ticks =  list(range(0,max(z_limits)+1,10))
        ax.set_zticks(z_ticks)
        ax.set_zticklabels([str(x)+"\%" for x in z_ticks])

        
        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population with " + third_vaccination_type[i_third_vax],bbox_to_anchor=(0.6, 1), loc=1)

        
        ax.set_xlabel('first wave attack rate')
        ax.set_ylabel('second wave attack rate')
        ax.set_zlabel('third wave attack rate')
        

        # xticks = [15,20,30,40,50,60,70,80,85]
        # for x0, x1 in zip(xticks[::2], xticks[1::2]):
        #     plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

        # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

        if len(population_type_list)==2:
            addition = "combined"
        else:
            addition = population_type_list[0]   

        plt.savefig(os.path.join(folder, "past_immunity_3D_" + addition+ "_"+plot_save[i_third_vax]+ ".png") , bbox_inches='tight')
        plt.close()




def plot_attack_rates_3D_animated(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],z_limits = [-1,60]):
    
    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days+1))

    #need THREE sets of figures, not just one, for each type of vaccination 
    # boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]
    list_of_param_list = [[0,1,4,7],[0,2,5,8],[0,3,6,9]]
    third_vaccination_type = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    plot_save =["no_more_vax","early_vax","reactive_vax"]

    
    
    for i_third_vax in range(len(list_of_param_list)):
        param_list_i = list_of_param_list[i_third_vax]

        fig = plt.figure(figsize=(6,6.75))
        ax = fig.add_subplot(projection='3d')
        
        # first, some plotting to get some fake legends...
        legend_points = []
        marker='o'

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
            
            for paramNum in param_list_i:
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

                    # all booster fractions should be 0.8
                    # if booster_fraction == 0.5:
                    #     continue
                    # elif booster_fraction ==0.8:
                    #     marker = "o"

                    boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                    outline = 'none'
                    if population_type == "younger":
                        if total_vaccination_rate == 0.2:
                            colour = 'lightskyblue'
                        elif total_vaccination_rate == 0.5:
                            colour = 'dodgerblue'
                        elif total_vaccination_rate == 0.8:
                            colour = 'navy'
                        elif total_vaccination_rate==0:
                            colour = 'white' 
                            outline ='lightskyblue'
                    else:
                        if total_vaccination_rate == 0.2:
                            colour = 'salmon'
                        elif total_vaccination_rate == 0.5:
                            colour = 'red'
                        elif total_vaccination_rate == 0.8:
                            colour = 'firebrick'
                        elif total_vaccination_rate==0:
                            colour = 'white'
                            outline='salmon'
                    
                    datafilename = filename + ".csv"
                    data_file = os.path.join(folder, datafilename)
                    pd_obj = pd.read_csv(data_file)

                    new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                    df = new_pd.pivot(index='day', columns='sim', values='n')
                    df_dict = df.to_dict()
                    infections_per_sim_wave_1 = []
                    infections_per_sim_wave_2 = []
                    infections_per_sim_wave_3 = []

                    scale = 40
                    for simnum in df_dict.keys():
                        infections_over_time = df_dict[simnum]
                        total_infections_wave_1 = sum(list_conversion_nans(infections_over_time, days_wave_1))
                        infections_per_sim_wave_1.append(total_infections_wave_1)

                        total_infections_wave_2 = sum(list_conversion_nans(infections_over_time, days_wave_2))
                        infections_per_sim_wave_2.append(total_infections_wave_2)

                        total_infections_wave_3 = sum(list_conversion_nans(infections_over_time, days_wave_3))
                        infections_per_sim_wave_3.append(total_infections_wave_3)
                    
                    percent_infected_wave_1 = [x/total_population*100 for x in infections_per_sim_wave_1]
                    percent_infected_wave_2 = [x/total_population*100 for x in infections_per_sim_wave_2]
                    percent_infected_wave_3 = [x/total_population*100 for x in infections_per_sim_wave_3]

                    ax.scatter(percent_infected_wave_1,percent_infected_wave_2, percent_infected_wave_3, color=colour, s=scale,  marker= marker, alpha=0.8, edgecolors=outline)
                    
        
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)
        ax.set_zlim(z_limits)

        y_ticks = list(range(0,max(y_limits)+1,10))
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

        x_ticks =  list(range(0,max(x_limits)+1,10))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        z_ticks =  list(range(0,max(z_limits)+1,10))
        ax.set_zticks(z_ticks)
        ax.set_zticklabels([str(x)+"\%" for x in z_ticks])

        
        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        # ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population with " + third_vaccination_type[i_third_vax],bbox_to_anchor=(0.6, 1.2), loc=1)

        ax.set_xlabel('first wave attack rate')
        ax.set_ylabel('second wave attack rate')
        ax.set_zlabel('third wave attack rate')

        def animate(i):
            ax.view_init(elev=20.,azim=i)
            return fig,

        rot_animation = matplotlib.animation.FuncAnimation(fig, animate, frames=np.arange(0,360,2),interval=100)
        # xticks = [15,20,30,40,50,60,70,80,85]
        # for x0, x1 in zip(xticks[::2], xticks[1::2]):
        #     plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

        # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

        if len(population_type_list)==2:
            addition = "combined"
        else:
            addition = population_type_list[0]   

        rot_animation.save(os.path.join(folder, "past_immunity_3D_" + addition+ "_"+plot_save[i_third_vax]+ ".gif"), dpi=72, writer='imagemagick')
        
        plt.close()



def plot_attack_rates_3D_animated_combined(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],z_limits = [-1,60]):
    
    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days+1))

    #need THREE sets of figures, not just one, for each type of vaccination 
    # boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]

    third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"] 

    

    for population_type in population_type_list :


        fig = plt.figure(figsize=(6,6.75))
        ax = fig.add_subplot(projection='3d')
        
        # first, some plotting to get some fake legends...
        legend_points = []

        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= '^', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= '^', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= '^', alpha=1.0, edgecolors='none'))

        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
    
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= '^', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= '^', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= '^', alpha=1.0, edgecolors='none'))

        for paramNum in param_list:
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

                # all booster fractions should be 0.8
                if booster_fraction == 0.5:
                    continue

                boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(boosters_only_vaccination_start)]
                if total_vaccination_rate==0 or third_vaccination_type in third_vaccination_types_wanted:
                    pass 
                else:
                    continue
                

                if total_vaccination_rate==0 or third_vaccination_type == "no further vaccination":
                    marker = 'o'
                elif third_vaccination_type == "reactive (delayed) vaccination":
                    marker = '^'
                else:
                    print("ERROR when assiging markers")
                    exit(1)

                outline = 'none'
                if population_type == "younger":
                    if total_vaccination_rate == 0.2:
                        colour = 'lightskyblue'
                    elif total_vaccination_rate == 0.5:
                        colour = 'dodgerblue'
                    elif total_vaccination_rate == 0.8:
                        colour = 'navy'
                    elif total_vaccination_rate==0:
                        colour = 'white' 
                        outline ='lightskyblue'
                else:
                    if total_vaccination_rate == 0.2:
                        colour = 'salmon'
                    elif total_vaccination_rate == 0.5:
                        colour = 'red'
                    elif total_vaccination_rate == 0.8:
                        colour = 'firebrick'
                    elif total_vaccination_rate==0:
                        colour = 'white'
                        outline='salmon'
                
                datafilename = filename + ".csv"
                data_file = os.path.join(folder, datafilename)
                pd_obj = pd.read_csv(data_file)

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')
                df_dict = df.to_dict()
                infections_per_sim_wave_1 = []
                infections_per_sim_wave_2 = []
                infections_per_sim_wave_3 = []

                scale = 40
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_wave_1 = sum(list_conversion_nans(infections_over_time, days_wave_1))
                    infections_per_sim_wave_1.append(total_infections_wave_1)

                    total_infections_wave_2 = sum(list_conversion_nans(infections_over_time, days_wave_2))
                    infections_per_sim_wave_2.append(total_infections_wave_2)

                    total_infections_wave_3 = sum(list_conversion_nans(infections_over_time, days_wave_3))
                    infections_per_sim_wave_3.append(total_infections_wave_3)
                
                percent_infected_wave_1 = [x/total_population*100 for x in infections_per_sim_wave_1]
                percent_infected_wave_2 = [x/total_population*100 for x in infections_per_sim_wave_2]
                percent_infected_wave_3 = [x/total_population*100 for x in infections_per_sim_wave_3]

                ax.scatter(percent_infected_wave_1,percent_infected_wave_2, percent_infected_wave_3, color=colour, s=scale,  marker= marker, alpha=0.8, edgecolors=outline)
                
        
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)
        ax.set_zlim(z_limits)

        y_ticks = list(range(0,max(y_limits)+1,10))
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

        x_ticks =  list(range(0,max(x_limits)+1,10))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        z_ticks =  list(range(0,max(z_limits)+1,10))
        ax.set_zticks(z_ticks)
        ax.set_zticklabels([str(x)+"\%" for x in z_ticks])


        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        ax.legend(legend_points, ["no vaccination","20\% vaccination coverage (no further vaccination)", "50\% vaccination coverage (no further vaccination)","80\% vaccination coverage (no further vaccination)","20\% vaccination coverage (+ reactive vaccination)", "50\% vaccination coverage (+ reactive vaccination)","80\% vaccination coverage (+ reactive vaccination)"],title=population_type_list[0] +" population",bbox_to_anchor=(0.6, 1.2), loc=1,ncol=2)

        ax.set_xlabel('first wave attack rate')
        ax.set_ylabel('second wave attack rate')
        ax.set_zlabel('third wave attack rate')

        def animate(i):
            ax.view_init(elev=20.,azim=i)
            return fig,

        rot_animation = matplotlib.animation.FuncAnimation(fig, animate, frames=np.arange(0,360,2),interval=100)
        # xticks = [15,20,30,40,50,60,70,80,85]
        # for x0, x1 in zip(xticks[::2], xticks[1::2]):
        #     plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

        # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

        if len(population_type_list)==2:
            addition = "combined"
        else:
            addition = population_type_list[0]   

        rot_animation.save(os.path.join(folder, "past_immunity_3D_combined_" + addition+".gif"), dpi=72, writer='imagemagick')

        plt.close()

def plot_wave_2_and_3_given_wave_1(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],aspect_ratio = 'equal'):
    
    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days+1))

    #need THREE sets of figures
    first_wave_vax_coverage = [0.2,0.5,0.8]
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]

    first_wave_attack_rate_limits = [[20,40],[40,60],[60,80]]

    for first_wave_vax in first_wave_vax_coverage:

        for lower_attack,higher_attack in first_wave_attack_rate_limits:
            fig, ax = plt.subplots(1,1, figsize=(8,7.75))
            
            # first, some plotting to get some fake legends...
            legend_points = []
            marker='o'

            for population_type in population_type_list :
                legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='violet'))
                legend_points.append(ax.scatter(-10000,-10000,color='violet', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='blueviolet', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='rebeccapurple', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                # if population_type=="younger":
                #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                # if population_type=="older":
                #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                
                for paramNum in param_list:
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

                        # print(total_vaccination_rate)

                        if total_vaccination_rate==0.0 or total_vaccination_rate == first_wave_vax:
                            marker = "o"
                        else:
                            continue

                        # all booster fractions should be 0.8
                        # if booster_fraction == 0.5:
                        #     continue
                        # elif booster_fraction ==0.8:
                        #     marker = "o"

                        boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                        # boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]
                        third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(boosters_only_vaccination_start)]

                        # print(third_vaccination_type)


                        outline = 'none'
                        if total_vaccination_rate==0:
                            colour = 'white' 
                            outline ='violet'
                        elif third_vaccination_type =="no further vaccination":
                            colour = 'violet'
                        elif third_vaccination_type == "additional early vaccination":
                            colour = 'blueviolet'
                        elif third_vaccination_type == "reactive (delayed) vaccination":
                            colour = 'rebeccapurple'
                        # if population_type == "younger":
                        #     if total_vaccination_rate == 0.2:
                        #         colour = 'lightskyblue'
                        #     elif total_vaccination_rate == 0.5:
                        #         colour = 'dodgerblue'
                        #     elif total_vaccination_rate == 0.8:
                        #         colour = 'navy'
                        #     elif total_vaccination_rate==0:
                        #         colour = 'white' 
                        #         outline ='lightskyblue'
                        # else:
                        #     if total_vaccination_rate == 0.2:
                        #         colour = 'salmon'
                        #     elif total_vaccination_rate == 0.5:
                        #         colour = 'red'
                        #     elif total_vaccination_rate == 0.8:
                        #         colour = 'firebrick'
                        #     elif total_vaccination_rate==0:
                        #         colour = 'white'
                        #         outline='salmon'
                        
                        
                        datafilename = filename + ".csv"
                        data_file = os.path.join(folder, datafilename)
                        pd_obj = pd.read_csv(data_file)

                        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                        df = new_pd.pivot(index='day', columns='sim', values='n')
                        df_dict = df.to_dict()
                        infections_per_sim_wave_1 = []
                        infections_per_sim_wave_2 = []
                        infections_per_sim_wave_3 = []

                        scale = 40
                        for simnum in df_dict.keys():
                            infections_over_time = df_dict[simnum]
                            total_infections_wave_1 = sum(list_conversion_nans(infections_over_time, days_wave_1))
                            infections_per_sim_wave_1.append(total_infections_wave_1)

                            total_infections_wave_2 = sum(list_conversion_nans(infections_over_time, days_wave_2))
                            infections_per_sim_wave_2.append(total_infections_wave_2)

                            total_infections_wave_3 = sum(list_conversion_nans(infections_over_time, days_wave_3))
                            infections_per_sim_wave_3.append(total_infections_wave_3)
                        
                        percent_infected_wave_1 = [x/total_population*100 for x in infections_per_sim_wave_1]
                        percent_infected_wave_2 = [x/total_population*100 for x in infections_per_sim_wave_2]
                        percent_infected_wave_3 = [x/total_population*100 for x in infections_per_sim_wave_3]


                        percent_infected_wave_2_filtered = []
                        percent_infected_wave_3_filtered = []
                        for i in range(len(percent_infected_wave_1)):
                            element = percent_infected_wave_1[i]
                            if element>=lower_attack and element<=higher_attack:
                                percent_infected_wave_2_filtered.append(percent_infected_wave_2[i])
                                percent_infected_wave_3_filtered.append(percent_infected_wave_3[i])

                        if len(percent_infected_wave_2_filtered)>0:
                            ax.scatter(percent_infected_wave_2_filtered, percent_infected_wave_3_filtered,color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)
                        
            
            ax.set_xlim(x_limits)
            ax.set_ylim(y_limits)

            y_ticks = list(range(0,max(y_limits)+1,10))
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

            x_ticks =  list(range(0,max(x_limits)+1,10))
            ax.set_xticks(x_ticks)
            ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

            ax.set_aspect(aspect_ratio)
            # ax.grid(True)
            ax.set_axisbelow(True)
            ax.grid(color='gray')
            # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

            ax.legend(legend_points, ["no vaccination ever","no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"],title=population_type_list[0] +" population with \n" + str(first_wave_vax*100) +"\% vaccination in first year and \n"+str(lower_attack)+"\% - " + str(higher_attack)+"\% first year attack rate",bbox_to_anchor=(0.9, 0.3), loc=1)

            
            ax.set_xlabel('second wave attack rate')
            ax.set_ylabel('third wave attack rate')
            

            # xticks = [15,20,30,40,50,60,70,80,85]
            # for x0, x1 in zip(xticks[::2], xticks[1::2]):
            #     plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

            # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

            if len(population_type_list)==2:
                addition = "combined"
            else:
                addition = population_type_list[0]   

            plt.savefig(os.path.join(folder, "past_immunity_" + addition+ "_"+ str(first_wave_vax)+"_vax_" + str(higher_attack) +"_attack.png") , bbox_inches='tight')
            plt.close()


def plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated(ICU_or_death,OG="",population_type_list = ["younger","older"],ylimits = [0,28],y_ticks = list(range(0,29,2)),x_limits=[15,85],filter=False,past_waves=[1],future_waves=[2]): # or "OG_"

    if past_waves == [1]:
        days_before = list(range(0,second_exposure_time ))
    elif past_waves ==[1,2]:
        days_before = list(range(0,third_exposure_time ))
    elif past_waves ==[2]:
        days_before = list(range(second_exposure_time,third_exposure_time))
    else:
        print("wrong past wave entry")
        exit(1)

    if past_waves[-1]==1 and future_waves==[2]:
        days_after = list(range(second_exposure_time ,third_exposure_time))
    elif past_waves[-1]==2 and future_waves==[3]:
        days_after = list(range(third_exposure_time,max_days+1))
    else:
        print("past wave / future wave parameters still under construction")
        exit(1)


    if future_waves ==[2]:
        list_of_param_list = [param_list]
    elif future_waves==[3]:
        # then, need THREE sets of figures, not just one, for each type of vaccination 
        # boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]

        list_of_param_list = [[0,1,4,7],[0,2,5,8],[0,3,6,9]]
        third_vaccination_type = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
        plot_save =["no_more_vax","early_vax","reactive_vax"]

    for i_third_vax in range(len(list_of_param_list)):
        param_list_i = list_of_param_list[i_third_vax]

        fig, ax = plt.subplots(1,1, figsize=(6,5))

        # first, some plotting to get some fake legends...
        legend_points = []
        max_y= 0
        marker = "o"

        for population_type in population_type_list:
            if population_type=='younger':
                legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
                legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            if population_type=='older':
                legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
                legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

            for paramNum in param_list_i:
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

                    outline = 'none'
                    if population_type == "younger":
                        if total_vaccination_rate == 0.2:
                            colour = 'lightskyblue'
                        elif total_vaccination_rate == 0.5:
                            colour = 'dodgerblue'
                        elif total_vaccination_rate == 0.8:
                            colour = 'navy'
                        elif total_vaccination_rate==0:
                            colour = 'white' 
                            outline ='lightskyblue'
                    else:
                        if total_vaccination_rate == 0.2:
                            colour = 'salmon'
                        elif total_vaccination_rate == 0.5:
                            colour = 'red'
                        elif total_vaccination_rate == 0.8:
                            colour = 'firebrick'
                        elif total_vaccination_rate==0:
                            colour = 'white'
                            outline='salmon'
                    
                    if booster_fraction == 0.5:
                        continue
                    elif booster_fraction ==0.8:
                        marker = "o"
                    
                    datafilename = filename + ".csv"
                    data_file = os.path.join(folder, datafilename)
                    pd_obj = pd.read_csv(data_file)

                    new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                    df = new_pd.pivot(index='day', columns='sim', values='n')
                    df_dict = df.to_dict()
                    infections_per_sim_before = []
                    infections_per_sim_after = []

                    severe_disease_after = []

                    clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                    clinical_file = os.path.join(folder,filename,clinical_filename)

                    if os.path.isfile(clinical_file):
                        pass
                    else:
                        print(clinical_file +" DOES NOT EXIST!")
                        continue


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
                            
                            new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_after))]
                            
                            if ICU_or_death == 'death':
                                daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                severe_disease_after.append(daily_deaths)
                            elif ICU_or_death =='ICU':
                                daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                severe_disease_after.append(daily_ICU_admissions)
                    #print(severe_disease_after)
                    percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                    percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]
                    
                    if not filter:
                        ax.scatter(percent_infected_before, severe_disease_after, color=colour, s=scale, marker= marker, alpha=0.8, edgecolors=outline)
                        max_y = max(max_y,max( severe_disease_after))
                    else:
                        percent_infected_before_filtered = []
                        severe_disease_after_filtered = []
                        for i in range(len(percent_infected_before)):
                            element = percent_infected_before[i]
                            if element>=20 and element<=80:
                                percent_infected_before_filtered.append(element)
                                severe_disease_after_filtered.append(severe_disease_after[i])

                        if  severe_disease_after_filtered!=[]:
                            ax.scatter(percent_infected_before_filtered, severe_disease_after_filtered, color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)
                            max_y = max(max_y,max( severe_disease_after_filtered))

        print(max_y)
        ax.set_xlim(x_limits)
        ax.set_ylim(ylimits)

        # x_ticks =  list(range(round(min(x_limits)-10,-1),max(x_limits)+11,10))
        x_ticks = [20,30,40,50,60,70,80]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        # y_ticks = list(range(0,ylimits[1]+1,2))
        ax.set_yticks(y_ticks)

        
        # ax.grid(True)
        # ax.legend(legend_list)
        ax.set_xlabel('past attack rate (before t = 450)')
        ax.grid(True, which='major',color='gray')
        ax.set_axisbelow(True)

        legendlist = ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"]

        if past_waves==[1] and future_waves==[2]:
            if len(population_type_list)==2:
                ax.legend(legend_points[:4], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.47, 1), loc=1)
                leg = Legend(ax,legend_points[4:], ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.47, 0.75), loc=1)
                ax.add_artist(leg)
            else:
                if max(ylimits)!=100:
                    ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.47, 1), loc=1)
                else:
                    ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.6, 1), loc=1)
        elif (past_waves==[1,2] and future_waves==[3]):
            ax.legend(legend_points, ["no vaccination","20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population with " + third_vaccination_type[i_third_vax],bbox_to_anchor=(0.6, 1), loc=1)

        ax.set_xlabel('past attack rate (before t = '+str(days_before[-1]+1) +')')

        xticks = [15,20,30,40,50,60,70,80,85]
        # xticks= x_ticks
        for x0, x1 in zip(xticks[::2], xticks[1::2]):
            plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

        if len(population_type_list)==2:
            addition = "combined"
        else:
            addition = population_type_list[0]  

        if ICU_or_death == 'death':
            ax.set_ylabel('near-future deaths (t = ' + str(days_after[0])+' to ' + str(days_after[-1]+1)+')')
            
            #ax.set_title('Deaths given past hybrid immunity',fontsize=14)
        elif ICU_or_death =='ICU':
            ax.set_ylabel('near-future ICU admissions (t = ' + str(days_after[0])+' to ' + str(days_after[-1]+1)+')')
            #ax.set_title('ICU admissions given past immunity',fontsize=14)

        if (past_waves==[1,2] and future_waves==[3]):
            plt.savefig(os.path.join(folder,"with_novax_" + ICU_or_death+"_vs_past_immunity"+OG+"_ages_80_booster_only_horizontal_"+addition+ "_pastwaves_" + "_".join(map(str, past_waves)) +"_futurewaves_" +"_".join(map(str, future_waves))+"_" +plot_save[i_third_vax] +".png") , bbox_inches='tight')
        else:
            plt.savefig(os.path.join(folder,"with_novax_" + ICU_or_death+"_vs_past_immunity"+OG+"_ages_80_booster_only_horizontal_"+addition+ "_pastwaves_" + "_".join(map(str, past_waves)) +"_futurewaves_" +"_".join(map(str, future_waves)) +".png") , bbox_inches='tight')
        plt.close()
        




def plot_third_wave_ICU_and_deaths_given_second_and_first_wave(ICU_or_death,OG="",population_type_list = ["younger","older"],ylimits = [0,28],y_ticks = list(range(0,29,2)),x_limits=[15,85]): # or "OG_"

    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days+1))

    #need THREE sets of figures
    first_wave_vax_coverage = [0.2,0.5,0.8]
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]

    first_wave_attack_rate_limits = [[20,40],[40,60],[60,80]]

    for first_wave_vax in first_wave_vax_coverage:

        for lower_attack,higher_attack in first_wave_attack_rate_limits:

            fig, ax = plt.subplots(1,1, figsize=(6,5))

            # first, some plotting to get some fake legends...
            legend_points = []
            max_y= 0
            marker = "o"

            for population_type in population_type_list:
                legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='violet'))
                legend_points.append(ax.scatter(-10000,-10000,color='violet', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='blueviolet', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color='rebeccapurple', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                # if population_type=='younger':
                #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                # if population_type=='older':
                #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                for paramNum in param_list:
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

                        if booster_fraction == 0.5:
                            continue
                        elif booster_fraction ==0.8:
                            marker = "o"

                        if total_vaccination_rate==0.0 or total_vaccination_rate == first_wave_vax:
                            marker = "o"
                        else:
                            continue
                        
                        boosters_only_vaccination_start = presim_parameters['boosters_only_vaccination_start']
                        # boosters_only_vaccination_start_list = [-1, max(third_exposure_time-30*4,7*26*3+1),third_exposure_time+14]
                        third_vaccination_type = third_vaccination_type_list[boosters_only_vaccination_start_list.index(boosters_only_vaccination_start)]

                        # print(third_vaccination_type)


                        outline = 'none'
                        if total_vaccination_rate==0:
                            colour = 'white' 
                            outline ='violet'
                        elif third_vaccination_type =="no further vaccination":
                            colour = 'violet'
                        elif third_vaccination_type == "additional early vaccination":
                            colour = 'blueviolet'
                        elif third_vaccination_type == "reactive (delayed) vaccination":
                            colour = 'rebeccapurple'
                        # outline = 'none'
                        # if population_type == "younger":
                        #     if total_vaccination_rate == 0.2:
                        #         colour = 'lightskyblue'
                        #     elif total_vaccination_rate == 0.5:
                        #         colour = 'dodgerblue'
                        #     elif total_vaccination_rate == 0.8:
                        #         colour = 'navy'
                        #     elif total_vaccination_rate==0:
                        #         colour = 'white' 
                        #         outline ='lightskyblue'
                        # else:
                        #     if total_vaccination_rate == 0.2:
                        #         colour = 'salmon'
                        #     elif total_vaccination_rate == 0.5:
                        #         colour = 'red'
                        #     elif total_vaccination_rate == 0.8:
                        #         colour = 'firebrick'
                        #     elif total_vaccination_rate==0:
                        #         colour = 'white'
                        #         outline='salmon'
                        
                        
                        
                        datafilename = filename + ".csv"
                        data_file = os.path.join(folder, datafilename)
                        pd_obj = pd.read_csv(data_file)

                        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                        df = new_pd.pivot(index='day', columns='sim', values='n')
                        df_dict = df.to_dict()
                        infections_per_sim_wave_1 = []
                        infections_per_sim_wave_2 = []
                        infections_per_sim_wave_1_expanded = []
                        infections_per_sim_wave_2_expanded = []

                        severe_disease_wave_3 = []

                        clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                        clinical_file = os.path.join(folder,filename,clinical_filename)

                        if os.path.isfile(clinical_file):
                            pass
                        else:
                            print(clinical_file +" DOES NOT EXIST!")
                            continue


                        clinical_pd_obj = pd.read_csv(clinical_file)

                        scale = 40
                        aug_num = 5
                        for simnum in df_dict.keys():
                            infections_over_time = df_dict[simnum]
                            total_infections_wave_1 = sum(list_conversion_nans(infections_over_time, days_wave_1))
                            infections_per_sim_wave_1.append(total_infections_wave_1)

                            total_infections_wave_2 = sum(list_conversion_nans(infections_over_time, days_wave_2))
                            infections_per_sim_wave_2.append(total_infections_wave_2)

                            for aug in range(1,aug_num+1):
                                infections_per_sim_wave_1_expanded.append(total_infections_wave_1 )
                                infections_per_sim_wave_2_expanded.append(total_infections_wave_2)
                                
                                new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_wave_3))]
                                
                                if ICU_or_death == 'death':
                                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                    severe_disease_wave_3.append(daily_deaths)
                                elif ICU_or_death =='ICU':
                                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                    severe_disease_wave_3.append(daily_ICU_admissions)
                        #print(severe_disease_after)
                        percent_infected_wave_1 = [x/total_population*100 for x in infections_per_sim_wave_1_expanded]
                        percent_infected_wave_2 = [x/total_population*100 for x in infections_per_sim_wave_2_expanded]
                        
                        percent_infected_wave_2_filtered = []
                        severe_disease_wave_3_filtered = []
                        for i in range(len(percent_infected_wave_1)):
                            element = percent_infected_wave_1[i]
                            if element>=lower_attack and element<=higher_attack:
                                percent_infected_wave_2_filtered.append(percent_infected_wave_2[i])
                                severe_disease_wave_3_filtered.append(severe_disease_wave_3[i])

                        if  severe_disease_wave_3_filtered!=[]:
                            ax.scatter(percent_infected_wave_2_filtered,severe_disease_wave_3_filtered , color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)
                            max_y = max(max_y,max( severe_disease_wave_3_filtered ))

            # print(max_y)
            ax.set_xlim(x_limits)
            ax.set_ylim(ylimits)

            x_ticks =  list(range(round(min(x_limits)-10,-1),max(x_limits)+11,10)) # list(range(round(min(x_limits),-1),max(x_limits)+1,10))
            ax.set_xticks(x_ticks)
            ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

            # y_ticks = list(range(0,ylimits[1]+1,2))
            ax.set_yticks(y_ticks)

            
            # ax.grid(True)
            # ax.legend(legend_list)
            ax.grid(True, which='major',color='gray')
            ax.set_axisbelow(True)

            ax.legend(legend_points, ["no vaccination ever","no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"],title=population_type_list[0] +" population with \n" + str(first_wave_vax*100) +"\% vaccination in first year and \n"+str(lower_attack)+"\% - " + str(higher_attack)+"\% first year attack rate",bbox_to_anchor=(0.9, 0.9), loc=1)

            
            ax.set_xlabel('second wave attack rate')

            # xticks = [15,20,30,40,50,60,70,80,85]
            # xticks= x_ticks
            # for x0, x1 in zip(xticks[::2], xticks[1::2]):
            #     plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

            if len(population_type_list)==2:
                addition = "combined"
            else:
                addition = population_type_list[0]  

            if ICU_or_death == 'death':
                ax.set_ylabel('third wave deaths')
                
            elif ICU_or_death =='ICU':
                ax.set_ylabel('third wave ICU admissions')

            plt.savefig(os.path.join(folder,ICU_or_death+"_vs_past_immunity"+OG+"_ages_80_booster_only_horizontal_"+addition+"_" + str(first_wave_vax)+"_vax_" + str(higher_attack) +"_attack.png") , bbox_inches='tight')
            plt.close()
            






def plot_comparison_third_wave_ICU_and_deaths_given_scenario(folder_start_wave_2,presim_parameters_folder_start_wave_2,folder_start_wave_3,presim_parameters_folder_start_wave_3, ICU_or_death,population_type_list = ["younger","older"]):

    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days+1))


    first_wave_vax_coverage = [0.2,0.5,0.8]
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"]

    wavestart_list =  ['start_wave_2','start_wave_3']
    folder_start_list = [folder_start_wave_2,folder_start_wave_3]
    presim_parameters_folder_start_list = [presim_parameters_folder_start_wave_2,presim_parameters_folder_start_wave_3]

    TP_reduced_list =  [TP_low, TP_high]
    TP_type_list = ['TP_low','TP_high']

    # TP_segregated_list = [TP_low,TP_mid,TP_high]
    for population_type in population_type_list :

        fig, ax = plt.subplots(1,1, figsize=(6,7))

        all_deaths = {'start_wave_2':{},'start_wave_3':{}}
        for wavestart in wavestart_list:
            all_deaths[wavestart] = {'TP_low':{},'TP_high':{}}
            for TP_type in TP_type_list:
                all_deaths[wavestart][TP_type] = {0:[],0.2:{},0.5:{},0.8:{}}
                for vax_cov in [0.2,0.5,0.8]:
                    all_deaths[wavestart][TP_type][vax_cov] = {"no further vaccination":[],"reactive (delayed) vaccination":[]}

        for wavestart, folder_start, presim_parameters_folder_start in zip(wavestart_list,folder_start_list,presim_parameters_folder_start_list):
            for TP_type, local_TP_list in zip(TP_type_list,TP_reduced_list):
                for paramNum in param_list:
                    for TP in local_TP_list:

                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
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
                        
                        severe_disease_wave_3 = []

                        clinical_filename = "_full_outcomes_dataframe.csv"
                        clinical_file = os.path.join(folder_start,filename,clinical_filename)

                        if os.path.isfile(clinical_file):
                            pass
                        else:
                            print(clinical_file +" DOES NOT EXIST!")
                            continue


                        clinical_pd_obj = pd.read_csv(clinical_file)

                        scale = 40
                        aug_num = 5
                        for simnum in range(1,SIM_NUMBER+1):
                            for aug in range(1,aug_num+1):
                                
                                new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_wave_3))]
                                
                                if ICU_or_death == 'death':
                                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                    severe_disease_wave_3.append(daily_deaths)
                                elif ICU_or_death =='ICU':
                                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                    severe_disease_wave_3.append(daily_ICU_admissions)
                        
                        if total_vaccination_rate==0:
                            all_deaths[wavestart][TP_type][total_vaccination_rate].extend(severe_disease_wave_3)
                        else:

                            all_deaths[wavestart][TP_type][total_vaccination_rate][third_vaccination_type].extend(severe_disease_wave_3)
                        
        print(all_deaths)
        pairwise_differences = {'TP_low':{},'TP_high':{}}
        for TP_type in TP_type_list:
            pairwise_differences[TP_type] = {0:[],0.2:{},0.5:{},0.8:{}}
            for vax_cov in [0.2,0.5,0.8]:
                pairwise_differences[TP_type][vax_cov] = {"no further vaccination":[],"reactive (delayed) vaccination":[]}
                for third_wave_vax_type in third_vaccination_types_wanted:
                    start_wave_2 = all_deaths['start_wave_2'][TP_type][vax_cov][third_wave_vax_type]
                    start_wave_3 = all_deaths['start_wave_3'][TP_type][vax_cov][third_wave_vax_type]
                    difference_list = []
                    for sw2_i in start_wave_2:
                        for sw3_i in start_wave_3:
                            difference = sw3_i - sw2_i 
                            difference_list.append(difference)
                    pairwise_differences[TP_type][vax_cov][third_wave_vax_type].extend(difference_list)
            for vax_cov in [0]:
                start_wave_2 = all_deaths['start_wave_2'][TP_type][vax_cov]
                start_wave_3 = all_deaths['start_wave_3'][TP_type][vax_cov]
                difference_list = []
                for sw2_i in start_wave_2:
                    for sw3_i in start_wave_3:
                        difference = sw3_i - sw2_i 
                        difference_list.append(difference)
                pairwise_differences[TP_type][vax_cov].extend(difference_list)

        plot_position = []
        plot_label = []
        position = 1

        print(pairwise_differences)

        for TP_type,TP_type_name in zip(TP_type_list, ["low TP","high TP"]):
            for vax_cov in [0]:
                if population_type == "younger":
                    plot_colour = "white"
                    outline ='lightskyblue'
                else:
                    plot_colour = "white"
                    outline='salmon'

                plot_position.append(position)
                plot_label.append(str(vax_cov*100)+"\% vaccination and " + TP_type_name)

                data_to_plot = [pairwise_differences[TP_type][vax_cov]]
                parts = ax.violinplot(data_to_plot,[position], showmeans=False, showmedians=False, showextrema=False,vert=False)
                for pc in parts['bodies']:
                    pc.set_facecolor(plot_colour)
                    pc.set_edgecolor(outline)
                    pc.set_alpha(0.7)
                
                position-=1

                

            for vax_cov in [0.2,0.5,0.8]:
                for third_wave_vax_type in third_vaccination_types_wanted:
                    outline = 'none'
                    if population_type == "younger":
                        if vax_cov == 0.2:
                            plot_colour = 'lightskyblue'
                            outline= 'lightskyblue'
                        elif vax_cov == 0.5:
                            plot_colour = 'dodgerblue'
                            outline = 'dodgerblue'
                        elif vax_cov == 0.8:
                            plot_colour = 'navy'
                            outline = 'navy'
                    else:
                        if vax_cov == 0.2:
                            plot_colour = 'salmon'
                            outline = 'salmon'
                        elif vax_cov == 0.5:
                            plot_colour = 'red'
                            outline = 'red'
                        elif vax_cov == 0.8:
                            plot_colour = 'firebrick'
                            outline = 'firebrick'
                    if third_wave_vax_type =="no further vaccination":
                        third_wave_vax_name = third_wave_vax_type
                    else:
                        third_wave_vax_name = "reactive vaccination"

                    plot_position.append(position)
                    plot_label.append(str(vax_cov*100)+"\% vaccination ("+ third_wave_vax_name+") and " + TP_type_name)
                    data_to_plot = [pairwise_differences[TP_type][vax_cov][third_wave_vax_type]]
                    parts = ax.violinplot(data_to_plot,[position],showmeans=False, showmedians=False, showextrema=False,vert=False) # 
                    for pc in parts['bodies']:
                        pc.set_facecolor(plot_colour)
                        pc.set_edgecolor(outline)
                        pc.set_alpha(0.7)

                    position-=1
                        
        ax.grid(color='#878787', linestyle=(0, (5, 1)))
        ax.set_facecolor('silver')
        ax.set_axisbelow(True)

        ax.axvline(x =0, color = 'black')

        # x_ticks =  list(range(round(min(x_limits)-10,-1),max(x_limits)+11,10)) # list(range(round(min(x_limits),-1),max(x_limits)+1,10))
        # ax.set_xticks(x_ticks)
        # ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        # y_ticks = list(range(0,ylimits[1]+1,2))
        # ax.set_yticks(y_ticks)
       
        ax.set_yticks(plot_position,labels= plot_label)
        
        # ax.grid(True)
        # ax.legend(legend_list)
        # ax.grid(True, which='major',color='gray')
        # ax.set_axisbelow(True)

        # ax.legend(legend_points, ["no vaccination ever","no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"],title=population_type_list[0] +" population with \n" + str(first_wave_vax*100) +"\% vaccination in first year and \n"+str(lower_attack)+"\% - " + str(higher_attack)+"\% first year attack rate",bbox_to_anchor=(0.9, 0.9), loc=1)

        
        # ax.set_xlabel('second wave attack rate')
        

        # xticks = [15,20,30,40,50,60,70,80,85]
        # xticks= x_ticks
        # for x0, x1 in zip(xticks[::2], xticks[1::2]):
        #     plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

        if len(population_type_list)==2:
            addition = "combined"
        else:
            addition = population_type_list[0]  

        if ICU_or_death == 'death':
            # ax.set_ylabel('third wave deaths')
            plt.suptitle('Third wave deaths')
            
        elif ICU_or_death =='ICU':
            # ax.set_ylabel('third wave ICU admissions')
            plt.suptitle('Third wave ICU admissions')

        ax.set_title('[immune escape starting wave 3] - [immune escape starting wave 2]')
        plt.savefig(os.path.join(folder,"violin_scenarios_"+ICU_or_death+"_vs_past_immunity_"+addition+".png") , bbox_inches='tight')
        plt.close()
        




def plot_comparison_third_wave_ICU_and_deaths_given_scenario_wavestart(folder_start_wave_2,presim_parameters_folder_start_wave_2,folder_start_wave_3,presim_parameters_folder_start_wave_3, ICU_or_death,population_type_list = ["younger","older"]):

    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days))


    first_wave_vax_coverage = [0.2,0.5,0.8]
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"]

    wavestart_list =  ['start_wave_2','start_wave_3']
    folder_start_list = [folder_start_wave_2,folder_start_wave_3]
    presim_parameters_folder_start_list = [presim_parameters_folder_start_wave_2,presim_parameters_folder_start_wave_3]

    TP_reduced_list =  [TP_low, TP_high]
    TP_type_list = ['TP_low','TP_high']

    # TP_segregated_list = [TP_low,TP_mid,TP_high]
    for population_type in population_type_list :

        

        all_deaths = {'start_wave_2':{},'start_wave_3':{}}
        for wavestart in wavestart_list:
            all_deaths[wavestart] = {'TP_low':{},'TP_high':{}}
            for TP_type in TP_type_list:
                all_deaths[wavestart][TP_type] = {0:[],0.2:{},0.5:{},0.8:{}}
                for vax_cov in [0.2,0.5,0.8]:
                    all_deaths[wavestart][TP_type][vax_cov] = {"no further vaccination":[],"reactive (delayed) vaccination":[]}

        for wavestart, folder_start, presim_parameters_folder_start in zip(wavestart_list,folder_start_list,presim_parameters_folder_start_list):
            for TP_type, local_TP_list in zip(TP_type_list,TP_reduced_list):
                for paramNum in param_list:
                    for TP in local_TP_list:

                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
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
                        
                        severe_disease_wave_3 = []

                        clinical_filename = "_full_outcomes_dataframe.csv"
                        clinical_file = os.path.join(folder_start,filename,clinical_filename)

                        if os.path.isfile(clinical_file):
                            pass
                        else:
                            print(clinical_file +" DOES NOT EXIST!")
                            continue


                        clinical_pd_obj = pd.read_csv(clinical_file)

                        scale = 40
                        aug_num = 5
                        for simnum in range(1,SIM_NUMBER+1):
                            for aug in range(1,aug_num+1):
                                
                                new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_wave_3))]
                                
                                if ICU_or_death == 'death':
                                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                    severe_disease_wave_3.append(daily_deaths)
                                elif ICU_or_death =='ICU':
                                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                    severe_disease_wave_3.append(daily_ICU_admissions)
                        
                        if total_vaccination_rate==0:
                            all_deaths[wavestart][TP_type][total_vaccination_rate].extend(severe_disease_wave_3)
                        else:

                            all_deaths[wavestart][TP_type][total_vaccination_rate][third_vaccination_type].extend(severe_disease_wave_3)
                        
        print(all_deaths)

        for wavestart, folder_start in zip(wavestart_list,folder_start_list):
            fig, ax = plt.subplots(1,1, figsize=(6,7))

            plot_position = []
            plot_label = []
            position = 1

            for TP_type,TP_type_name in zip(TP_type_list, ["low TP","high TP"]):
                for vax_cov in [0]:
                    if population_type == "younger":
                        plot_colour = "white"
                        outline ='lightskyblue'
                    else:
                        plot_colour = "white"
                        outline='salmon'

                    plot_position.append(position)
                    plot_label.append(str(vax_cov*100)+"\% vaccination and " + TP_type_name)

                    data_to_plot = [all_deaths[wavestart][TP_type][vax_cov]]
                    parts = ax.violinplot(data_to_plot,[position], showmeans=False, showmedians=False, showextrema=False,vert=False)
                    for pc in parts['bodies']:
                        pc.set_facecolor(plot_colour)
                        pc.set_edgecolor(outline)
                        pc.set_alpha(0.7)
                    
                    position-=1

                    

                for vax_cov in [0.2,0.5,0.8]:
                    for third_wave_vax_type in third_vaccination_types_wanted:
                        outline = 'none'
                        if population_type == "younger":
                            if vax_cov == 0.2:
                                plot_colour = 'lightskyblue'
                                outline= 'lightskyblue'
                            elif vax_cov == 0.5:
                                plot_colour = 'dodgerblue'
                                outline = 'dodgerblue'
                            elif vax_cov == 0.8:
                                plot_colour = 'navy'
                                outline = 'navy'
                        else:
                            if vax_cov == 0.2:
                                plot_colour = 'salmon'
                                outline = 'salmon'
                            elif vax_cov == 0.5:
                                plot_colour = 'red'
                                outline = 'red'
                            elif vax_cov == 0.8:
                                plot_colour = 'firebrick'
                                outline = 'firebrick'
                        if third_wave_vax_type =="no further vaccination":
                            third_wave_vax_name = third_wave_vax_type
                        else:
                            third_wave_vax_name = "reactive vaccination"

                        plot_position.append(position)
                        plot_label.append(str(vax_cov*100)+"\% vaccination ("+ third_wave_vax_name+") and " + TP_type_name)
                        data_to_plot = [all_deaths[wavestart][TP_type][vax_cov][third_wave_vax_type]]
                        parts = ax.violinplot(data_to_plot,[position],showmeans=False, showmedians=False, showextrema=False,vert=False) # 
                        for pc in parts['bodies']:
                            pc.set_facecolor(plot_colour)
                            pc.set_edgecolor(outline)
                            pc.set_alpha(0.7)

                        position-=1
                            
            ax.grid(color='#878787', linestyle=(0, (5, 1)))
            ax.set_facecolor('silver')
            ax.set_axisbelow(True)

            ax.axvline(x =0, color = 'black')
        
            ax.set_yticks(plot_position,labels= plot_label)
            ax.set_xlim(-2,80)
            
            if len(population_type_list)==2:
                addition = "combined"
            else:
                addition = population_type_list[0]  

            if ICU_or_death == 'death':
                # ax.set_ylabel('third wave deaths')
                ax.set_title('Third wave deaths')
                
            elif ICU_or_death =='ICU':
                # ax.set_ylabel('third wave ICU admissions')
                ax.set_title('Third wave ICU admissions')

            plt.savefig(os.path.join(folder_start,"violin_scenarios_wave_start_"+ wavestart+"_" +ICU_or_death+"_vs_past_immunity_"+addition+".png") , bbox_inches='tight')
            plt.close()
        




def plot_comparison_third_wave_ICU_and_deaths_given_scenario_breakdown_wavestart(folder_start_wave_2,presim_parameters_folder_start_wave_2,folder_start_wave_3,presim_parameters_folder_start_wave_3, ICU_or_death,population_type_list = ["younger","older"]):

    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days))


    first_wave_vax_coverage = [0.2,0.5,0.8]
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    # third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"]
    plot_save =["no_more_vax","early_vax","reactive_vax"]

    wavestart_list =  ['start_wave_2','start_wave_3']
    folder_start_list = [folder_start_wave_2,folder_start_wave_3]
    presim_parameters_folder_start_list = [presim_parameters_folder_start_wave_2,presim_parameters_folder_start_wave_3]

    TP_reduced_list =  [TP_low, TP_high]
    TP_type_list = ['TP_low','TP_high']

    # TP_segregated_list = [TP_low,TP_mid,TP_high]

    for wavestart, folder_start, presim_parameters_folder_start in zip(wavestart_list,folder_start_list,presim_parameters_folder_start_list):

        for third_vaccination_type_here, plot_save_here in zip(third_vaccination_type_list,plot_save):

            for population_type in population_type_list :
            
                for TP_type, local_TP_list in zip(TP_type_list,TP_reduced_list):

                    all_severe_disease_wave_3 = {0:[],0.2:[],0.5:[],0.8:[]}

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
                        if total_vaccination_rate==0 or third_vaccination_type ==third_vaccination_type_here:
                            pass 
                        else:
                            continue
                            
                        for TP in local_TP_list:

                            filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                            
                            severe_disease_wave_3 = []

                            clinical_filename = "_full_outcomes_dataframe.csv"
                            clinical_file = os.path.join(folder_start,filename,clinical_filename)

                            if os.path.isfile(clinical_file):
                                pass
                            else:
                                print(clinical_file +" DOES NOT EXIST!")
                                continue


                            clinical_pd_obj = pd.read_csv(clinical_file)

                            scale = 40
                            aug_num = 5
                            for simnum in range(1,SIM_NUMBER+1):
                                for aug in range(1,aug_num+1):
                                    
                                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_wave_3))]
                                    
                                    if ICU_or_death == 'death':
                                        daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                        severe_disease_wave_3.append(daily_deaths)
                                    elif ICU_or_death =='ICU':
                                        daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                        severe_disease_wave_3.append(daily_ICU_admissions)
                            
                            all_severe_disease_wave_3[total_vaccination_rate].extend(severe_disease_wave_3)
                            
            
                    fig, ax = plt.subplots(1,1, figsize=(6,4))

                    plot_position = []
                    plot_label = []
                    position = 1
                    for vax_cov in [0,0.2,0.5,0.8]:
                        if population_type == "younger":
                            if vax_cov == 0.2:
                                plot_colour = 'lightskyblue'
                                outline= 'lightskyblue'
                            elif vax_cov == 0.5:
                                plot_colour = 'dodgerblue'
                                outline = 'dodgerblue'
                            elif vax_cov == 0.8:
                                plot_colour = 'navy'
                                outline = 'navy'
                            else:
                                plot_colour = "white"
                                outline ='lightskyblue'
                        else:
                            if vax_cov == 0.2:
                                plot_colour = 'salmon'
                                outline = 'salmon'
                            elif vax_cov == 0.5:
                                plot_colour = 'red'
                                outline = 'red'
                            elif vax_cov == 0.8:
                                plot_colour = 'firebrick'
                                outline = 'firebrick'
                            else:
                                plot_colour = "white"
                                outline='salmon'
                        
                        plot_position.append(position)
                        plot_label.append(str(round(vax_cov*100,0))+"\% vaccination")

                        data_to_plot = [all_severe_disease_wave_3[vax_cov]]
                        parts = ax.violinplot(data_to_plot,[position], showmeans=False, showmedians=False, showextrema=False,vert=False)
                        for pc in parts['bodies']:
                            pc.set_facecolor(plot_colour)
                            pc.set_edgecolor(outline)
                            pc.set_alpha(0.9)
                        
                        position-=1
                                    
                    ax.grid(color='#878787', linestyle=(0, (5, 1)))
                    ax.set_facecolor('silver')
                    ax.set_axisbelow(True)

                    ax.axvline(x =0, color = 'black')
                
                    # ax.set_yticks(plot_position,labels= plot_label)
                    ax.set_yticks(plot_position,labels= plot_label)
                    # ax.set_xlim(-2,80)
                    ax.set_xlim(0,80)
                    
                    if len(population_type_list)==2:
                        addition = "combined"
                    else:
                        addition = population_type_list[0]  

                    if ICU_or_death == 'death':
                        # ax.set_ylabel('third wave deaths')
                        # ax.set_title('Third wave deaths')
                        ax.set_xlabel('third wave deaths')
                        
                    elif ICU_or_death =='ICU':
                        # ax.set_ylabel('third wave ICU admissions')
                        ax.set_title('Third wave ICU admissions')

                    plt.savefig(os.path.join(folder_start,"violin_scenarios_wave_start_"+ wavestart+"_" + plot_save_here+"_"+ TP_type + "_" +ICU_or_death+"_vs_past_immunity_"+addition+".png") , bbox_inches='tight')
                    plt.close()
            



def plot_comparison_third_wave_ICU_and_deaths_given_scenario_wavestart_TP(folder_start_wave_2,presim_parameters_folder_start_wave_2,folder_start_wave_3,presim_parameters_folder_start_wave_3, ICU_or_death,population_type_list = ["younger","older"]):

    days_wave_1 = list(range(0,second_exposure_time))
    days_wave_2 = list(range(second_exposure_time,third_exposure_time ))
    days_wave_3 = list(range(third_exposure_time,max_days))


    first_wave_vax_coverage = [0.2,0.5,0.8]
    third_vaccination_type_list = ["no further vaccination", "additional early vaccination", "reactive (delayed) vaccination"]
    third_vaccination_types_wanted = ["no further vaccination", "reactive (delayed) vaccination"]

    wavestart_list =  ['start_wave_2','start_wave_3']
    folder_start_list = [folder_start_wave_2,folder_start_wave_3]
    presim_parameters_folder_start_list = [presim_parameters_folder_start_wave_2,presim_parameters_folder_start_wave_3]

    TP_reduced_list =  [TP_low, TP_high]
    TP_type_list = ['TP_low','TP_high']

    # TP_segregated_list = [TP_low,TP_mid,TP_high]
    for population_type in population_type_list :

        for wavestart, folder_start, presim_parameters_folder_start in zip(wavestart_list,folder_start_list,presim_parameters_folder_start_list):
            for TP_type, local_TP_list in zip(TP_type_list,TP_reduced_list):

                all_deaths = {0.2:{},0.5:{},0.8:{}}
                for vax_cov in [0.2,0.5,0.8]:
                    all_deaths[vax_cov] = {"no further vaccination":[],"reactive (delayed) vaccination":[]}

        
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
                    if total_vaccination_rate in first_wave_vax_coverage and third_vaccination_type in third_vaccination_types_wanted:
                        pass 
                    else:
                        continue

                    for TP in local_TP_list:

                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                        
                        
                        severe_disease_wave_3 = []

                        clinical_filename = "_full_outcomes_dataframe.csv"
                        clinical_file = os.path.join(folder_start,filename,clinical_filename)

                        if os.path.isfile(clinical_file):
                            pass
                        else:
                            print(clinical_file +" DOES NOT EXIST!")
                            continue


                        clinical_pd_obj = pd.read_csv(clinical_file)

                        scale = 40
                        aug_num = 5
                        for simnum in range(1,SIM_NUMBER+1):
                            for aug in range(1,aug_num+1):
                                
                                new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_wave_3))]
                                
                                if ICU_or_death == 'death':
                                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                    severe_disease_wave_3.append(daily_deaths)
                                elif ICU_or_death =='ICU':
                                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                    severe_disease_wave_3.append(daily_ICU_admissions)
                        
                        all_deaths[total_vaccination_rate][third_vaccination_type].extend(severe_disease_wave_3)
                pairwise_differences =  {0.2:[],0.5:[],0.8:[]}
                for vax_cov in [0.2,0.5,0.8]:
                    no_further_vax = all_deaths[vax_cov]["no further vaccination"]
                    reactive_vax = all_deaths[vax_cov]["reactive (delayed) vaccination"]
                    difference_list = []
                    for rv_i in reactive_vax:
                        for nfv_i in no_further_vax:
                            difference =nfv_i  - rv_i
                            difference_list.append(difference)
                    pairwise_differences[vax_cov].extend(difference_list)
                
                fig, ax = plt.subplots(1,1, figsize=(6,4))

                plot_position = []
                plot_label = []
                position = 1 

                for vax_cov in [0.2,0.5,0.8]:
                    if population_type == "younger":
                        if vax_cov == 0.2:
                            plot_colour = 'lightskyblue'
                            outline= 'lightskyblue'
                        elif vax_cov == 0.5:
                            plot_colour = 'dodgerblue'
                            outline = 'dodgerblue'
                        elif vax_cov == 0.8:
                            plot_colour = 'navy'
                            outline = 'navy'
                    else:
                        if vax_cov == 0.2:
                            plot_colour = 'salmon'
                            outline = 'salmon'
                        elif vax_cov == 0.5:
                            plot_colour = 'red'
                            outline = 'red'
                        elif vax_cov == 0.8:
                            plot_colour = 'firebrick'
                            outline = 'firebrick'
                    

                    plot_position.append(position)
                    plot_label.append(str(vax_cov*100)+"\% vaccination")

                    data_to_plot = [pairwise_differences[vax_cov]]
                    parts = ax.violinplot(data_to_plot,[position],showmeans=False, showmedians=False, showextrema=False,vert=False) # 
                    for pc in parts['bodies']:
                        pc.set_facecolor(plot_colour)
                        pc.set_edgecolor(outline)
                        pc.set_alpha(0.9)

                        position-=1
                                
                ax.grid(color='#878787', linestyle=(0, (5, 1)))
                ax.set_facecolor('silver')
                ax.set_axisbelow(True)

                ax.axvline(x =0, color = 'black')
            
                ax.set_yticks(plot_position,labels= plot_label)
                # ax.set_xlim(-2,80)
                ax.set_xlim(-40,40)
                
                if len(population_type_list)==2:
                    addition = "combined"
                else:
                    addition = population_type_list[0]  

                if ICU_or_death == 'death':
                    # ax.set_ylabel('third wave deaths')
                    # ax.set_title('Third wave deaths')
                    ax.set_xlabel('difference in third wave deaths (no further vaccination - reactive vaccination)')
                    
                elif ICU_or_death =='ICU':
                    # ax.set_ylabel('third wave ICU admissions')
                    ax.set_title('Third wave ICU admissions')

                plt.savefig(os.path.join(folder_start,ICU_or_death+"_differences_violin_scenarios_wave_start_"+ wavestart+"_" +"_vs_past_immunity_"+addition+"_"+ TP_type + "_" +".png") , bbox_inches='tight')
                plt.close()
                




################################################################################################
# PLOTTING Waves: BA1, BA4/5, BA4/5
################################################################################################

folder = '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/'
presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files/'

# plot_combined_infections_over_time_80_booster(younger_or_older=["younger"],line_color="coloured")

# plot_combined_infections_over_time_80_booster(younger_or_older=["older"],line_color="coloured")

# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,65],x_limits=[19,81],filter=True,aspect_ratio = 'equal',past_waves=[1],future_waves=[2])
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],y_limits = [-1,65],x_limits=[19,81],filter=True,aspect_ratio = 'equal',past_waves=[1],future_waves=[2])

#>>>> not exactly right at the moment (should move the legend if I actually want these plots)
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,100],x_limits=[0,150],filter=False,aspect_ratio = 'equal',past_waves=[1,2],future_waves=[3])
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],y_limits = [-1,100],x_limits=[0,150],filter=False,aspect_ratio = 'equal',past_waves=[1,2],future_waves=[3])

#>>>> not exactly right: should add a line from the point down to the plane for ease...
# or even change it so that each figure is a different 1st wave vaccination rate
# plot_attack_rates_3D(population_type_list = ["younger"],x_limits=[-1,100],y_limits = [-1,100],z_limits = [-1,100])
# plot_attack_rates_3D(population_type_list = ["older"],x_limits=[-1,100],y_limits = [-1,100],z_limits = [-1,100])


# plot_wave_2_and_3_given_wave_1(population_type_list = ["younger"],x_limits=[-1,100],y_limits = [-1,100],aspect_ratio = 'equal')
# plot_wave_2_and_3_given_wave_1(population_type_list = ["older"],x_limits=[-1,100],y_limits = [-1,100],aspect_ratio = 'equal')


# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"],ylimits=[-1,30],y_ticks = list(range(0,31,5)),x_limits=[19,81],filter=True,past_waves=[1],future_waves=[2])
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["older"],ylimits=[-1,30],y_ticks = list(range(0,31,5)),x_limits=[19,81],filter=True,past_waves=[1],future_waves=[2])

# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[0,150],filter=False,past_waves=[1,2],future_waves=[3])
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["older"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[0,150],filter=False,past_waves=[1,2],future_waves=[3])


# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["younger"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True,past_waves=[1],future_waves=[2])
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["older"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True,past_waves=[1],future_waves=[2])


# plot_third_wave_ICU_and_deaths_given_second_and_first_wave("death",OG="",population_type_list = ["younger"],ylimits = [0,50],y_ticks = list(range(0,50,2)),x_limits=[0,100])
# plot_third_wave_ICU_and_deaths_given_second_and_first_wave("death",OG="",population_type_list = ["older"],ylimits = [0,50],y_ticks = list(range(0,50,2)),x_limits=[0,100])

# plotting after Monday 21st November 2022 meeting:

# plot_separated_infections_over_time(younger_or_older=["younger"])
# plot_separated_infections_over_time(younger_or_older=["older"])

# plot_ribbon_infections_over_time(younger_or_older=["younger"])
# plot_ribbon_infections_over_time(younger_or_older=["older"])


# plot_attack_rates_3D_animated_combined(population_type_list = ["younger"],x_limits=[0,100],y_limits = [0,100],z_limits = [0,120])

# plot_attack_rates_3D_animated(population_type_list = ["younger"],x_limits=[0,100],y_limits = [0,100],z_limits = [0,100])
# plot_attack_rates_3D_animated(population_type_list = ["older"],x_limits=[-1,100],y_limits = [-1,100],z_limits = [-1,100])


# plot_violin_infections_over_time(younger_or_older=["younger"])
# plot_violin_infections_over_time(younger_or_older=["older"])

################################################################################################
# PLOTTING Waves: BA1, BA1, BA4/5
################################################################################################

folder = '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/'
presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files/'

# plot_combined_infections_over_time_80_booster(younger_or_older=["younger"],line_color="coloured")

# plot_combined_infections_over_time_80_booster(younger_or_older=["older"],line_color="coloured")

# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,100],x_limits=[19,81],filter=True,aspect_ratio = 'equal',past_waves=[1],future_waves=[2])
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],y_limits = [-1,100],x_limits=[19,81],filter=True,aspect_ratio = 'equal',past_waves=[1],future_waves=[2])


# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,100],x_limits=[0,150],filter=False,aspect_ratio = 'equal',past_waves=[1,2],future_waves=[3])
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],y_limits = [-1,100],x_limits=[0,150],filter=False,aspect_ratio = 'equal',past_waves=[1,2],future_waves=[3])


# plot_attack_rates_3D(population_type_list = ["younger"],x_limits=[-1,100],y_limits = [-1,100],z_limits = [-1,100])
# plot_attack_rates_3D(population_type_list = ["older"],x_limits=[-1,100],y_limits = [-1,100],z_limits = [-1,100])


# plot_wave_2_and_3_given_wave_1(population_type_list = ["younger"],x_limits=[-1,100],y_limits = [-1,100],aspect_ratio = 'equal')
# plot_wave_2_and_3_given_wave_1(population_type_list = ["older"],x_limits=[-1,100],y_limits = [-1,100],aspect_ratio = 'equal')



# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True,past_waves=[1],future_waves=[2])
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["older"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True,past_waves=[1],future_waves=[2])

# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[0,150],filter=False,past_waves=[1,2],future_waves=[3])
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["older"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[0,150],filter=False,past_waves=[1,2],future_waves=[3])


# plot_third_wave_ICU_and_deaths_given_second_and_first_wave("death",OG="",population_type_list = ["younger"],ylimits = [0,50],y_ticks = list(range(0,50,2)),x_limits=[0,100])
# plot_third_wave_ICU_and_deaths_given_second_and_first_wave("death",OG="",population_type_list = ["older"],ylimits = [0,50],y_ticks = list(range(0,50,2)),x_limits=[0,100])


# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["younger"],ylimits=[0,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["older"],ylimits=[0,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)

# plotting after Monday 21st November 2022 meeting:

# plot_separated_infections_over_time(younger_or_older=["younger"])
# plot_separated_infections_over_time(younger_or_older=["older"])

# plot_ribbon_infections_over_time(younger_or_older=["younger"])
# plot_ribbon_infections_over_time(younger_or_older=["older"])

# plot_attack_rates_3D_animated(population_type_list = ["younger"],x_limits=[0,100],y_limits = [0,100],z_limits = [0,100])
# plot_attack_rates_3D_animated(population_type_list = ["older"],x_limits=[-1,100],y_limits = [-1,100],z_limits = [-1,100])

# plot_violin_infections_over_time(younger_or_older=["younger"])
# plot_violin_infections_over_time(younger_or_older=["older"])

folder = '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/'
presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files/'

# plot_comparison_third_wave_ICU_and_deaths_given_scenario(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["younger"])

# plot_comparison_third_wave_ICU_and_deaths_given_scenario(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["older"])


# plot_comparison_third_wave_ICU_and_deaths_given_scenario_wavestart(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["younger"])

# plot_comparison_third_wave_ICU_and_deaths_given_scenario_wavestart(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["older"])


# plot_comparison_third_wave_ICU_and_deaths_given_scenario_breakdown_wavestart(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["younger"])

# plot_comparison_third_wave_ICU_and_deaths_given_scenario_breakdown_wavestart(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["older"])


plot_comparison_third_wave_ICU_and_deaths_given_scenario_wavestart_TP(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["younger"])

plot_comparison_third_wave_ICU_and_deaths_given_scenario_wavestart_TP(folder_start_wave_2='/scratch/cm37/tpl/covid_BA1_BA45_wave_start_2_outputs/',presim_parameters_folder_start_wave_2=presim_parameters_folder ,folder_start_wave_3= '/scratch/cm37/tpl/covid_BA1_BA45_wave_start_3_outputs/',presim_parameters_folder_start_wave_3=presim_parameters_folder , ICU_or_death="death",population_type_list = ["older"])