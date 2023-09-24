#
# Produces plots for Figure 7a, 7b
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

max_days = 52*3*7 # 3 years 
first_exposure_time =225

original_program_time = 26*7*3

boosters_only_vaccination_duration = 13*7# i.e. about 3 months

date_values = list(range(0,max_days,10))
date_names = [str(x) for x in date_values]

# days = list(range(0,max_days+1))
local_days = list(range(max_days))

no_boosting_colour = 'white'
pedatric_boosting_colour = 'lightskyblue'
old_boosting_colour ='dodgerblue'
random_boosting_colour = 'navy' # technically the new primary boosting 

max_infections=5000 

BA1_colour = '#a1a1a1'
BA45_colour = "#666666"
vaccinating_colour = "yellowgreen"
boosting_colour_general = "darkgreen"

def plot_subfigure_boosting_ribbon(ax,boosting_time):
    legend0 = []
    marker = "s"
    # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]

    legend0.append(ax.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
    legend0.append(ax.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))

    legend0.append(ax.scatter(-10000,-10000,color=vaccinating_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
    legend0.append(ax.scatter(-10000,-10000,color=boosting_colour_general, s=100, marker= marker, alpha=1.0, edgecolors='none'))
    legend_labels = [ "circulating BA.1","circulating BA.4/5", "main vaccinaton program","further boosting program"]

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



def plot_ribbon_infections_over_time_plus(ax, all_other_parameters, younger_or_older=["older"],immune_escape_time=546):
    
    folder, presim_parameters_folder,boosting_time,local_TP_list,vaccination_coverage  = all_other_parameters
    
    legend_points = []
    marker='o'

    for population_type in younger_or_older:

        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='lightskyblue'))
            legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

            
        if population_type=="older":
            
            legend_points.append(ax.scatter(-10000,-10000,color='white', s=100, marker= 'o', alpha=1.0, edgecolors='salmon'))
            legend_points.append(ax.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=old_boosting_colour , s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= 'o', alpha=1.0, edgecolors='none'))

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

    title = younger_or_older[0] +" population"
    if vaccination_coverage == 0.2:
        title = title + "\n(low vaccination coverage)"
    else:
        title = title + "\n(medium vaccination coverage)"

   
    leg = Legend(ax, legend_points, ["no further boosting", "new pediatric vaccination","high risk boosting", "new primary vaccinations"],title=title, loc="upper center",bbox_to_anchor=(0.5,0.975),borderaxespad=0,frameon=False,  labelcolor='w', fontsize=14,title_fontsize=15,labelspacing =0.1,handletextpad=0.1)
    plt.setp(leg.get_title(), color='white')
    leg._legend_box.align = "left"
    ax.add_artist(leg)
    
    ax.set_ylabel('number of infections', fontsize=16)
    
                

def plot_figure_7ab():
    original_program_time = 26*7*3

    immune_escape_time = original_program_time + 26*7
    save_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","boosting_paper_figures"))
    if not os.path.exists(save_folder ):
        os.makedirs(save_folder )

    # figure with 3 subplots
    fig, (axa, axb,ax0) = plt.subplots(3,1, sharex=True, gridspec_kw={'height_ratios': [6,6, 1]},figsize = (7.5,7.5))


    folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_1_younger_immune_escape_t" + str(immune_escape_time)))
    presim_parameters_folder  =  os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "presim_code","parameter_files_annual_boosting_1_younger"))

    # boosters_only_vaccination_start_list = [original_program_time + 26*7]
    boosting_time = original_program_time + 26*7
    local_TP_list = TP_high 

    vaccination_coverage = 0.2
    all_other_parameters = [folder, presim_parameters_folder,boosting_time,local_TP_list,vaccination_coverage ]

    plot_ribbon_infections_over_time_plus(axa, all_other_parameters,younger_or_older=["younger"],immune_escape_time=immune_escape_time)


    vaccination_coverage = 0.5
    all_other_parameters = [folder, presim_parameters_folder,boosting_time,local_TP_list,vaccination_coverage ]
    plot_ribbon_infections_over_time_plus(axb, all_other_parameters,younger_or_older=["younger"],immune_escape_time=immune_escape_time)

    plot_subfigure_boosting_ribbon(ax0,boosting_time)

    fig.subplots_adjust(hspace=0.1)

    axa.annotate('(a)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)
    axb.annotate('(b)',
            xy=(.025, .975), xycoords='axes fraction',
            horizontalalignment='left', verticalalignment='top',
            fontsize=16)


    plt.savefig(os.path.join(save_folder, "figure_7ab.png") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_7ab.pdf") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_7ab.svg") , bbox_inches='tight')

    plt.savefig(os.path.join(save_folder, "figure_7ab.eps") , bbox_inches='tight')

    plt.close()

plot_figure_7ab()