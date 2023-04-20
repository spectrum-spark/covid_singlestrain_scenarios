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

TP_list = ["1.05", "1.95"]
TP_low = ["1.05"]
TP_high = ["1.95"]
TP_segregated_list = [TP_low,TP_high]

param_list = list(range(0,12+1))
# novax_index = 0
# SIM_NUMBER = 100

max_days = 52*3*7 # 3 years 
first_exposure_time =225

original_program_time = 26*7*3
boosters_only_vaccination_start_list = [original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7  , original_program_time + 52*7 ]
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

date_values = list(range(0,max_days,10))
date_names = [str(x) for x in date_values]

# days = list(range(0,max_days+1))
local_days = list(range(max_days))



def plot_ribbon_infections_over_time_plus(younger_or_older=["older"],immune_escape_time=546):
    max_infections=5000 

    BA1_colour = '#a1a1a1'
    BA45_colour = "#666666"
    vaccinating_colour = "yellowgreen"
    boosting_colour_general = "darkgreen"

    # pedatric_boosting_colour = 'purple'
    # old_boosting_colour = 'firebrick'
    # random_boosting_colour = 'chocolate'

    # pedatric_boosting_colour = 'dodgerblue'
    # old_boosting_colour = 'firebrick'
    # random_boosting_colour = 'mediumorchid'

    for boosting_time in boosters_only_vaccination_start_list:

        for local_TP_list in TP_segregated_list:

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

                # if population_type=="younger":
                #     print("colours not determined yet")
                #     exit(1)
                #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                #     legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                # if population_type=="older":
                    
                legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
                legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                    # legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
                    # legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    # legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                    # legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

                all_curves_over_local_days = {'none':[], '5-15':[], '65+':[],'random' :[]}

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

                    if boosting_group=='none' or  boosting_time == sims_boosting_time:
                        pass
                    else:
                        continue  

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
                upper_ribbon = {'none':[], '5-15':[], '65+':[],'random' :[]} # for vaccinated groups
                lower_ribbon = {'none':[],'5-15':[], '65+':[],'random' :[]}
                median_line = {'none':[],'5-15':[], '65+':[],'random' :[]}

                for boosting_group in ['none', '5-15','65+','random']:
                    upper_ribbon[boosting_group] = [max([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
                    lower_ribbon[boosting_group] = [min([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
                    median_line[boosting_group] = [np.median([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
                for boosting_group in ['none', '5-15','65+','random']:
                    # if population_type == "younger":
                    #     pass
                    # else:
                    if boosting_group == '5-15':
                        plot_colour = pedatric_boosting_colour
                    elif boosting_group == '65+':
                        plot_colour = old_boosting_colour
                    elif boosting_group == 'random':
                        plot_colour = random_boosting_colour
                    elif boosting_group =='none':
                        plot_colour = no_boosting_colour
                    
                    ax.fill_between(local_days,upper_ribbon[boosting_group],lower_ribbon[boosting_group],facecolor=plot_colour,alpha=0.5)
                    # ax.plot(local_days,median_line[vax],color = plot_colour,linestyle='solid')
                for boosting_group in ['none', '5-15','65+','random']:
                    # if population_type == "younger":
                    #     pass
                    # else:
                    if boosting_group == '5-15':
                        plot_colour = pedatric_boosting_colour
                    elif boosting_group == '65+':
                        plot_colour = old_boosting_colour
                    elif boosting_group == 'random':
                        plot_colour = random_boosting_colour
                    elif boosting_group =='none':
                        plot_colour = no_boosting_colour
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

            ax2.legend(legend0, ["circulating BA.1","circulating BA.4/5", "main vaccinaton program","further boosting program"],bbox_to_anchor=(1.01,-0.1), loc="lower left",borderaxespad=0,frameon=False)

            if population_type=="older":
                leg = Legend(ax, legend_points, ["no further boosting", "pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"],title=younger_or_older[0] +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            else:
                leg = Legend(ax, legend_points, ["no further boosting", "pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"],title=younger_or_older[0] +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            leg._legend_box.align = "left"
            ax.add_artist(leg)
            
            ax.set_ylabel('number of infections')
            
            plt.savefig(os.path.join(folder, "ribbon_infections_over_time_plus_"+younger_or_older[0]+ "_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) + ".png") , bbox_inches='tight')
            plt.close()


def plot_before_vs_after_infections(boosting_time,population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],aspect_ratio = 'equal',cut_time = original_program_time):
    # third_stage_vaccination = "none", "early","reactive"

    days_before = list(range(0,cut_time))
    days_after = list(range(cut_time,max_days))

    

    for local_TP_list in TP_segregated_list:

        for population_type in population_type_list:

            if y_limits[1]>80:
                fig, ax = plt.subplots(1,1, figsize=(8,7.75)) # for the second strain
            else:
                fig, ax = plt.subplots(1,1, figsize=(6,6.75))
            
            # first, some plotting to get some fake legends...
            legend_points = []
            marker='o'

        
            # if population_type=="younger":
            #     print("colours not determined yet")
            #     exit(1)
            #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
            #     legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            #     legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            #     legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            # if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
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

                if boosting_time == sims_boosting_time or boosting_group=='none':
                    pass
                else:
                    continue
                
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
                    elif boosting_group == 'random':
                        plot_colour = random_boosting_colour
                    elif boosting_group=='none':
                        plot_colour= no_boosting_colour
                        outline = pedatric_boosting_colour

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

            if population_type=="older":
                leg = Legend(ax, legend_points, ["no further boosting", "pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            else:
                leg = Legend(ax, legend_points, ["no further boosting", "pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            leg._legend_box.align = "left"
            ax.add_artist(leg)

            ax.set_ylabel('future attack rate (t = ' + str(days_after[0])+' to ' + str(days_after[-1])+')')
            ax.set_xlabel('past attack rate (before t = '+str(days_before[-1]+1) +')')
            

            # xticks = [15,20,30,40,50,60,70,80,85]
            xticks = x_ticks
            for x0, x1 in zip(xticks[::2], xticks[1::2]):
                plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

            # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

            plt.savefig(os.path.join(folder, "past_vs_future_waves_infections_"+ population_type +"_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) +"_cut-time-"+str(cut_time) +".png") , bbox_inches='tight')
            plt.close()


def total_infections_and_deaths_histograms(boosting_time,ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):

    for local_TP_list in TP_segregated_list:
        fig, (ax, ax2) = plt.subplots(2, figsize=(8,4))

        legend_points = []
        marker = "o" # "s"
        for population_type in younger_or_older:

            # if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
            legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

            total_infections_local_days =  {'none':[], '5-15':[], '65+':[],'random' :[]}
            total_severe_disease_local_days = {'none':[],'5-15':[], '65+':[],'random' :[]}

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

                if boosting_time==sims_boosting_time or boosting_group =='none':
                    pass
                else:
                    continue

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
            for boosting_group in ['none','5-15','65+','random']:
                # if population_type == "younger":
                #     pass
                # else:
                if boosting_group == '5-15':
                    plot_colour = pedatric_boosting_colour
                elif boosting_group == '65+':
                    plot_colour = old_boosting_colour
                elif boosting_group == 'random':
                    plot_colour = random_boosting_colour
                elif boosting_group =='none':
                    plot_colour = no_boosting_colour
                
                ax.hist(total_infections_local_days[boosting_group], bins=10, alpha=0.5, color=plot_colour)

                ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, alpha=0.5, color=plot_colour)


        ax.set_ylabel('Count')
        ax.set_xlim(0,360000)
        ax.set_ylim(0,20)
        # ax.set_xlim([min(local_days),max_days])
        ax.grid(color='#878787', linestyle=(0, (5, 1)))
        ax.set_facecolor('silver')
        ax.set_axisbelow(True)

        # ax2.set_title("For ages >= " + str(minimum_age))

        ax.set_xlabel("Total infections (t = " + str(timeframe[0])+" to " + str(timeframe[-1])+")")
        # ax.set_xlim(0,200000)

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

        if population_type=="older":
            leg = Legend(ax, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        else:
            leg = Legend(ax, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        leg._legend_box.align = "left"
        ax.add_artist(leg)
        
        plt.subplots_adjust(hspace=0.5)
        
        plt.savefig(os.path.join(folder, "total_infections_and_" + ICU_or_death+"_histogram_"+"_".join(younger_or_older)+ "_"+"_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) +"_time"+str(timeframe[0])+"-" + str(timeframe[-1])+"_minimum-age-"+str(minimum_age)+ ".png") , bbox_inches='tight')
        plt.close()



def total_deaths_histograms(boosting_time,immune_escape_time,ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):
    BA1_colour = '#a1a1a1'
    BA45_colour = "#666666"
    vaccinating_colour = "yellowgreen"
    boosting_colour_general = "darkgreen"

    for local_TP_list in TP_segregated_list:
        fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [6, 1,1],'width_ratios':[1,1]}, figsize=(13,4))
        # fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [6, 1,1],'width_ratios':[3,2]}, figsize=(10,4))
        ax_table.axis("off")
        ax5.axis("off")
        ax6.axis("off")

        legend_points = []
        marker = "o" # "s"
        total_severe_disease_statistics = {'none':[],'5-15':[], '65+':[],'random' :[]}
        for population_type in younger_or_older:

            # if population_type=="older":
            legend_points.append(ax2.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
            legend_points.append(ax2.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax2.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax2.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

            # total_infections_local_days =  {'none':[], '5-15':[], '65+':[],'random' :[]}
            total_severe_disease_local_days = {'none':[],'5-15':[], '65+':[],'random' :[]}
           

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

                if boosting_time==sims_boosting_time or boosting_group =='none':
                    pass
                else:
                    continue

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
                        # infections_over_time = df_dict[simnum]
                        # total_infections = sum(list_conversion_nans(infections_over_time, timeframe ))
                        # total_infections_local_days[boosting_group].append(total_infections ) 

                        for aug in range(1,aug_num+1):
                            new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]
                            
                            if ICU_or_death == 'death':
                                daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                total_severe_disease_local_days[boosting_group].append(daily_deaths) 
                            elif ICU_or_death =='ICU':
                                daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                total_severe_disease_local_days[boosting_group].append(daily_ICU_admissions) 
            
            
            outline = 'none'
            for boosting_group in ['none','5-15','65+','random']:
                # if population_type == "younger":
                #     pass
                # else:
                if boosting_group == '5-15':
                    plot_colour = pedatric_boosting_colour
                    outline =  pedatric_boosting_colour
                elif boosting_group == '65+':
                    plot_colour = old_boosting_colour
                    outline = old_boosting_colour
                elif boosting_group == 'random':
                    plot_colour = random_boosting_colour
                    outline =  random_boosting_colour
                elif boosting_group =='none':
                    plot_colour = no_boosting_colour
                    outline =no_boosting_colour
                
                # ax.hist(total_infections_local_days[boosting_group], bins=10, alpha=0.5, color=plot_colour)
                median = np.median(total_severe_disease_local_days[boosting_group])
                lower_quantile = np.quantile(total_severe_disease_local_days[boosting_group],0.025)
                upper_quantile = np.quantile(total_severe_disease_local_days[boosting_group],0.975)
                total_severe_disease_statistics[boosting_group] = [median,lower_quantile,upper_quantile]

                ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, alpha=0.5, color=plot_colour,histtype='bar')
                ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, facecolor="none", edgecolor=outline, histtype='step')
        

        ax2.set_ylabel('Count')
        ax2.set_xlim(0,110)
        ax2.set_ylim(bottom=0,top=200)
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


        # total_severe_disease_statistics[boosting_group] = [median,lower_quantile,upper_quantile]

        # if population_type=="older":
        #     leg = Legend(ax2, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        # else:
        #     leg = Legend(ax2, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        # leg._legend_box.align = "left"
        # ax2.add_artist(leg)
        
        print(total_severe_disease_statistics)
        # n_rows = 4
        columns = ("Median","95\% quantiles")
        if  population_type=="older":
            rows =  ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"]
        else:
            rows =  ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"]
        colors = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
        cell_text = [[round(values[0],2),(round(values[1],2),round(values[2],2))] for boosting_group,values in total_severe_disease_statistics.items()]

        ####### table of statistics instead of legend 
        the_table = ax_table.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                       loc='center',
                      colWidths=[0.12,0.24])
        cell = the_table[2,-1]
        cell.get_text().set_color('white')
        cell = the_table[3,-1]
        cell.get_text().set_color('white')
        cell = the_table[4,-1]
        cell.get_text().set_color('white')

        for i in [1,2,3,4]:
            cell = the_table[i,-1]
            cell.set_height(0.18)

        cellDict = the_table.get_celld()
        for i in range(0,len(columns)):
            cellDict[(0,i)].set_height(.3)
            for j in range(0,len(cell_text)+1):
                cellDict[(j,i)].set_height(.18)


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
        
        plt.savefig(os.path.join(folder, "total_" + ICU_or_death+"_histogram_"+"_".join(younger_or_older)+ "_"+"_boosting_"+str(boosting_time)+ "_maxTP_"+str(max(local_TP_list)) +"_time"+str(round(timeframe[0]/(52*7),2))+"-" + str(round(timeframe[-1]/(52*7),2))+"years_minimum-age-"+str(minimum_age)+ ".png") , bbox_inches='tight')
        plt.close()




def plot_ribbon_infections_over_time_plus_fixed_boosting_group(boosting_group_here = "65+",younger_or_older=["older"],immune_escape_time=546):
    max_infections=5000 

    BA1_colour = '#a1a1a1'
    BA45_colour = "#666666"
    vaccinating_colour = "yellowgreen"

    # boosters_only_vaccination_start_list = [original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7  , original_program_time + 52*7 ]

    boosters_start_colour_list = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
    boosters_start_edgecolour_list = [pedatric_boosting_colour,'none','none','none']


    for local_TP_list in [TP_high]:
        for population_type in younger_or_older:
            # fig, ax = plt.subplots(1,1, figsize=(8,3.5)) #10,4  # 16:9
            fig, (ax, ax2,ax3) = plt.subplots(3, sharex=True, gridspec_kw={'height_ratios': [6, 1,1]},figsize = (8,5.2))

            legend0 = []
            marker = "s"
            # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]
            legend0.append(ax.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend0.append(ax.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend0.append(ax.scatter(-10000,-10000,color=vaccinating_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))

            legend_points = []
            marker='o'
            # if population_type=="younger":
            #     print("colours not determined yet")
            #     exit(1)
            # if population_type=="older":
            for plot_colour,edge_colour in zip(boosters_start_colour_list,boosters_start_edgecolour_list):
                legend_points.append(ax.scatter(-10000,-10000,color=plot_colour, s=100, marker= 'o', alpha=1.0, edgecolors=edge_colour))

            all_curves_over_local_days = {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            
            for paramNum in param_list:

                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)

                # total_population = presim_parameters["total_population"]
                # population_type = presim_parameters["population_type"]
                # total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                # booster_fraction = presim_parameters["booster_fraction"]
                boosting_group = presim_parameters['boosting_group']
                sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                if boosting_group != boosting_group_here:
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
                        all_curves_over_local_days[sims_boosting_time].append(infections_over_time_list)

                        # ax.plot(local_days,infections_over_time_list,alpha=1,color=plot_colour)
                        plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(sims_boosting_time)]
                        ax.plot(local_days,infections_over_time_list,color = plot_colour,linestyle='solid',alpha=0.5)
            
            upper_ribbon = {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            lower_ribbon =  {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            median_line = {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}

            for boosting_time in boosters_only_vaccination_start_list:
                upper_ribbon[boosting_time] = [max([all_curves_over_local_days[boosting_time][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_time]))]) for i in range(len(local_days))]
                lower_ribbon[boosting_time] = [min([all_curves_over_local_days[boosting_time][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_time]))]) for i in range(len(local_days))]
                median_line[boosting_time] = [np.median([all_curves_over_local_days[boosting_time][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_time]))]) for i in range(len(local_days))]
            for boosting_time in boosters_only_vaccination_start_list:
                # if population_type == "younger":
                #     pass
                # else:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]

                    # boosters_only_vaccination_start_list = [original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7  , original_program_time + 52*7 ]
                    # boosters_start_colour_list = ['white','salmon','red','firebrick']
                    # boosters_start_edgecolour_list = ['salmon','none','none','none']

                ax.fill_between(local_days,upper_ribbon[boosting_time],lower_ribbon[boosting_time],facecolor=plot_colour,alpha=0.5)
                # ax.plot(local_days,median_line[vax],color = plot_colour,linestyle='solid')
            

            #####################
            #  many boosters

            legend_points.append(ax.scatter(-10000,-10000,color=many_boosters_colour, s=100, marker= 'o', alpha=1.0, edgecolors=many_boosters_colour))
            all_curves_over_local_days = []

            for TP in local_TP_list:
                filename_many_boosters = "abm_continuous_simulation_parameters_"+population_type+"_SOCRATES_TP"+TP
                print(filename_many_boosters)
                datafilename = filename_many_boosters + ".csv"
                data_file = os.path.join(folder_many_boosters, datafilename)

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
                    all_curves_over_local_days.append(infections_over_time_list)

                    # ax.plot(local_days,infections_over_time_list,alpha=1,color=plot_colour)
                    plot_colour = many_boosters_colour
                    ax.plot(local_days,infections_over_time_list,color = plot_colour,linestyle='solid',alpha=0.1)
            
            upper_ribbon_many_boosters = [max([all_curves_over_local_days[simnum][i] for simnum in range(len(all_curves_over_local_days))]) for i in range(len(local_days))]
            lower_ribbon_many_boosters =   [min([all_curves_over_local_days[simnum][i] for simnum in range(len(all_curves_over_local_days))]) for i in range(len(local_days))]
            median_line_many_boosters =  [np.median([all_curves_over_local_days[simnum][i] for simnum in range(len(all_curves_over_local_days))]) for i in range(len(local_days))]


            ax.fill_between(local_days,upper_ribbon_many_boosters,lower_ribbon_many_boosters,facecolor=many_boosters_colour,alpha=0.1)
        
            ################################################

            for boosting_time in boosters_only_vaccination_start_list:
                # if population_type == "younger":
                #     pass
                # else:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]

                # ax.fill_between(local_days,upper_ribbon[vax],lower_ribbon[vax],facecolor=plot_colour,alpha=0.5)
                ax.plot(local_days,median_line[boosting_time],color = plot_colour,linestyle='solid')

            plot_colour = many_boosters_colour
            edge_colour = many_boosters_colour

            ax.plot(local_days,median_line_many_boosters,color = plot_colour,linestyle='solid')

            ######################
            
            days_per_six_months = 26*7
            six_months_on_day = [i*days_per_six_months for i in range(7) ]
            x_tick_labels = ["0", "0.5", "1","1.5","2","2.5","3"]
            ax.set_xticks(six_months_on_day)
            ax.set_xticklabels(x_tick_labels)
            ax3.set_xlabel('time (years)')

            ax.set_ylim([0,max_infections])
            ax.set_xlim([min(local_days),max_days])
            # ax.set_xlabel('time (days)')
            ax.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8)
            ax2.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
            ax3.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
            
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
            for boosting_time in boosters_only_vaccination_start_list:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                ax2.axvspan(boosting_time,boosting_time+13*7,facecolor= plot_colour ,zorder=0,hatch="/",edgecolor = edge_colour)

            ax2.set_yticklabels([])

            # legend0.append(ax.scatter(-10000,-10000,color=many_boosters_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))


            ax2.legend(legend0, ["circulating BA.1","circulating BA.4/5", "main vaccination program"],bbox_to_anchor=(1.01,0.0), loc="lower left",borderaxespad=0,frameon=False)

            ax3.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)
            for boosting_time in [637,637+7*26,637+7*52]:
                plot_colour = many_boosters_colour
                edge_colour = many_boosters_colour
                ax3.axvspan(boosting_time,boosting_time+13*7,facecolor= plot_colour ,zorder=0,hatch="/",edgecolor = edge_colour)

            ax3.set_yticklabels([])

            
            legend_names = [str(round(x/(52*7),2)) + " years"  for x in boosters_only_vaccination_start_list]
            legend_names.append("Half-yearly boosters")

            if population_type=="older":
                leg = Legend(ax, legend_points,legend_names,title=younger_or_older[0] +" population\nhigh risk boosting (65+)\nfurther boosting commences at:",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
                
            else:
                leg = Legend(ax, legend_points,legend_names,title=younger_or_older[0] +" population\nhigh risk boosting (55+)\nfurther boosting commences at:",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            leg._legend_box.align = "left"
            ax.add_artist(leg)
            
            ax.set_ylabel('number of infections')
            
            plt.savefig(os.path.join(folder_many_boosters, "ribbon_infections_over_time_plus_fixed_boosting_group"+younger_or_older[0]+ "_boosting_"+str(boosting_group_here)+ "_maxTP_"+str(max(local_TP_list)) + ".png") , bbox_inches='tight')
            plt.close()





def total_infections_and_deaths_histograms_fixed_boosting_group(boosting_group_here = "65+",ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):
    boosters_start_colour_list = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
    boosters_start_edgecolour_list = [pedatric_boosting_colour,'none','none','none']


    for local_TP_list in TP_segregated_list:
        for population_type in younger_or_older:
            fig, (ax, ax2) = plt.subplots(2, figsize=(8,4))

            legend_points = []
            marker = "o" # "s"
        
            # if population_type=="younger":
            #     print("colours not determined yet")
            #     exit(1)
            # if population_type=="older":
            for plot_colour,edge_colour in zip(boosters_start_colour_list,boosters_start_edgecolour_list):
                legend_points.append(ax.scatter(-10000,-10000,color=plot_colour, s=100, marker= 'o', alpha=1.0, edgecolors=edge_colour))

            total_infections_local_days =  {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            total_severe_disease_local_days =  {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}

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

                if boosting_group != boosting_group_here:
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
                        total_infections_local_days[sims_boosting_time].append(total_infections ) 

                        for aug in range(1,aug_num+1):
                            new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]
                            
                            if ICU_or_death == 'death':
                                daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                total_severe_disease_local_days[sims_boosting_time].append(daily_deaths) 
                            elif ICU_or_death =='ICU':
                                daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                total_severe_disease_local_days[sims_boosting_time].append(daily_ICU_admissions) 
            
            
            outline = 'none'
            for boosting_time in boosters_only_vaccination_start_list:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                
                ax.hist(total_infections_local_days[boosting_time], bins=10, alpha=0.5, color=plot_colour,edgecolor = edge_colour)

                ax2.hist(total_severe_disease_local_days[boosting_time],bins=10, alpha=0.5, color=plot_colour,edgecolor=edge_colour)


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


            leg = Legend(ax, legend_points,["year " + str(round(x/(52*7),2)) for x in boosters_only_vaccination_start_list],title=younger_or_older[0] +" population, high risk boosting;\nboosting commences:",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            leg._legend_box.align = "left"
            ax.add_artist(leg)

            

            
            plt.subplots_adjust(hspace=0.5)
            
            plt.savefig(os.path.join(folder, "total_infections_and_" + ICU_or_death+"_histogram_"+population_type+ "_fixed_boosting_group"+"_boosting_"+str(boosting_group_here)+ "_maxTP_"+str(max(local_TP_list)) +"_time"+str(timeframe[0])+"-" + str(timeframe[-1])+"_minimum-age-"+str(minimum_age)+ ".png") , bbox_inches='tight')
            plt.close()





def total_deaths_histograms_fixed_boosting_group(immune_escape_time,boosting_group_here = "65+",ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):
    boosters_start_colour_list = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
    # boosters_start_edgecolour_list = [pedatric_boosting_colour,'none','none','none']
    boosters_start_edgecolour_list =boosters_start_colour_list 

    BA1_colour = '#a1a1a1'
    BA45_colour = "#666666"
    vaccinating_colour = "yellowgreen"
    boosting_colour_general = "darkgreen"


    for local_TP_list in  [TP_high]:
        for population_type in younger_or_older:
            # fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [6, 1,1],'width_ratios':[2,1]}, figsize=(11,4))

            fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [6, 1,1],'width_ratios':[1,1]}, figsize=(13,4))
            ax_table.axis("off")
            ax5.axis("off")
            ax6.axis("off")

            legend_points = []
            marker = "o" # "s"

            # if population_type=="younger":
            #     print("colours not determined yet")
            #     exit(1)
            # if population_type=="older":
            for plot_colour,edge_colour in zip(boosters_start_colour_list,boosters_start_edgecolour_list):
                legend_points.append(ax2.scatter(-10000,-10000,color=plot_colour, s=100, marker= 'o', alpha=1.0, edgecolors=edge_colour))
            # total_infections_local_days =  {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            total_severe_disease_local_days =  {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            total_severe_disease_local_days['many boosters'] = []

            total_severe_disease_statistics = {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            total_severe_disease_statistics['many boosters'] = []


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

                if boosting_group != boosting_group_here:
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
                        # infections_over_time = df_dict[simnum]
                        # total_infections = sum(list_conversion_nans(infections_over_time, timeframe ))
                        # total_infections_local_days[sims_boosting_time].append(total_infections ) 

                        for aug in range(1,aug_num+1):
                            new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]
                            
                            if ICU_or_death == 'death':
                                daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                total_severe_disease_local_days[sims_boosting_time].append(daily_deaths) 
                            elif ICU_or_death =='ICU':
                                daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                                total_severe_disease_local_days[sims_boosting_time].append(daily_ICU_admissions) 
            ###########

            # many boosters

            for TP in local_TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_SOCRATES_TP"+TP
                print(filename)

                datafilename = filename + ".csv"

                data_file = os.path.join(folder_many_boosters, datafilename)

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
                clinical_file = os.path.join(folder_many_boosters,filename,clinical_filename)

                if os.path.isfile(clinical_file):
                    pass
                else:
                    print(clinical_file +" DOES NOT EXIST!")
                    continue


                clinical_pd_obj = pd.read_csv(clinical_file)

                scale = 40
                aug_num = 5
                for simnum in df_dict.keys():

                    for aug in range(1,aug_num+1):
                        new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]
                        
                        if ICU_or_death == 'death':
                            daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                            total_severe_disease_local_days["many boosters"].append(daily_deaths) 
                        elif ICU_or_death =='ICU':
                            daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                            total_severe_disease_local_days["many boosters"].append(daily_ICU_admissions) 



            ########
            outline = 'none'
            for boosting_time in boosters_only_vaccination_start_list:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]

                median = np.median(total_severe_disease_local_days[boosting_time])
                lower_quantile = np.quantile(total_severe_disease_local_days[boosting_time],0.025)
                upper_quantile = np.quantile(total_severe_disease_local_days[boosting_time],0.975)
                total_severe_disease_statistics[boosting_time] = [median,lower_quantile,upper_quantile]

                ax2.hist(total_severe_disease_local_days[boosting_time],bins=10, alpha=0.5, color=plot_colour,histtype='bar')
                ax2.hist(total_severe_disease_local_days[boosting_time],bins=10, facecolor="none", edgecolor=edge_colour, histtype='step')

            median = np.median(total_severe_disease_local_days["many boosters"])
            lower_quantile = np.quantile(total_severe_disease_local_days["many boosters"],0.025)
            upper_quantile = np.quantile(total_severe_disease_local_days["many boosters"],0.975)
            total_severe_disease_statistics["many boosters"] = [median,lower_quantile,upper_quantile]

            ax2.hist(total_severe_disease_local_days["many boosters"],bins=10, alpha=0.5, color=many_boosters_colour,histtype='bar')
            ax2.hist(total_severe_disease_local_days["many boosters"],bins=10, facecolor="none", edgecolor=many_boosters_colour, histtype='step')

        
            ax2.set_ylabel('Count')
            ax2.set_xlim(0,110)
            ax2.set_ylim(bottom=0,top=200)
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


            # leg = Legend(ax, legend_points,["year " + str(round(x/(52*7),2)) for x in boosters_only_vaccination_start_list],title=younger_or_older[0] +" population, high risk boosting;\nboosting commences:",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            # leg._legend_box.align = "left"
            # ax.add_artist(leg)

            print(total_severe_disease_statistics)
            # n_rows = 4
            columns = ("Median","95\% quantiles")
            rows =  [ str(round(x/(52*7),2)) +" years" for x in boosters_only_vaccination_start_list]
            rows.append("Half-yearly boosters")
            colors = boosters_start_colour_list
            colors.append(many_boosters_colour)
            cell_text = [[round(values[0],2),(round(values[1],2),round(values[2],2))] for key,values in total_severe_disease_statistics.items()]

            ####### table of statistics instead of legend 
            the_table = ax_table.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns,
                        loc='center',
                        colWidths=[0.12,0.24])
            cell = the_table[2,-1]
            cell.get_text().set_color('white')
            cell = the_table[3,-1]
            cell.get_text().set_color('white')
            cell = the_table[4,-1]
            cell.get_text().set_color('white')
            cell = the_table[5,-1]
            cell.get_text().set_color('white')

            for i in [1,2,3,4,5]:
                cell = the_table[i,-1]
                cell.set_height(0.18)

            cellDict = the_table.get_celld()
            for i in range(0,len(columns)):
                cellDict[(0,i)].set_height(.3)
                for j in range(0,len(cell_text)+1):
                    cellDict[(j,i)].set_height(.18)


            ########## the little timeline plots
            ax3.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
            ax4.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
            ax3.set_xlim([0,max_days])
            ax4.set_xlim([0,max_days])
            ax3.set_yticklabels([])
            ax4.set_yticklabels([])

            legend0 = []
            marker = "s"
            # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]
            legend0.append(ax3.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend0.append(ax3.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))

            ax3.set_facecolor(BA1_colour)
            ax3.axvspan(immune_escape_time,max_days,facecolor=BA45_colour ,zorder=0)
            ax3.axvspan(0,first_exposure_time,facecolor="#cfcfcf",zorder=0)
            


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
            ax4.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)

            for boosting_time in boosters_only_vaccination_start_list:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                ax4.axvspan(boosting_time,boosting_time+13*7,facecolor= plot_colour ,zorder=0,hatch="/",edgecolor = edge_colour)

            ax4.set_xticks(six_months_on_day)
            ax4.set_xticklabels(x_tick_labels)
            ax4.set_xlabel('time (years)')
            ax4.legend(legend1, ["main vaccinaton program"],bbox_to_anchor=(1.01,-0.2), loc="lower left",borderaxespad=0,frameon=False)


            plt.subplots_adjust(hspace=0.9)
            
            plt.savefig(os.path.join(folder_many_boosters, "total_" + ICU_or_death+"_histogram_"+population_type+ "_fixed_boosting_group"+"_boosting_"+str(boosting_group_here)+ "_maxTP_"+str(max(local_TP_list)) +"_time"+str(timeframe[0])+"-" + str(timeframe[-1])+"_minimum-age-"+str(minimum_age)+ ".png") , bbox_inches='tight')
            plt.close()





def total_deaths_histograms_fixed_boosting_group_with_mean(immune_escape_time,boosting_group_here = "65+",ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):
    boosters_start_colour_list = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
    # boosters_start_edgecolour_list = [pedatric_boosting_colour,'none','none','none']
    boosters_start_edgecolour_list =boosters_start_colour_list 

    BA1_colour = '#a1a1a1'
    BA45_colour = "#666666"
    vaccinating_colour = "yellowgreen"
    boosting_colour_general = "darkgreen"


    for local_TP_list in  [TP_high]:
        for population_type in younger_or_older:
            # fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [6, 1,1],'width_ratios':[2,1]}, figsize=(11,4))

            fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [6, 1,1],'width_ratios':[1,1]}, figsize=(13,4))
            ax_table.axis("off")
            ax5.axis("off")
            ax6.axis("off")

            legend_points = []
            marker = "o" # "s"

            # if population_type=="younger":
            #     print("colours not determined yet")
            #     exit(1)
            # if population_type=="older":
            for plot_colour,edge_colour in zip(boosters_start_colour_list,boosters_start_edgecolour_list):
                legend_points.append(ax2.scatter(-10000,-10000,color=plot_colour, s=100, marker= 'o', alpha=1.0, edgecolors=edge_colour))
            # total_infections_local_days =  {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            total_severe_disease_local_days =  {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            total_severe_disease_local_days['many boosters'] = []

            total_severe_disease_statistics = {booster_start_time:[] for booster_start_time in boosters_only_vaccination_start_list}
            total_severe_disease_statistics['many boosters'] = []


            for paramNum in param_list:

                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)

                # total_population = presim_parameters["total_population"]
                # population_type = presim_parameters["population_type"]
                # total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                # booster_fraction = presim_parameters["booster_fraction"]
                boosting_group = presim_parameters['boosting_group']
                sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                if boosting_group != boosting_group_here:
                    continue 
                else:
                    pass 

                for TP in local_TP_list:

                    filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                    print(filename)

                    datafilename = filename + ".csv"

                    # data_file = os.path.join(folder, datafilename)

                    # if os.path.isfile(data_file):
                    #     pass
                    # else:
                    #     print(data_file)
                    #     print("This file ^ doesn't exist????")
                    #     continue

                    # pd_obj = pd.read_csv(data_file)
                    # # print(pd_obj)

                    # new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                    # df = new_pd.pivot(index='day', columns='sim', values='n')

                    # df_dict = df.to_dict()

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
                        total_severe_disease_local_days[sims_boosting_time] = daily_deaths
                        print("=============daily deaths")
                        print(daily_deaths)
                    elif ICU_or_death =='ICU':
                        daily_ICU_admissions =clinical_pd_obj['daily_ICU_admissions'].to_list()
                        total_severe_disease_local_days[sims_boosting_time] = daily_ICU_admissions

                    # scale = 40
                    # aug_num = 5
                    # for simnum in df_dict.keys():
                    #     # infections_over_time = df_dict[simnum]
                    #     # total_infections = sum(list_conversion_nans(infections_over_time, timeframe ))
                    #     # total_infections_local_days[sims_boosting_time].append(total_infections ) 

                    #     for aug in range(1,aug_num+1):
                    #         new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]
                            
                    #         if ICU_or_death == 'death':
                    #             daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                    #             total_severe_disease_local_days[sims_boosting_time].append(daily_deaths) 
                    #         elif ICU_or_death =='ICU':
                    #             daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                    #             total_severe_disease_local_days[sims_boosting_time].append(daily_ICU_admissions) 
            ###########

            # many boosters

            for TP in local_TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_SOCRATES_TP"+TP
                print(filename)

                datafilename = filename + ".csv"

                # data_file = os.path.join(folder_many_boosters, datafilename)

                # if os.path.isfile(data_file):
                #     pass
                # else:
                #     print(data_file)
                #     print("This file ^ doesn't exist????")
                #     continue

                # pd_obj = pd.read_csv(data_file)
                # # print(pd_obj)

                # new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                # df = new_pd.pivot(index='day', columns='sim', values='n')

                # df_dict = df.to_dict()

                clinical_filename = "_full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder_many_boosters,filename,clinical_filename)

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
                    total_severe_disease_local_days["many boosters"] = daily_deaths
                    print("=============daily deaths")
                    print(daily_deaths)
                elif ICU_or_death =='ICU':
                    daily_ICU_admissions =clinical_pd_obj['daily_ICU_admissions'].to_list()
                    total_severe_disease_local_days["many boosters"] = daily_ICU_admissions

                # scale = 40
                # aug_num = 5
                # for simnum in df_dict.keys():

                #     for aug in range(1,aug_num+1):
                #         new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(timeframe )) & (clinical_pd_obj['age']>=minimum_age)]
                        
                #         if ICU_or_death == 'death':
                #             daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                #             total_severe_disease_local_days["many boosters"].append(daily_deaths) 
                #         elif ICU_or_death =='ICU':
                #             daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                #             total_severe_disease_local_days["many boosters"].append(daily_ICU_admissions) 



            ########
            outline = 'none'
            for boosting_time in boosters_only_vaccination_start_list:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]

                median = np.median(total_severe_disease_local_days[boosting_time])
                lower_quantile = np.quantile(total_severe_disease_local_days[boosting_time],0.025)
                upper_quantile = np.quantile(total_severe_disease_local_days[boosting_time],0.975)
                mean = np.mean(total_severe_disease_local_days[boosting_time])
                total_severe_disease_statistics[boosting_time] = [median,lower_quantile,upper_quantile,mean]

                ax2.hist(total_severe_disease_local_days[boosting_time],bins=10, alpha=0.5, color=plot_colour,histtype='bar')
                ax2.hist(total_severe_disease_local_days[boosting_time],bins=10, facecolor="none", edgecolor=edge_colour, histtype='step')

            median = np.median(total_severe_disease_local_days["many boosters"])
            lower_quantile = np.quantile(total_severe_disease_local_days["many boosters"],0.025)
            upper_quantile = np.quantile(total_severe_disease_local_days["many boosters"],0.975)
            mean = np.mean(total_severe_disease_local_days["many boosters"])
            total_severe_disease_statistics["many boosters"] = [median,lower_quantile,upper_quantile,mean]

            ax2.hist(total_severe_disease_local_days["many boosters"],bins=10, alpha=0.5, color=many_boosters_colour,histtype='bar')
            ax2.hist(total_severe_disease_local_days["many boosters"],bins=10, facecolor="none", edgecolor=many_boosters_colour, histtype='step')

        
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


            # leg = Legend(ax, legend_points,["year " + str(round(x/(52*7),2)) for x in boosters_only_vaccination_start_list],title=younger_or_older[0] +" population, high risk boosting;\nboosting commences:",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            # leg._legend_box.align = "left"
            # ax.add_artist(leg)

            print(total_severe_disease_statistics)
            # n_rows = 4
            columns = ("Mean","Median","95\% quantiles")
            rows =  [ str(round(x/(52*7),2)) +" years" for x in boosters_only_vaccination_start_list]
            rows.append("Half-yearly boosters")
            colors = boosters_start_colour_list
            colors.append(many_boosters_colour)
            cell_text = [[round(values[3],2),round(values[0],2),(round(values[1],2),round(values[2],2))] for key,values in total_severe_disease_statistics.items()]

            ####### table of statistics instead of legend 
            the_table = ax_table.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns,
                        loc='center',
                        colWidths=[0.12,0.12,0.24])
            cell = the_table[2,-1]
            cell.get_text().set_color('white')
            cell = the_table[3,-1]
            cell.get_text().set_color('white')
            cell = the_table[4,-1]
            cell.get_text().set_color('white')
            cell = the_table[5,-1]
            cell.get_text().set_color('white')

            for i in [1,2,3,4,5]:
                cell = the_table[i,-1]
                cell.set_height(0.18)

            cellDict = the_table.get_celld()
            for i in range(0,len(columns)):
                cellDict[(0,i)].set_height(.3)
                for j in range(0,len(cell_text)+1):
                    cellDict[(j,i)].set_height(.18)


            ########## the little timeline plots
            ax3.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
            ax4.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
            ax3.set_xlim([0,max_days])
            ax4.set_xlim([0,max_days])
            ax3.set_yticklabels([])
            ax4.set_yticklabels([])

            legend0 = []
            marker = "s"
            # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]
            legend0.append(ax3.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend0.append(ax3.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))

            ax3.set_facecolor(BA1_colour)
            ax3.axvspan(immune_escape_time,max_days,facecolor=BA45_colour ,zorder=0)
            ax3.axvspan(0,first_exposure_time,facecolor="#cfcfcf",zorder=0)
            


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
            ax4.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)

            for boosting_time in boosters_only_vaccination_start_list:
                plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                ax4.axvspan(boosting_time,boosting_time+13*7,facecolor= plot_colour ,zorder=0,hatch="/",edgecolor = edge_colour)

            ax4.set_xticks(six_months_on_day)
            ax4.set_xticklabels(x_tick_labels)
            ax4.set_xlabel('time (years)')
            ax4.legend(legend1, ["main vaccinaton program"],bbox_to_anchor=(1.01,-0.2), loc="lower left",borderaxespad=0,frameon=False)


            plt.subplots_adjust(hspace=0.9)
            
            plt.savefig(os.path.join(folder_many_boosters, "total_" + ICU_or_death+"_histogram_"+population_type+ "_fixed_boosting_group"+"_boosting_"+str(boosting_group_here)+ "_maxTP_"+str(max(local_TP_list)) +"_time"+str(timeframe[0])+"-" + str(timeframe[-1])+"_minimum-age-"+str(minimum_age)+ ".png") , bbox_inches='tight')
            plt.close()


def plot_before_vs_after_infections_ALL(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],aspect_ratio = 'equal',infections_or_deaths_plotting = "infections"):
    # third_stage_vaccination = "none", "early","reactive"

    original_program_time = 26*7*3

    immune_escape_times = [original_program_time, original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7 , original_program_time + 52*7] 

    for population_type in population_type_list:

        # fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        fig, ax = plt.subplots(1,1, figsize=(10,10))
        
        # first, some plotting to get some fake legends...
        legend_points = []
        marker='o'
    
        # if population_type=="younger":
        #     print("colours not determined yet")
        #     exit(1)
        #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        # if population_type=="older":
        legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
        legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

        for immune_escape_time in immune_escape_times:

            folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"
            presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'

            for boosting_time in boosters_only_vaccination_start_list:
                cut_time = boosting_time

                days_before = list(range(0,cut_time))
                days_after = list(range(cut_time,max_days))

                for local_TP_list in TP_segregated_list:
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
                            elif boosting_group == 'random':
                                plot_colour = random_boosting_colour
                            elif boosting_group =='none':
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
        
        x_ticks = list(range(0,max(x_limits)+1,10))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        ax.set_aspect(aspect_ratio)
        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        if population_type =="older":
            leg = Legend(ax, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        else:
            leg = Legend(ax, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
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
            plt.savefig(os.path.join(folder, "past_vs_future_waves_infections_"+ population_type +"_boosting_ALL_TIMES_maxTP_ALL_cut-time-is-boosting-time.png") , bbox_inches='tight')
            plt.close()
        elif infections_or_deaths_plotting=="deaths":
            plt.savefig(os.path.join(folder, "past_wave_vs_future_deaths_"+ population_type +"_boosting_ALL_TIMES_maxTP_ALL_cut-time-is-boosting-time.png") , bbox_inches='tight')
            plt.close()




def plot_before_vs_after_infections_ALL_animated(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],aspect_ratio = 'equal',infections_or_deaths_plotting = "infections"):
    # third_stage_vaccination = "none", "early","reactive"

    original_program_time = 26*7*3

    immune_escape_times = [original_program_time, original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7 , original_program_time + 52*7] 

    for population_type in population_type_list:

        # fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        fig, ax = plt.subplots(1,1, figsize=(16,7))
        
        # first, some plotting to get some fake legends...
        legend_points = []
        marker='o'
    
        # if population_type=="younger":
        #     print("colours not determined yet")
        #     exit(1)
        #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        # if population_type=="older":
        legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
        legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

        your_list = [(i, j, k) for i in immune_escape_times for j in boosters_only_vaccination_start_list for k in TP_list]
        
        def animate(i):
            immune_escape_time, boosting_time, TP = your_list[i]

            folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"
            presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'
            cut_time = boosting_time

            days_before = list(range(0,cut_time))
            days_after = list(range(cut_time,max_days))

            for paramNum in param_list:
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)

                total_population = presim_parameters["total_population"]
                # population_type = presim_parameters["population_type"]
                # total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                # booster_fraction = presim_parameters["booster_fraction"]
                boosting_group = presim_parameters['boosting_group']
                sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                if boosting_time == sims_boosting_time or boosting_group=='none':
                    pass
                else:
                    continue
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
                elif boosting_group == 'random':
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
        
        x_ticks = list(range(0,max(x_limits)+1,10))
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

        ax.set_aspect(aspect_ratio)
        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        if population_type=="older":
            leg = Legend(ax, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        else:
            leg = Legend(ax, legend_points, ["no further boosting","pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
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

        plot_animation = matplotlib.animation.FuncAnimation(fig, animate, frames=np.arange(0,len(your_list),1),interval=500)

        folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_times[-1]) +"_outputs/"

        # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)
        if infections_or_deaths_plotting=="infections":
            plot_animation.save(os.path.join(folder, "past_vs_future_waves_infections_"+ population_type +"_boosting_ALL_TIMES_maxTP_ALL_cut-time-is-boosting-time.gif") , dpi=72, writer='imagemagick')
            
        elif infections_or_deaths_plotting=="deaths":
            plot_animation.save(os.path.join(folder, "past_wave_vs_future_deaths_"+ population_type +"_boosting_ALL_TIMES_maxTP_ALL_cut-time-is-boosting-time.gif") , dpi=72, writer='imagemagick')


        plt.close()




def plot_total_infections_violin_boosting_group(boosting_group_here = "65+",population_type_list = ["younger","older"],y_limits = [-1,60],infections_or_deaths_plotting = "infections"):
    # third_stage_vaccination = "none", "early","reactive"

    original_program_time = 26*7*3

    immune_escape_times = [original_program_time, original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7 , original_program_time + 52*7] 

    boosters_start_colour_list = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
    boosters_start_edgecolour_list = [pedatric_boosting_colour,'none','none','none']
    max_y_value = 0

    for population_type in population_type_list:

        # fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        fig, ax = plt.subplots(1,1, figsize=(8,10))
        
        # first, some plotting to get some fake legends...
        legend_points = []
        marker='o'
    
        # if population_type=="younger":
        #     print("colours not determined yet")
        #     exit(1)
        #     legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        #     legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        # if population_type=="older":

        for plot_colour,edge_colour in zip(boosters_start_colour_list,boosters_start_edgecolour_list):
                            legend_points.append(ax.scatter(-10000,-10000,color=plot_colour, s=100, marker= 'o', alpha=1.0, edgecolors=edge_colour))

        for immune_escape_time in immune_escape_times:

            folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"
            presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'

            for boosting_time in boosters_only_vaccination_start_list:
                # cut_time = boosting_time

                days_used = list(range(0,max_days))
                for paramNum in param_list:
                    presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                    presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                    with open(presimfilename, "r") as f:
                        presim_parameters = json.load(f)

                    total_population = presim_parameters["total_population"]
                    # population_type = presim_parameters["population_type"]
                    # total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                    # booster_fraction = presim_parameters["booster_fraction"]
                    boosting_group = presim_parameters['boosting_group']
                    sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

                    if boosting_time != sims_boosting_time:
                        continue 
                    else:
                        pass 

                    if boosting_group != boosting_group_here:
                        continue 
                    else:
                        pass
                    
                    for TP in TP_list:

                        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP

                        datafilename = filename + ".csv"
                        data_file = os.path.join(folder, datafilename)
                        pd_obj = pd.read_csv(data_file)

                        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                        df = new_pd.pivot(index='day', columns='sim', values='n')
                        df_dict = df.to_dict()
                        infections_per_sim = []
                        if infections_or_deaths_plotting=="deaths":
                            clinical_filename = "_full_outcomes_dataframe.csv"
                            clinical_file = os.path.join(folder,filename,clinical_filename)

                            if os.path.isfile(clinical_file):
                                pass
                            else:
                                print(clinical_file +" DOES NOT EXIST!")
                                continue

                            clinical_pd_obj = pd.read_csv(clinical_file)
                            deaths_per_sim = [] 


                        scale = 40
                        aug_num = 5
                        for simnum in df_dict.keys():
                            if infections_or_deaths_plotting=="infections":
                                infections_over_time = df_dict[simnum]
                                total_infections = sum(list_conversion_nans(infections_over_time, days_used))
                                infections_per_sim.append(total_infections)

                            elif infections_or_deaths_plotting=="deaths":
                                for aug in range(1,aug_num+1):
                                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==(simnum-1)*aug_num+aug) & (clinical_pd_obj['day'].isin(days_used))]
                                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())
                                    deaths_per_sim.append(daily_deaths) 


                        outline = 'None'

                        plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                        edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]
                        
                        if infections_or_deaths_plotting=="infections":
                            percent_infected = [x/total_population*100 for x in infections_per_sim]
                            max_y_value = max(max_y_value,max(percent_infected))
                            data_to_plot = [percent_infected]
                        elif infections_or_deaths_plotting=="deaths":
                            max_y_value = max(max_y_value,max(deaths_per_sim))
                            data_to_plot = [deaths_per_sim]

                        position = sims_boosting_time - immune_escape_time + (immune_escape_time-790)/20 # additional jittery
                        parts = ax.violinplot(data_to_plot,positions=[position], showmeans=False, showmedians=False, showextrema=False,widths = 30)

                        for pc in parts['bodies']:
                            pc.set_facecolor(plot_colour)
                            pc.set_edgecolor(edge_colour)
                            pc.set_alpha(0.7)

                
        ax.set_ylim(y_limits)
        ax.set_xlim([-400,400])

        if infections_or_deaths_plotting=="infections":
            y_ticks = list(range(0,max(y_limits)+1,20))
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(y)+"\%" for y in y_ticks])
        elif infections_or_deaths_plotting=="deaths":
            y_ticks = list(range(0,max(y_limits)+1,5))
            ax.set_yticks(y_ticks)

        print(infections_or_deaths_plotting +": max y " + str(max_y_value ))
        
       
        # ax.grid(True)
        ax.set_axisbelow(True)
        ax.grid(color='gray')
        # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

        # leg = Legend(ax, legend_points,boosters_only_vaccination_start_list,title=population_type +" population, high risk boosting; boosting times:",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
        leg = Legend(ax, legend_points,["year " + str(round(x/(52*7),2)) for x in boosters_only_vaccination_start_list],title=younger_or_older[0] +" population, high risk boosting;\nboosting commences:",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

        leg._legend_box.align = "left"
        ax.add_artist(leg)
        
        if infections_or_deaths_plotting=="infections":
            ax.set_ylabel('total attack rate')
        elif infections_or_deaths_plotting=="deaths":
            ax.set_ylabel('total deaths')
        ax.set_xlabel('boosting_time - immune_escape_time')
        
        # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)
        if infections_or_deaths_plotting=="infections":
            plt.savefig(os.path.join(folder, "total_infections_violin_"+ population_type +"_boosting_" +str(boosting_group_here)+"_maxTP_ALL_cut-time-is-boosting-time.png") , bbox_inches='tight')
            plt.close()
        elif infections_or_deaths_plotting=="deaths":
            plt.savefig(os.path.join(folder, "total_deaths_violin_"+ population_type +"_boosting_" +str(boosting_group_here)+"_maxTP_ALL_cut-time-is-boosting-time.png") , bbox_inches='tight')
            plt.close()
################################################################################################
# PLOTTING
################################################################################################
original_program_time = 26*7*3

immune_escape_times = [original_program_time, original_program_time + 52*7] 

# time dependancy
for younger_or_older in  [["older"],["younger"]]:
    if younger_or_older == ["younger"]:
        no_boosting_colour = 'white'
        pedatric_boosting_colour = 'lightskyblue'
        old_boosting_colour ='dodgerblue'
        random_boosting_colour = 'navy'
    else:
        pedatric_boosting_colour = 'salmon'
        old_boosting_colour = 'red'
        random_boosting_colour = 'firebrick'
        no_boosting_colour = 'white'

    many_boosters_colour = 'mediumpurple'
    for immune_escape_time in immune_escape_times:

        folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"
        presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'

        folder_many_boosters = "/scratch/cm37/tpl/annual_boosting_2_immune_escape_t" + str(immune_escape_time) +"_outputs/"

        plot_ribbon_infections_over_time_plus_fixed_boosting_group(boosting_group_here = "65+",younger_or_older=younger_or_older,immune_escape_time=immune_escape_time)

        total_deaths_histograms_fixed_boosting_group_with_mean(immune_escape_time,boosting_group_here = "65+",ICU_or_death='death',younger_or_older=younger_or_older,timeframe =list(range(original_program_time,max_days)))