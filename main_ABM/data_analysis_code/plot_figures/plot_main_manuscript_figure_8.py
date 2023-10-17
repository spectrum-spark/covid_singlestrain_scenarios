#
# Produces plots for Figure 8
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

age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]

days_per_stage = 7*26 # 26 weeks


############################################################


max_days = 52*3*7 # 3 years 
first_exposure_time =225
original_program_time = 26*7*3

immune_escape_time = 728
bivalent_start_time = immune_escape_time
no_vax_list = [-1,0]
param_list = [2,5]


days_per_stage = 7*26 # 26 weeks


TP_list = ["1.05", "1.95"]
TP_type_list = ['TP_low','TP_high']
population_type_list = ["younger"]
boosting_group_names =  {'none':'no further vaccination','65+':'further boosting high risk'}


boosting_time = 728
boosters_only_vaccination_duration = 13*7# i.e. about 3 months

date_values = list(range(0,max_days,10))
date_names = [str(x) for x in date_values]
local_days = list(range(max_days))




presim_parameters_folder  = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "presim_code","parameter_files_annual_boosting_1_younger"))


bivalent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","bivalent_boosting","low_coverage_immune_escape_t" + str(immune_escape_time) +"_bivalent_t"+str(bivalent_start_time) ))

monovalent_folder =os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_1_younger_immune_escape_t" + str(immune_escape_time)))


no_boosting_colour = 'white'
monovalent_boosting = 'dodgerblue'# 'lightskyblue'
bivalent_boosting ='navy'

boosting_colours = {'none': no_boosting_colour, 'monovalent':monovalent_boosting,'bivalent':bivalent_boosting}
boosting_edge_colours = {'none': 'lightskyblue', 'monovalent':'none','bivalent':'none'}
boosting_scenarios = ['none', 'monovalent','bivalent']

BA1_colour = '#a1a1a1'
BA45_colour = "#666666"
vaccinating_colour = "yellowgreen"
boosting_colour_general = "darkgreen"

max_infections=5000 



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


def plot_ribbon_infections_comparison(ax, vaccination_coverage):

    TP =  "1.95"
            
    legend_points = []
    marker='o'
    population_type = "younger"


    # making the legend
    for group in boosting_scenarios:
        legend_points.append(ax.scatter(-10000,-10000,color=boosting_colours[group], s=100, marker= 'o', alpha=1.0, edgecolors=boosting_edge_colours[group]))
    
    all_curves_over_local_days = {x:[] for x in boosting_scenarios}

    ########## no further boosting first
    boosting_scenario_here = 'none'
    boosting_group_wanted = 'none'
    for paramNum in no_vax_list:
        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
        presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

        with open(presimfilename, "r") as f:
            presim_parameters = json.load(f)

        total_vaccination_rate = presim_parameters["total_vaccination_rate"]
        boosting_group = presim_parameters['boosting_group']

        if total_vaccination_rate== vaccination_coverage: # checking that the vaccination coverage is correct
            pass
        else: continue 

        if boosting_group==boosting_group_wanted: # making sure that it's a no-further-boosting scenario
            pass
        else: continue 

        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
        print(filename)
        datafilename = filename + ".csv"
        data_file = os.path.join(monovalent_folder, datafilename)

        if os.path.isfile(data_file):
            pass
        else:
            print(data_file)
            print("This file ^ doesn't exist????")
            continue

        pd_obj = pd.read_csv(data_file)
        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
        df = new_pd.pivot(index='day', columns='sim', values='n')
        df_dict = df.to_dict()

        for simnum in df_dict.keys():
            infections_over_time = df_dict[simnum]
            infections_over_time_list = list_conversion_nans(infections_over_time, local_days)
            all_curves_over_local_days[boosting_scenario_here].append(infections_over_time_list)
    ################################################
    # next is monovalent 
    boosting_scenario_here = 'monovalent'
    boosting_group_wanted = '65+' # what it is called...
    for paramNum in param_list:
        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
        presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

        with open(presimfilename, "r") as f:
            presim_parameters = json.load(f)

        total_vaccination_rate = presim_parameters["total_vaccination_rate"]
        boosting_group = presim_parameters['boosting_group']
        sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

        if total_vaccination_rate== vaccination_coverage and sims_boosting_time==boosting_time and boosting_group==boosting_group_wanted: # checking that the vaccination coverage, scenario, is correct
            pass
        else: continue 

        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
        print(filename)
        datafilename = filename + ".csv"
        data_file = os.path.join(monovalent_folder, datafilename)

        if os.path.isfile(data_file):
            pass
        else:
            print(data_file)
            print("This file ^ doesn't exist????")
            continue

        pd_obj = pd.read_csv(data_file)
        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
        df = new_pd.pivot(index='day', columns='sim', values='n')
        df_dict = df.to_dict()

        for simnum in df_dict.keys():
            infections_over_time = df_dict[simnum]
            infections_over_time_list = list_conversion_nans(infections_over_time, local_days)
            all_curves_over_local_days[boosting_scenario_here].append(infections_over_time_list)




    ################################################
    # finally is bivalent
    boosting_scenario_here = 'bivalent'
    boosting_group_wanted = '65+' # what it is called...
    for paramNum in param_list:
        presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
        presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

        with open(presimfilename, "r") as f:
            presim_parameters = json.load(f)

        total_vaccination_rate = presim_parameters["total_vaccination_rate"]
        boosting_group = presim_parameters['boosting_group']
        sims_boosting_time = presim_parameters['boosters_only_vaccination_start']

        if total_vaccination_rate== vaccination_coverage and sims_boosting_time==boosting_time and boosting_group==boosting_group_wanted: # checking that the vaccination coverage, scenario, is correct
            pass
        else: continue 

        filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
        print(filename)
        datafilename = filename + ".csv"
        data_file = os.path.join(bivalent_folder, datafilename)

        if os.path.isfile(data_file):
            pass
        else:
            print(data_file)
            print("This file ^ doesn't exist????")
            continue

        pd_obj = pd.read_csv(data_file)
        new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
        df = new_pd.pivot(index='day', columns='sim', values='n')
        df_dict = df.to_dict()

        for simnum in df_dict.keys():
            infections_over_time = df_dict[simnum]
            infections_over_time_list = list_conversion_nans(infections_over_time, local_days)
            all_curves_over_local_days[boosting_scenario_here].append(infections_over_time_list)

    #########################

    upper_ribbon = {x:[] for x in boosting_scenarios} # for vaccinated groups
    lower_ribbon ={x:[] for x in boosting_scenarios}
    median_line = {x:[] for x in boosting_scenarios}

    for boosting_group in boosting_scenarios:
        upper_ribbon[boosting_group] = [max([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
        lower_ribbon[boosting_group] = [min([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
        median_line[boosting_group] = [np.median([all_curves_over_local_days[boosting_group][simnum][i] for simnum in range(len(all_curves_over_local_days[boosting_group]))]) for i in range(len(local_days))]
    for boosting_group in boosting_scenarios:
        plot_colour = boosting_colours[boosting_group]
        
        ax.fill_between(local_days,upper_ribbon[boosting_group],lower_ribbon[boosting_group],facecolor=plot_colour,alpha=0.5)
        # ax.plot(local_days,median_line[vax],color = plot_colour,linestyle='solid')
    for boosting_group in boosting_scenarios:
        plot_colour = boosting_colours[boosting_group]

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

    title = population_type +" population"
    if vaccination_coverage == 0.2:
        title = title + "\n(low vaccination coverage)"
    else:
        title = title + "\n(medium vaccination coverage)"
    
    bbox_x = 0.5
    if vaccination_coverage==0.5:
        bbox_x = 0.55

    leg = Legend(ax, legend_points, ["no further boosting","monovalent boosting", "bivalent boosting"],title=title, loc="upper center",bbox_to_anchor=(bbox_x,0.99),borderaxespad=0,frameon=False,  labelcolor='w', fontsize=13.5,title_fontsize=14.5,labelspacing =0.01,handletextpad=0.1)
    plt.setp(leg.get_title(), color='white')
    leg._legend_box.align = "left"
    ax.add_artist(leg)
    
    ax.set_ylabel('number of infections', fontsize=16)
    
    


def plot_figure_8():

    # make figure with 4 subplots 
    fig, ((axa,axb),(ax0,ax1)) = plt.subplots(2,2, sharex=True, gridspec_kw={'height_ratios': [6, 1]},figsize = (13,4.5))

    save_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","boosting_paper_figures"))
    if not os.path.exists(save_folder ):
        os.makedirs(save_folder )

    vaccination_coverage = 0.2
    plot_ribbon_infections_comparison(axa,vaccination_coverage)

    vaccination_coverage = 0.5
    plot_ribbon_infections_comparison(axb, vaccination_coverage)

    plot_subfigure_boosting_ribbon(ax0,boosting_time,"left")
    plot_subfigure_boosting_ribbon(ax1,boosting_time,"right")

    fig.subplots_adjust(hspace=0.1)

    axa.annotate('(a)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)
    axb.annotate('(b)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)


    plt.savefig(os.path.join(save_folder, "figure_8.png") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_8.pdf") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_8.svg") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_8.eps") , bbox_inches='tight')
    plt.close()


plot_figure_8()

