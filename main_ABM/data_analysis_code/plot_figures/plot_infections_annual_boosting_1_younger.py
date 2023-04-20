#
# Produces plots for the younger population lower-coverage scenarios, i.e. scenarios 5 (= 15), 6 (=13), 14, 16.
#

import os
import pandas as pd
import json
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

TP_list = ["1.05", "1.95"]
TP_low = ["1.05"]
TP_high = ["1.95"]
TP_segregated_list = [TP_low,TP_high]

param_list = list(range(-1,6+1))
# novax_index = 0
# SIM_NUMBER = 100

max_days = 52*3*7 # 3 years 
first_exposure_time =225

original_program_time = 26*7*3
boosters_only_vaccination_start_list = [original_program_time + 26*7]
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

date_values = list(range(0,max_days,10))
date_names = [str(x) for x in date_values]

# days = list(range(0,max_days+1))
local_days = list(range(max_days))

no_boosting_colour = 'white'
pedatric_boosting_colour = 'lightskyblue'
old_boosting_colour ='dodgerblue'
random_boosting_colour = 'navy' # technically the new primary boosting 


def plot_ribbon_infections_over_time_plus(younger_or_older=["older"],immune_escape_time=546):
    max_infections=5000 

    BA1_colour = '#a1a1a1'
    BA45_colour = "#666666"
    vaccinating_colour = "yellowgreen"
    boosting_colour_general = "darkgreen"

    for boosting_time in boosters_only_vaccination_start_list:

        for local_TP_list in TP_segregated_list:

            for vaccination_coverage  in [0.2,0.5]:

                # fig, ax = plt.subplots(1,1, figsize=(8,3.5)) #10,4  # 16:9
                fig, (ax, ax2) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [6, 1]},figsize = (8,4.5))

                legend0 = []
                marker = "s"
                # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]
                legend0.append(ax.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
                legend0.append(ax.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
                legend0.append(ax.scatter(-10000,-10000,color=vaccinating_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
                legend0.append(ax.scatter(-10000,-10000,color=boosting_colour_general, s=100, marker= marker, alpha=1.0, edgecolors='none'))


                legend_points = []
                marker='o'

                for population_type in younger_or_older:

                    if population_type=="younger":
                        legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
                        legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                        # legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
                        # legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        # legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        # legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    if population_type=="older":
                        
                        legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
                        legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                        # legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
                        # legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        # legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                        # legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                    all_curves_over_local_days = {'none':[], '5-15':[], '65+':[],'primary' :[]}

                    for paramNum in param_list:

                        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                        presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                        with open(presimfilename, "r") as f:
                            presim_parameters = json.load(f)

                        # total_population = presim_parameters["total_population"]
                        # population_type = presim_parameters["population_type"]
                        total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                        # booster_fraction = presim_parameters["booster_fraction"]
                        boosting_group = presim_parameters['boosting_group']
                        sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                        if boosting_time == sims_boosting_time or boosting_group=='none':
                            pass
                        else:
                            continue 

                        if total_vaccination_rate!= vaccination_coverage:
                            continue
                        else:
                            pass

                        for TP in local_TP_list:
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
                                all_curves_over_local_days[boosting_group].append(infections_over_time_list)

                                # ax.plot(local_days,infections_over_time_list,alpha=1,color=plot_colour)
                    upper_ribbon = {'none':[], '5-15':[], '65+':[],'primary' :[]} # for vaccinated groups
                    lower_ribbon = {'none':[],'5-15':[], '65+':[],'primary' :[]}
                    median_line = {'none':[],'5-15':[], '65+':[],'primary':[]}

                    for boosting_group in ['none', '5-15','65+','primary']:
                        upper_ribbon[boosting_group] = [max([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
                        lower_ribbon[boosting_group] = [min([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
                        median_line[boosting_group] = [np.median([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
                    for boosting_group in ['none', '5-15','65+','primary']:
                        if population_type == "younger":
                            if boosting_group == '5-15':
                                plot_colour = pedatric_boosting_colour
                            elif boosting_group == '65+':
                                plot_colour = old_boosting_colour
                            elif boosting_group == 'primary':
                                plot_colour = random_boosting_colour
                            elif boosting_group =='none':
                                plot_colour = no_boosting_colour
                        else:
                            pass 
                            # if boosting_group == '5-15':
                            #     plot_colour = pedatric_boosting_colour
                            # elif boosting_group == '65+':
                            #     plot_colour = old_boosting_colour
                            # elif boosting_group == 'random':
                            #     plot_colour = random_boosting_colour
                        
                        ax.fill_between(local_days,upper_ribbon[boosting_group],lower_ribbon[boosting_group],facecolor=plot_colour,alpha=0.5)
                        # ax.plot(local_days,median_line[vax],color = plot_colour,linestyle='solid')
                    for boosting_group in ['none', '5-15','65+','primary']:
                        if population_type == "younger":
                            if boosting_group == '5-15':
                                plot_colour = pedatric_boosting_colour
                            elif boosting_group == '65+':
                                plot_colour = old_boosting_colour
                            elif boosting_group == 'primary':
                                plot_colour = random_boosting_colour
                            elif boosting_group =='none':
                                plot_colour = no_boosting_colour
                        else:
                            pass
                            # if boosting_group == '5-15':
                            #     plot_colour = pedatric_boosting_colour
                            # elif boosting_group == '65+':
                            #     plot_colour = old_boosting_colour
                            # elif boosting_group == 'random':
                            #     plot_colour = random_boosting_colour
                        # ax.fill_between(local_days,upper_ribbon[vax],lower_ribbon[vax],facecolor=plot_colour,alpha=0.5)
                        ax.plot(local_days,median_line[boosting_group],color = plot_colour,linestyle='solid')

                # average_days_per_month = 30.437
                # months_on_day = [i*average_days_per_month for i in range(30) ]
                # months_numbering = list(range(0,len(months_on_day ),1))
                # ax.set_xticks(months_on_day)
                # ax.set_xticklabels(months_numbering)
                # ax2.set_xlabel('time (months-ish)') # ax.set_xlabel('time (months-ish)')
                
                days_per_year = 52*7 
                days_per_six_months = 26*7
                six_months_on_day = [i*days_per_six_months for i in range(7) ]
                x_tick_labels = ["0", "0.5", "1","1.5","2","2.5","3"]
                ax.set_xticks(six_months_on_day)
                ax.set_xticklabels(x_tick_labels)
                ax2.set_xlabel('time (years)')

                ax.set_ylim([0,max_infections])
                ax.set_xlim([min(local_days),max_days])
                # ax.set_xlabel('time (days)')
                ax.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8)
                ax2.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
                
                arrow_len = -500
                arrow_pos = 700 - arrow_len
                ax.arrow(x=first_exposure_time, y=arrow_pos, dx=0, dy=arrow_len, width=2, head_width=15, head_length=100,facecolor='white', edgecolor='none')
                ax.annotate('importations begin', xy = (first_exposure_time-5, arrow_pos+150),rotation=90,color="white",size=14)

                

                # ax.set_facecolor('silver')
                ax.set_facecolor(BA1_colour)
                ax.axvspan(immune_escape_time,max_days,facecolor=BA45_colour ,zorder=0)
                ax.axvspan(0,first_exposure_time,facecolor="#cfcfcf",zorder=0)

                # little vaccination bar 
                ax2.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)
                ax2.axvspan(boosting_time,boosting_time+13*7,facecolor= boosting_colour_general,zorder=0)
                ax2.set_yticklabels([])

                ax2.legend(legend0, ["circulating BA.1","circulating BA.4/5", "main vaccinaton program","further vaccination program"],bbox_to_anchor=(1.01,-0.1), loc="lower left",borderaxespad=0,frameon=False)

                leg = Legend(ax, legend_points, ["no further boosting", "new pediatric vaccination (ages 5-15)","high risk boosting (65+ first)", "new primary vaccinations"],title=younger_or_older[0] +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
                leg._legend_box.align = "left"
                ax.add_artist(leg)
                
                ax.set_ylabel('number of infections')
                
                plt.savefig(os.path.join(folder, "ribbon_infections_over_time_plus_"+younger_or_older[0]+ "_vax_"+str(vaccination_coverage)+ "_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) + ".png") , bbox_inches='tight')
                plt.close()


def plot_before_vs_after_infections(boosting_time,population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],aspect_ratio = 'equal',cut_time = original_program_time):
    # third_stage_vaccination = "none", "early","reactive"

    days_before = list(range(0,cut_time))
    days_after = list(range(cut_time,max_days))
    for local_TP_list in TP_segregated_list:

        for vaccination_coverage in [0.2,0.5]:

            for population_type in population_type_list:



                if y_limits[1]>80:
                    fig, ax = plt.subplots(1,1, figsize=(8,7.75)) # for the second strain
                else:
                    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
                
                # first, some plotting to get some fake legends...
                legend_points = []
                marker='o'

            
                if population_type=="younger":
                    legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
                    legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                if population_type=="older":
                    legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            
                for paramNum in param_list:
                    presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                    presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                    with open(presimfilename, "r") as f:
                        presim_parameters = json.load(f)

                    total_population = presim_parameters["total_population"]
                    # population_type = presim_parameters["population_type"]
                    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                    booster_fraction = presim_parameters["booster_fraction"]
                    boosting_group = presim_parameters['boosting_group']
                    sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                    if boosting_time == sims_boosting_time or boosting_group =='none':
                        pass
                    else:
                        continue

                    if vaccination_coverage!= total_vaccination_rate:
                        continue
                    else:
                        pass 
                    
                    for TP in local_TP_list:

                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                    
                    
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


                        outline = 'None'
                        percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                        percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                        if boosting_group == '5-15':
                            plot_colour = pedatric_boosting_colour
                        elif boosting_group == '65+':
                            plot_colour = old_boosting_colour
                        elif boosting_group == 'primary' or boosting_group=='random':
                            plot_colour = random_boosting_colour
                        elif boosting_group=='none':
                            plot_colour = no_boosting_colour

                        ax.scatter( percent_infected_before, percent_infected_after,color=plot_colour, s=scale,  marker= marker, alpha=0.8, edgecolors=outline)
                        
                ax.plot([0, 100], [0, 100],linestyle='--',color="black")
                
                ax.set_xlim(x_limits)
                ax.set_ylim(y_limits)

                y_ticks = list(range(0,max(y_limits)+1,20))
                ax.set_yticks(y_ticks)
                ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

                x_ticks = list(range(0,max(x_limits)+1,20))
                ax.set_xticks(x_ticks)
                ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

                ax.set_aspect(aspect_ratio)
                # ax.grid(True)
                ax.set_axisbelow(True)
                ax.grid(color='gray')
                # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

                leg = Legend(ax, legend_points, ["no further boosting", "new pediatric vaccination (ages 5-15)","high risk boosting (65+ first)", "new primary vaccinations"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
                leg._legend_box.align = "left"
                ax.add_artist(leg)

                ax.set_ylabel('future attack rate (t = ' + str(days_after[0])+' to ' + str(days_after[-1])+')')
                ax.set_xlabel('past attack rate (before t = '+str(days_before[-1]+1) +')')
                

                # xticks = [15,20,30,40,50,60,70,80,85]
                xticks = x_ticks
                for x0, x1 in zip(xticks[::2], xticks[1::2]):
                    plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

                # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

                plt.savefig(os.path.join(folder, "past_vs_future_waves_infections_"+ population_type +"_vax_"+str(vaccination_coverage) +"_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) +"_cut-time-"+str(cut_time) +".png") , bbox_inches='tight')
                plt.close()


def total_infections_and_deaths_histograms(boosting_time,ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):

    for vaccination_coverage in [0.2,0.5]:

        for local_TP_list in TP_segregated_list:
            
            for population_type in younger_or_older:

                fig, (ax, ax2) = plt.subplots(2, figsize=(8,4))

                legend_points = []
                marker = "o" # "s"

                if population_type=="older" or population_type=="younger":
                    legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
                    legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                total_infections_local_days =  {'none':[], '5-15':[], '65+':[],'primary' :[]}
                total_severe_disease_local_days = {'none':[],'5-15':[], '65+':[],'primary' :[]}

                for paramNum in param_list:

                    presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                    presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                    with open(presimfilename, "r") as f:
                        presim_parameters = json.load(f)

                    # total_population = presim_parameters["total_population"]
                    # population_type = presim_parameters["population_type"]
                    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                    booster_fraction = presim_parameters["booster_fraction"]
                    boosting_group = presim_parameters['boosting_group']
                    sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                    if boosting_time == sims_boosting_time or boosting_group=='none':
                        pass
                    else:
                        continue 

                    if vaccination_coverage!= total_vaccination_rate:
                        continue
                    else:
                        pass 

                    for TP in local_TP_list:

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

                        clinical_filename = "_full_outcomes_dataframe.csv"
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
                            total_infections = sum(list_conversion_nans(infections_over_time, timeframe ))
                            total_infections_local_days[boosting_group].append(total_infections ) 

                            for aug in range(1,aug_num+1):
                                new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]
                                
                                if ICU_or_death == 'death':
                                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                    total_severe_disease_local_days[boosting_group].append(daily_deaths) 
                                elif ICU_or_death =='ICU':
                                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                    total_severe_disease_local_days[boosting_group].append(daily_ICU_admissions) 
                
                
                outline = 'none'
                for boosting_group in ['none', '5-15','65+','primary']:
                    if population_type == "younger":
                        if boosting_group == '5-15':
                            plot_colour = pedatric_boosting_colour
                        elif boosting_group == '65+':
                            plot_colour = old_boosting_colour
                        elif boosting_group == 'primary':
                            plot_colour = random_boosting_colour
                        elif boosting_group == 'none':
                            plot_colour = no_boosting_colour
                    else:
                        if boosting_group == '5-15':
                            plot_colour = pedatric_boosting_colour
                        elif boosting_group == '65+':
                            plot_colour = old_boosting_colour
                        elif boosting_group == 'primary':
                            plot_colour = random_boosting_colour
                    
                    ax.hist(total_infections_local_days[boosting_group], bins=10, alpha=0.5, color=plot_colour)

                    ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, alpha=0.5, color=plot_colour)


                ax.set_ylabel('Count')
                ax.set_xlim(0,360000)
                ax.set_ylim(0,20)
                # ax.set_xlim([min(local_days),max_days])
                ax.grid(color='#878787', linestyle=(0, (5, 1)))
                ax.set_facecolor('silver')
                ax.set_axisbelow(True)

                ax.set_xlabel("Total infections (t = " + str(timeframe[0])+" to " + str(timeframe[-1])+")")
                # ax.set_xlim(0,200000)

                # ax2.set_title("For ages >= " + str(minimum_age))

                ax2.set_ylabel('Count')
                ax2.set_xlim(0,140)
                if ICU_or_death == 'death':
                    if minimum_age==65:
                        ax2.set_xlabel("Deaths in the 65+ age-group (t = " + str(timeframe[0])+" to " + str(timeframe[-1])+")")
                    else:
                        ax2.set_xlabel("Total deaths (t = " + str(timeframe[0])+" to " + str(timeframe[-1])+")")
                elif ICU_or_death =='ICU':
                    ax2.set_xlabel("Total ICU Admissions (t = " + str(timeframe[0])+" to " + str(timeframe[-1])+")")
                
                # ax2.set_xlim(0,1000)
                ax2.grid(color='#878787', linestyle=(0, (5, 1)))
                ax2.set_facecolor('silver')


                leg = Legend(ax, legend_points, ["no further boosting","new pediatric vaccination (ages 5-15)","high risk boosting (65+ first)", "new primary vaccinations"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
                leg._legend_box.align = "left"
                ax.add_artist(leg)
                
                plt.subplots_adjust(hspace=0.5)
                
                plt.savefig(os.path.join(folder, "total_infections_and_" + ICU_or_death+"_histogram_"+population_type+"_vax_" + str(vaccination_coverage)+"_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) +"_time"+str(timeframe[0])+"-" + str(timeframe[-1])+"_minimum-age-"+str(minimum_age)+  ".png") , bbox_inches='tight')
                plt.close()



def total_deaths_histograms_with_mean(boosting_time,immune_escape_time,ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):
    BA1_colour = '#a1a1a1'
    BA45_colour = "#666666"
    vaccinating_colour = "yellowgreen"
    boosting_colour_general = "darkgreen"

    for vaccination_coverage in [0.2,0.5]:

        for local_TP_list in TP_segregated_list:
            
            for population_type in younger_or_older:

                fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [7, 1,1],'width_ratios':[3,3]}, figsize=(13,5))
                # fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [6, 1,1],'width_ratios':[3,2]}, figsize=(10,4))
                ax_table.axis("off")
                ax5.axis("off")
                ax6.axis("off")

                legend_points = []
                marker = "o" # "s"

                # if population_type=="older" or population_type=="younger":
                #     legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
                #     legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                # total_infections_local_days =  {'none':[], '5-15':[], '65+':[],'primary' :[]}
                total_severe_disease_local_days = {'none':[],'5-15':[], '65+':[],'primary' :[]}
                total_severe_disease_statistics = {'none':[],'5-15':[], '65+':[],'primary' :[]}

                for paramNum in param_list:

                    presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                    presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                    with open(presimfilename, "r") as f:
                        presim_parameters = json.load(f)

                    # total_population = presim_parameters["total_population"]
                    # population_type = presim_parameters["population_type"]
                    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                    # booster_fraction = presim_parameters["booster_fraction"]
                    boosting_group = presim_parameters['boosting_group']
                    sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                    if boosting_time == sims_boosting_time or boosting_group=='none':
                        pass
                    else:
                        continue 

                    if vaccination_coverage!= total_vaccination_rate:
                        continue
                    else:
                        pass 

                    for TP in local_TP_list:

                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                        print(filename)

                        datafilename = filename + ".csv"

                        clinical_filename = "_full_outcomes_dataframe.csv"
                        clinical_file = os.path.join(folder,filename,clinical_filename)

                        if os.path.isfile(clinical_file):
                            pass
                        else:
                            print(clinical_file +" DOES NOT EXIST!")
                            continue

                        clinical_pd_obj = pd.read_csv(clinical_file)

                        clinical_pd_obj = clinical_pd_obj.loc[(clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]

                        clinical_pd_obj = clinical_pd_obj.groupby(['iteration']).agg({'daily_ICU_admissions':'sum','daily_deaths':'sum'}).reset_index()

                        print("=============clinical_pd_obj")
                        print(clinical_pd_obj)

                        if ICU_or_death == 'death':
                            daily_deaths = clinical_pd_obj['daily_deaths'].to_list()
                            total_severe_disease_local_days[boosting_group] = daily_deaths
                            print("=============daily deaths")
                            print(daily_deaths)
                        elif ICU_or_death =='ICU':
                            daily_ICU_admissions =clinical_pd_obj['daily_ICU_admissions'].to_list()
                            total_severe_disease_local_days[boosting_group] = daily_ICU_admissions
                
                
                outline = 'none'
                for boosting_group in ['none', '5-15','65+','primary']:
                    if population_type == "younger":
                        if boosting_group == '5-15':
                            plot_colour = pedatric_boosting_colour
                        elif boosting_group == '65+':
                            plot_colour = old_boosting_colour
                        elif boosting_group == 'primary':
                            plot_colour = random_boosting_colour
                        elif boosting_group == 'none':
                            plot_colour = no_boosting_colour
                    else:
                        if boosting_group == '5-15':
                            plot_colour = pedatric_boosting_colour
                        elif boosting_group == '65+':
                            plot_colour = old_boosting_colour
                        elif boosting_group == 'primary':
                            plot_colour = random_boosting_colour
                    mean = np.mean(total_severe_disease_local_days[boosting_group])
                    median = np.median(total_severe_disease_local_days[boosting_group])
                    lower_quantile = np.quantile(total_severe_disease_local_days[boosting_group],0.025)
                    upper_quantile = np.quantile(total_severe_disease_local_days[boosting_group],0.975)
                    total_severe_disease_statistics[boosting_group] = [median,lower_quantile,upper_quantile,mean]

                    ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, alpha=0.5, color=plot_colour,histtype='bar')
                    ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, facecolor="none", edgecolor=plot_colour, histtype='step')

                ax2.set_ylabel('Count')
                ax2.set_xlim(0,110)
                ax2.set_ylim(bottom=0,top=1750)
                if ICU_or_death == 'death':
                    if minimum_age==65:
                        ax2.set_xlabel("Deaths in the 65+ age-group (t = " + str(timeframe[0])+" to " + str(timeframe[-1])+")")
                    else:
                        ax2.set_xlabel("Total deaths between " + str(round(timeframe[0]/(52*7),2))+" - " + str(round(timeframe[-1]/(52*7),2))+" years")
                elif ICU_or_death =='ICU':
                    ax2.set_xlabel("Total ICU Admissions (t = " + str(timeframe[0])+" to " + str(timeframe[-1])+")")
                
                # ax2.set_xlim(0,1000)
                ax2.grid(color='#878787', linestyle=(0, (5, 1)))
                ax2.set_facecolor('silver')


                # leg = Legend(ax, legend_points, ["no further boosting","new pediatric vaccination (ages 5-15)","high risk boosting (65+ first)", "new primary vaccinations"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
                # leg._legend_box.align = "left"
                # ax.add_artist(leg)

                print(total_severe_disease_statistics)
        
                columns = ("Mean","Median","95\% quantiles")
                rows =  ["no further boosting","new pediatric vaccination (ages 5-15)","high risk boosting (65+ first)", "new primary vaccinations"]

                colors = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
                cell_text = [[round(values[3],2),round(values[0],2),(round(values[1],2),round(values[2],2))] for boosting_group,values in total_severe_disease_statistics.items()]

                ####### table of statistics instead of legend 
                the_table = ax_table.table(cellText=cell_text,
                            rowLabels=rows,
                            rowColours=colors,
                            colLabels=columns,
                            loc='center',
                            colWidths=[0.11,0.11,0.20])
                cell = the_table[2,-1]
                cell.get_text().set_color('white')
                cell = the_table[3,-1]
                cell.get_text().set_color('white')
                cell = the_table[4,-1]
                cell.get_text().set_color('white')

                for i in [1,2,3,4]:
                    cell = the_table[i,-1]
                    cell.set_height(0.17)

                cellDict = the_table.get_celld()
                for i in range(0,len(columns)):
                    cellDict[(0,i)].set_height(.3)
                    for j in range(0,len(cell_text)+1):
                        cellDict[(j,i)].set_height(.17)



                ########## the little timeline plots
                ax3.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
                ax4.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
                ax3.set_xlim([0,max_days])
                ax4.set_xlim([0,max_days])

                legend0 = []
                marker = "s"
                # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]
                legend0.append(ax3.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
                legend0.append(ax3.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))

                ax3.set_facecolor(BA1_colour)
                ax3.axvspan(immune_escape_time,max_days,facecolor=BA45_colour ,zorder=0)
                ax3.axvspan(0,first_exposure_time,facecolor="#cfcfcf",zorder=0)
                ax3.set_yticklabels([])


                days_per_year = 52*7 
                days_per_six_months = 26*7
                six_months_on_day = [i*days_per_six_months for i in range(7) ]
                x_tick_labels = ["0", "0.5", "1","1.5","2","2.5","3"]
                ax3.set_xticks(six_months_on_day)
                ax3.set_xticklabels(x_tick_labels)
                ax3.set_xlabel('time (years)')
                ax3.legend(legend0, ["circulating BA.1","circulating BA.4/5"],bbox_to_anchor=(1.01,-0.2), loc="lower left",borderaxespad=0,frameon=False)

                legend1 = []
                legend1.append(ax4.scatter(-10000,-10000,color=vaccinating_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
                legend1.append(ax4.scatter(-10000,-10000,color=boosting_colour_general, s=100, marker= marker, alpha=1.0, edgecolors='none'))
                ax4.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)
                ax4.axvspan(boosting_time,boosting_time+13*7,facecolor= boosting_colour_general,zorder=0)
                ax4.set_yticklabels([])

                ax4.set_xticks(six_months_on_day)
                ax4.set_xticklabels(x_tick_labels)
                ax4.set_xlabel('time (years)')
                ax4.legend(legend1, ["main vaccinaton program","further boosting program"],bbox_to_anchor=(1.01,-0.2), loc="lower left",borderaxespad=0,frameon=False)



                
                plt.subplots_adjust(hspace=0.9)
                plt.subplots_adjust(hspace=2)
                
                plt.savefig(os.path.join(folder, "total_" + ICU_or_death+"_histogram_"+population_type+"_vax_" + str(vaccination_coverage)+"_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) +"_time"+str(timeframe[0])+"-" + str(timeframe[-1])+"_minimum-age-"+str(minimum_age)+  ".png") , bbox_inches='tight')
                plt.close()



def plot_before_vs_after_infections_ALL(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],aspect_ratio = 'equal',infections_or_deaths_plotting = "infections"):

    original_program_time = 26*7*3
    immune_escape_time = original_program_time + 26*7
    boosting_time = immune_escape_time

    cut_time = immune_escape_time
    days_before = list(range(0,cut_time))
    days_after = list(range(cut_time,max_days))

    folder = "/scratch/cm37/tpl/annual_boosting_1_younger_immune_escape_t" + str(immune_escape_time) +"_outputs/"
    presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1_younger/'

    for population_type in population_type_list:
        fig, ax = plt.subplots(1,1, figsize=(10,10))

        # first, some plotting to get some fake legends...
        legend_points = []
        marker='o'
    
        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
            legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            

        for local_TP_list in TP_segregated_list:

            for vaccination_coverage in [0.2,0.5]:
                
                for paramNum in param_list:
                    presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                    presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                    with open(presimfilename, "r") as f:
                        presim_parameters = json.load(f)

                    total_population = presim_parameters["total_population"]
                    # population_type = presim_parameters["population_type"]
                    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                    booster_fraction = presim_parameters["booster_fraction"]
                    boosting_group = presim_parameters['boosting_group']
                    sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                    if boosting_time == sims_boosting_time or boosting_group=='none':
                        pass
                    else:
                        continue

                    if vaccination_coverage!= total_vaccination_rate:
                        continue
                    else:
                        pass 
                    
                    for TP in local_TP_list:

                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                    
                    
                        datafilename = filename + ".csv"
                        data_file = os.path.join(folder, datafilename)
                        pd_obj = pd.read_csv(data_file)

                        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                        df = new_pd.pivot(index='day', columns='sim', values='n')
                        df_dict = df.to_dict()
                        infections_per_sim_before = []
                        infections_per_sim_after = []

                        if infections_or_deaths_plotting=="deaths":
                            clinical_filename = "_full_outcomes_dataframe.csv"
                            clinical_file = os.path.join(folder,filename,clinical_filename)

                            if os.path.isfile(clinical_file):
                                pass
                            else:
                                print(clinical_file +" DOES NOT EXIST!")
                                continue


                            clinical_pd_obj = pd.read_csv(clinical_file)

                            deaths_per_sim_after = [] 

                        scale = 40
                        aug_num = 5
                        for simnum in df_dict.keys():
                            if infections_or_deaths_plotting=="infections":
                                infections_over_time = df_dict[simnum]
                                total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                                infections_per_sim_before.append(total_infections_before)

                                total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                                infections_per_sim_after.append(total_infections_after)
                            elif infections_or_deaths_plotting=="deaths":
                                infections_over_time = df_dict[simnum]
                                total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))

                                for aug in range(1,aug_num+1):
                                    infections_per_sim_before.append(total_infections_before)

                                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_after))]
                                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                    deaths_per_sim_after.append(daily_deaths) 



                        outline = 'None'
                        percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                        if infections_or_deaths_plotting=="infections":
                            percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                        if boosting_group == '5-15':
                            plot_colour = pedatric_boosting_colour
                        elif boosting_group == '65+':
                            plot_colour = old_boosting_colour
                        elif boosting_group == 'primary' or boosting_group=='random':
                            plot_colour = random_boosting_colour
                        elif boosting_group=='none':
                            plot_colour = no_boosting_colour
                            outline = pedatric_boosting_colour

                        if infections_or_deaths_plotting=="infections":
                            ax.scatter( percent_infected_before, percent_infected_after,color=plot_colour, s=scale,  marker= marker, alpha=0.8, edgecolors=outline)
                        elif infections_or_deaths_plotting=="deaths":
                                ax.scatter( percent_infected_before,deaths_per_sim_after,color=plot_colour, s=scale,  marker= marker, alpha=0.8, edgecolors=outline)

        if infections_or_deaths_plotting=="infections":       
            ax.plot([0, 300], [0, 300],linestyle='--',color="black")
        
        ax.set_xlim(x_limits)
        ax.set_ylim(y_limits)

        if infections_or_deaths_plotting=="infections":
            y_ticks = list(range(0,max(y_limits)+1,20))
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(y)+"\%" for y in y_ticks])
        elif infections_or_deaths_plotting=="deaths":
            y_ticks = list(range(0,max(y_limits)+1,5))
            ax.set_yticks(y_ticks)

        x_ticks = list(range(0,max(x_limits)+1,20))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        ax.set_aspect(aspect_ratio)
        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        leg = Legend(ax, legend_points, ["no further boosting","new pediatric vaccination (ages 5-15)","high risk boosting (65+ first)", "new primary vaccinations"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        leg._legend_box.align = "left"
        ax.add_artist(leg)

        if infections_or_deaths_plotting=="infections":
            ax.set_ylabel('attack rate after boosting starts')
        elif infections_or_deaths_plotting=="deaths":
            ax.set_ylabel('deaths after boosting starts')
        ax.set_xlabel('attack rate before boosting starts')
        

        # xticks = [15,20,30,40,50,60,70,80,85]
        xticks = x_ticks
        for x0, x1 in zip(xticks[::2], xticks[1::2]):
            plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

        # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)
        if infections_or_deaths_plotting=="infections":
            plt.savefig(os.path.join(folder, "past_vs_future_waves_infections_"+ population_type +"_vax_ALL_boosting_"+str(boosting_time)+ "_maxTP_ALL_cut-time-"+str(cut_time) +".png") , bbox_inches='tight')
        elif infections_or_deaths_plotting=="deaths":
            plt.savefig(os.path.join(folder, "past_wave_vs_future_deaths_"+ population_type +"_vax_ALL_boosting_"+str(boosting_time)+ "_maxTP_ALL_cut-time-"+str(cut_time) +".png") , bbox_inches='tight')
        plt.close()


################################################################################################
# PLOTTING
################################################################################################
original_program_time = 26*7*3

immune_escape_times = [original_program_time + 26*7 ] 

for immune_escape_time in immune_escape_times:

    folder = "/scratch/cm37/tpl/annual_boosting_1_younger_immune_escape_t" + str(immune_escape_time) +"_outputs/"
    presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1_younger/'

    plot_ribbon_infections_over_time_plus(younger_or_older=["younger"],immune_escape_time=immune_escape_time)

    for boosting_time in boosters_only_vaccination_start_list:

        total_deaths_histograms_with_mean(boosting_time,immune_escape_time,ICU_or_death='death',younger_or_older=["younger"],timeframe=list(range(original_program_time,max_days)),minimum_age = 0)


        # plot_before_vs_after_infections(boosting_time,population_type_list = ["younger"],x_limits=[0,200],y_limits = [0,200],aspect_ratio = 'equal',cut_time=original_program_time)

        # plot_before_vs_after_infections(boosting_time,population_type_list = ["younger"],x_limits=[0,200],y_limits = [0,200],aspect_ratio = 'equal',cut_time=boosting_time)

        # total_infections_and_deaths_histograms(boosting_time,ICU_or_death='death',younger_or_older=["younger"],timeframe=local_days)
        # total_infections_and_deaths_histograms(boosting_time,ICU_or_death='death',younger_or_older=["younger"],timeframe=list(range(boosting_time,max_days)))

        # total_infections_and_deaths_histograms(boosting_time,ICU_or_death='death',younger_or_older=["younger"],timeframe=list(range(original_program_time,max_days)))

        # total_infections_and_deaths_histograms(boosting_time,ICU_or_death='death',younger_or_older=["younger"],timeframe=local_days,minimum_age=65)
        # total_infections_and_deaths_histograms(boosting_time,ICU_or_death='death',younger_or_older=["younger"],timeframe=list(range(boosting_time,max_days)),minimum_age=65)

# plot_before_vs_after_infections_ALL(population_type_list = ["younger"],x_limits=[0,180],y_limits = [0,200],aspect_ratio = 'equal',infections_or_deaths_plotting = "infections")

# plot_before_vs_after_infections_ALL(population_type_list = ["younger"],x_limits=[0,180],y_limits = [0,40],aspect_ratio = 'equal',infections_or_deaths_plotting = "deaths")