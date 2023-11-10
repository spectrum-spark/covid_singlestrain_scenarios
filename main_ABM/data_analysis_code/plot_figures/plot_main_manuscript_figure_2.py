#
# Produces epidemic wave plots the main manuscript Figure 2 (boosting in high-coverage populations)
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


param_list = list(range(0,12+1))

max_days = 52*3*7 # 3 years 
first_exposure_time =225

original_program_time = 26*7*3
boosters_only_vaccination_start_list = [original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7  , original_program_time + 52*7 ]
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

date_values = list(range(0,max_days,10))
date_names = [str(x) for x in date_values]

local_days = list(range(max_days))

max_infections=5000 

BA1_colour = '#a1a1a1'
BA45_colour = "#666666"
vaccinating_colour = "yellowgreen"
boosting_colour_general = "darkgreen"


def plot_subfigure_boosting_ribbon(ax,boosting_time,side):
    legend0 = []
    marker = "s"
    # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]

    if side == "left":
        legend0.append(ax.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
        legend0.append(ax.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
        legend_labels = ["circulating BA.1","circulating BA.4/5"]
    elif side=="right":
        legend0.append(ax.scatter(-10000,-10000,color=vaccinating_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
        legend0.append(ax.scatter(-10000,-10000,color=boosting_colour_general, s=100, marker= marker, alpha=1.0, edgecolors='none'))
        legend_labels = [ "main vaccination program","further boosting program"]

    # little vaccination bar 
    ax.set_xlabel('time (years)', fontsize=16)
    ax.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
    ax.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)
    ax.axvspan(boosting_time,boosting_time+13*7,facecolor= boosting_colour_general,zorder=0)
    
    days_per_six_months = 26*7
    six_months_on_day = [i*days_per_six_months for i in range(7) ]
    x_tick_labels = ["0", "0.5", "1","1.5","2","2.5","3"]
    ax.set_xticks(six_months_on_day)
    ax.set_xticklabels(x_tick_labels,fontsize=13)

    ax.set_ylim([0,1])
    ax.set_yticklabels([])
    ax.set_xlim([min(local_days),max_days])

    ax.legend(legend0, legend_labels,bbox_to_anchor=(0.5, -1.1), loc="upper center",borderaxespad=0,frameon=False,ncol = 2, fontsize=14,labelspacing =0.1,handletextpad=0.1)

def plot_subfigure_ribbon_infections_over_time_plus(ax, folder, presim_parameters_folder, boosting_colours, scenario_list, younger_or_older=["older"],immune_escape_time=546):

    no_boosting_colour, pedatric_boosting_colour, old_boosting_colour, random_boosting_colour = boosting_colours

    param_list, boosters_only_vaccination_start_list, TP_segregated_list= scenario_list

    for boosting_time in boosters_only_vaccination_start_list:

        for local_TP_list in TP_segregated_list:
            legend_points = []
            marker='o'

            for population_type in younger_or_older:
                    
                legend_points.append(ax.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors=pedatric_boosting_colour))
                legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
                legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

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

           
            
            days_per_year = 52*7 
            days_per_six_months = 26*7
            six_months_on_day = [i*days_per_six_months for i in range(7) ]
            x_tick_labels = ["0", "0.5", "1","1.5","2","2.5","3"]
            ax.set_xticks(six_months_on_day)
            ax.set_xticklabels(x_tick_labels,fontsize=13)
            
           

            ax.set_ylim([0,max_infections])
            ax.set_xlim([min(local_days),max_days])
            # ax.set_xlabel('time (days)')
            ax.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8)

            ax.tick_params(axis='y', labelsize=13)
            
             
            arrow_len = -600
            arrow_pos = 100 - arrow_len
            ax.arrow(x=first_exposure_time-25, y=arrow_pos, dx=0+25, dy=arrow_len, width=5, head_width=19, head_length=100,facecolor='black', edgecolor='none')
            # ax.annotate('importations begin', xy = (first_exposure_time-5, arrow_pos+150),rotation=90,color="white",size=15)
            ax.annotate('importations begin', xy = (first_exposure_time-50, arrow_pos+150),rotation=90,color="black",size=15)

            

            # ax.set_facecolor('silver')
            ax.set_facecolor(BA1_colour)
            ax.axvspan(immune_escape_time,max_days,facecolor=BA45_colour ,zorder=0)
            ax.axvspan(0,first_exposure_time,facecolor="#cfcfcf",zorder=0)

            

            if population_type=="older":
                legend_labels = ["no further boosting", "pediatric boosting (ages 5-15)","high risk boosting (65+)", "random boosting"]
                legend_labels = ["no further boosting", "pediatric boosting","high risk boosting (65+)", "random boosting"]
            else:
                legend_labels = ["no further boosting", "pediatric boosting (ages 5-15)","high risk boosting (55+)", "random boosting"]

                legend_labels = ["no further boosting", "pediatric boosting","high risk boosting (55+)", "random boosting"]
            
            if immune_escape_time==original_program_time:
                pass 
            else:
                leg = Legend(ax, legend_points,legend_labels ,title=younger_or_older[0] +" population", loc="upper center",bbox_to_anchor=(0.55,0.975),borderaxespad=0,frameon=False,  labelcolor='w', fontsize=14,title_fontsize=15,labelspacing =0.1,handletextpad=0.1)
            
                plt.setp(leg.get_title(), color='white')
                leg._legend_box.align = "left"
                ax.add_artist(leg)
            
            ax.set_ylabel('number of infections', fontsize=16)


def plot_figure_2():
    param_list = [0,4,5,6] # 2.0 year boosting scenarios (for no boosting, and boosting to different groups)
    boosters_only_vaccination_start_list = [original_program_time + 26*7 ] # 2.0 year boosting only
    boosting_time = original_program_time + 26*7 
    TP_segregated_list = [TP_high] # high TP only
    local_TP_list = TP_high

    presim_parameters_folder  = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "presim_code","parameter_files_annual_boosting_1"))
    

    # make figure with 6 subplots 
    fig, ((axa,axb),(axc,axd),(ax0,ax1)) = plt.subplots(3,2, sharex=True, gridspec_kw={'height_ratios': [6, 6, 1]},figsize = (13,7.5))

    younger_or_older =["older"]
    pedatric_boosting_colour = 'salmon'
    old_boosting_colour = 'red'
    random_boosting_colour = 'firebrick'
    no_boosting_colour = 'white'

    boosting_colours = [no_boosting_colour, pedatric_boosting_colour, old_boosting_colour, random_boosting_colour]
    scenario_list = [param_list, boosters_only_vaccination_start_list, TP_segregated_list]

    save_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","boosting_paper_figures"))
    if not os.path.exists(save_folder ):
        os.makedirs(save_folder )
    

    # Figure 1 a

    immune_escape_time = original_program_time
    folder =os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_1_immune_escape_t" + str(immune_escape_time)))

    plot_subfigure_ribbon_infections_over_time_plus(axa, folder, presim_parameters_folder, boosting_colours,scenario_list, younger_or_older=younger_or_older,immune_escape_time=immune_escape_time)


    # Figure 1 c

    immune_escape_time=original_program_time + 52*7
    folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_1_immune_escape_t" + str(immune_escape_time)))

    plot_subfigure_ribbon_infections_over_time_plus(axc, folder, presim_parameters_folder, boosting_colours, scenario_list, younger_or_older=younger_or_older,immune_escape_time=immune_escape_time)

    plot_subfigure_boosting_ribbon(ax0,boosting_time,"left")


    younger_or_older = ["younger"]
    no_boosting_colour = 'white'
    pedatric_boosting_colour = 'lightskyblue'
    old_boosting_colour ='dodgerblue'
    random_boosting_colour = 'navy'
    boosting_colours = [no_boosting_colour, pedatric_boosting_colour, old_boosting_colour, random_boosting_colour]

    # Figure 1 b

    immune_escape_time = original_program_time
    folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_1_immune_escape_t" + str(immune_escape_time)))

    plot_subfigure_ribbon_infections_over_time_plus(axb, folder, presim_parameters_folder, boosting_colours, scenario_list,younger_or_older=younger_or_older,immune_escape_time=immune_escape_time)


    # Figure 1 d

    immune_escape_time = original_program_time + 52*7
    folder =os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_1_immune_escape_t" + str(immune_escape_time)))

    plot_subfigure_ribbon_infections_over_time_plus(axd, folder, presim_parameters_folder, boosting_colours, scenario_list,younger_or_older=younger_or_older,immune_escape_time=immune_escape_time)

    plot_subfigure_boosting_ribbon(ax1,boosting_time, "right")

    # fig.subplots_adjust(right=0.2,top=0.2)

    fig.subplots_adjust(hspace=0.1)

    axa.annotate('(a)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)
    axb.annotate('(b)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)
    axc.annotate('(c)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)
    axd.annotate('(d)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)

    plt.savefig(os.path.join(save_folder, "figure_2.png") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_2.pdf") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_2.svg") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_2.eps") , bbox_inches='tight')

    plt.close()



plot_figure_2()