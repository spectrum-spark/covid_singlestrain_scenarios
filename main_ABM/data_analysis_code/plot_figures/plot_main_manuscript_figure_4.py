
#
# Produces epidemic wave plots the main manuscript Figure 4
#


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

def plot_subfigures_boosting_ribbons(ax_single,ax_many,boosting_colours):

    no_boosting_colour, pedatric_boosting_colour, old_boosting_colour, random_boosting_colour,many_boosters_colour = boosting_colours

    boosters_start_colour_list = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
    boosters_start_edgecolour_list = [pedatric_boosting_colour,'none','none','none']


    legend0 = []
    marker = "s"
    # ["circulating BA.1","circulating BA.4/5", "vaccination occuring"]

    p1 =ax_many.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')
    p2 = ax_many.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')
    p3 = ax_many.scatter(-10000,-10000,color=vaccinating_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')

    p4 =  ax_many.scatter(-10000,-10000,color=no_boosting_colour, s=100, marker= marker, alpha=1.0, edgecolors=pedatric_boosting_colour)
    p5 = ax_many.scatter(-10000,-10000,color=pedatric_boosting_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')
    p6 = ax_many.scatter(-10000,-10000,color=old_boosting_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')
    p7 = ax_many.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')
    p8 = ax_many.scatter(-10000,-10000,color=random_boosting_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')

    p9 = ax_many.scatter(-10000,-10000,color=many_boosters_colour, s=100, marker= marker, alpha=1.0, edgecolors='none')

    legend0 = [p1,p2,p3,(p4,p5,p6,p7,p8,p9)]         

    # legend0.append(ax_many.scatter(-10000,-10000,color=BA1_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
    # legend0.append(ax_many.scatter(-10000,-10000,color=BA45_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))
    # legend0.append(ax_many.scatter(-10000,-10000,color=vaccinating_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))



    ax_many.set_xlabel('time (years)', fontsize=16)
    ax_single.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')
    ax_many.grid(color='#878787', linestyle=(0, (5, 1)),alpha=0.8,axis='x')

    # little vaccination bar 
    ax_single.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)
    latch_open = True
    for boosting_time in boosters_only_vaccination_start_list:
        plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(boosting_time)]
        edge_colour = boosters_start_edgecolour_list[boosters_only_vaccination_start_list.index(boosting_time)]
        if latch_open:
            ax_single.axvspan(boosting_time,boosting_time+13*7,facecolor= plot_colour ,zorder=0,hatch="/",edgecolor = edge_colour)
            latch_open = False
        else:
            ax_single.axvspan(boosting_time,boosting_time+13*7,facecolor= plot_colour ,zorder=0,edgecolor = edge_colour)

    ax_single.set_yticklabels([])

    # legend0.append(ax.scatter(-10000,-10000,color=many_boosters_colour, s=100, marker= marker, alpha=1.0, edgecolors='none'))


    

    ax_many.axvspan(min(local_days),546,facecolor= vaccinating_colour,zorder=0)
    for boosting_time in [637,637+7*26,637+7*52]:
        plot_colour = many_boosters_colour
        edge_colour = many_boosters_colour
        ax_many.axvspan(boosting_time,boosting_time+13*7,facecolor= plot_colour ,zorder=0,edgecolor = edge_colour) # hatch="/",

    ax_many.set_yticklabels([])

    legend_labels = ["circulating BA.1","circulating BA.4/5", "main vaccination program", "further boosting programs"]

    # ax_many.legend(legend0, legend_labels,bbox_to_anchor=(0.5, -1), loc="upper center",borderaxespad=0,frameon=False,ncol=2,fontsize=14,labelspacing =0.1,handletextpad=0.1,handler_map = {tuple: matplotlib.legend_handler.HandlerTuple(None)})

    # from matplotlib.legend_handler import HandlerTuple 
    # handler_map={tuple: HandlerTuple(ndivide=None)}

    return legend0,legend_labels



def plot_subfigure_ribbon_infections_over_time_plus_fixed_boosting_group(ax,all_other_parameters, boosting_group_here = "65+",younger_or_older=["older"],immune_escape_time=546):

    boosting_colours, folder, presim_parameters_folder, folder_many_boosters = all_other_parameters

    no_boosting_colour, pedatric_boosting_colour, old_boosting_colour, random_boosting_colour,many_boosters_colour = boosting_colours
    

    boosters_start_colour_list = [no_boosting_colour,pedatric_boosting_colour,old_boosting_colour,random_boosting_colour]
    boosters_start_edgecolour_list = [pedatric_boosting_colour,'none','none','none']


    for local_TP_list in [TP_high]:
        for population_type in younger_or_older:
            legend_points = []
            marker='o'
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
                        # plot_colour = boosters_start_colour_list[boosters_only_vaccination_start_list.index(sims_boosting_time)]
                        # ax.plot(local_days,infections_over_time_list,color = plot_colour,linestyle='solid',alpha=0.5)
            
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
                    # plot_colour = many_boosters_colour
                    # ax.plot(local_days,infections_over_time_list,color = plot_colour,linestyle='solid',alpha=0.1)
            
            upper_ribbon_many_boosters = [max([all_curves_over_local_days[simnum][i] for simnum in range(len(all_curves_over_local_days))]) for i in range(len(local_days))]
            lower_ribbon_many_boosters =   [min([all_curves_over_local_days[simnum][i] for simnum in range(len(all_curves_over_local_days))]) for i in range(len(local_days))]
            median_line_many_boosters =  [np.median([all_curves_over_local_days[simnum][i] for simnum in range(len(all_curves_over_local_days))]) for i in range(len(local_days))]


            ax.fill_between(local_days,upper_ribbon_many_boosters,lower_ribbon_many_boosters,facecolor=many_boosters_colour,alpha=0.8)
        
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

            
            
            
            legend_names = [str(round(x/(52*7),2)) + " years"  for x in boosters_only_vaccination_start_list]
            legend_names.append("Half-yearly boosters")

            if population_type=="older":
                legend_title = younger_or_older[0] +" population, high risk\nboosting (65+) starts at:"
            else:
                legend_title = younger_or_older[0] +" population, high risk\nboosting (55+) starts at:"

            if immune_escape_time==original_program_time:
                pass 
                # leg = Legend(ax, legend_points,legend_names,title=legend_title, loc="upper right",borderaxespad=0,frameon=False,labelcolor='w',fontsize=14,title_fontsize=15)
                # plt.setp(leg.get_title(), color='white')
                # leg._legend_box.align = "left"
                # ax.add_artist(leg)

            else:
                leg = Legend(ax, legend_points,legend_names,title=legend_title, loc="upper center",bbox_to_anchor=(0.60,0.975),borderaxespad=0,frameon=False,labelcolor='w',fontsize=14,title_fontsize=15, labelspacing=0.1,handletextpad=0.1)
                
                plt.setp(leg.get_title(), color='white')
                leg._legend_box.align = "left"
                ax.add_artist(leg)
            
            ax.set_ylabel('number of infections', fontsize=16)
            
            
            

def plot_figure_4():
    original_program_time = 26*7*3

    immune_escape_times = [original_program_time, original_program_time + 52*7] 

    # make figure with 8 subplots 
    fig, ((axa,axb),(axc,axd),(ax0,ax1),(ax2,ax3)) = plt.subplots(4,2, sharex=True, gridspec_kw={'height_ratios': [6, 6, 1,1]},figsize = (13,8))

    ax_list = [axa,axc,axb,axd]
    ax_i = 0

    ax_time_list = [[ax0,ax2],[ax1,ax3]]
    ax_t_i = 0

    save_folder =  "/scratch/cm37/tpl/boosting_paper_figures/"

    # time dependancies
    figure_legends = []
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

        boosting_colours = [no_boosting_colour, pedatric_boosting_colour, old_boosting_colour, random_boosting_colour,many_boosters_colour]

        for immune_escape_time in immune_escape_times:
            ax = ax_list[ax_i]

            folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"
            presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'

            folder_many_boosters = "/scratch/cm37/tpl/annual_boosting_2_immune_escape_t" + str(immune_escape_time) +"_outputs/"

            all_other_parameters = [boosting_colours, folder, presim_parameters_folder, folder_many_boosters]

            plot_subfigure_ribbon_infections_over_time_plus_fixed_boosting_group(ax,all_other_parameters, boosting_group_here = "65+",younger_or_older=younger_or_older,immune_escape_time=immune_escape_time)

            ax_i+=1

        ax_single, ax_many = ax_time_list[ax_t_i]
        legend0,legend_labels = plot_subfigures_boosting_ribbons(ax_single,ax_many,boosting_colours)
        figure_legends.append([legend0,legend_labels])
        ax_t_i +=1

    bottom_legend = []
    bottom_legend_labels = []

    older_legend, younger_legend = figure_legends
    legend0, legend_labels = older_legend
    p1,p2,p3,(p4,p5,p6,p7,p8,p9) = legend0
    legend1, legend_labels = younger_legend
    p1,p2,p3,(p4a,p5a,p6a,p7a,p8a,p9a) = legend1

    bottom_legend_labels = legend_labels

    bottom_legend = [p1,p2,p3,(p4,p5,p6,p7,p8,p4a,p5a,p6a,p7a,p8a,p9a)]


    # fig.legend(bottom_legend, bottom_legend_labels,bbox_to_anchor=(0.5, -1), loc="upper center",borderaxespad=0,frameon=False,ncol=3,fontsize=14,labelspacing =0.1,handletextpad=0.1,handler_map = {tuple: matplotlib.legend_handler.HandlerTuple(None)})

    # from matplotlib.legend_handler import HandlerTuple 
    # handler_map={tuple: HandlerTuple(ndivide=None)}

    fig.legend(bottom_legend, bottom_legend_labels,bbox_to_anchor=(0.5, 0.05), loc="upper center",borderaxespad=0,frameon=False,ncol=4,fontsize=14,labelspacing =0.1,handler_map = {tuple: matplotlib.legend_handler.HandlerTuple(ndivide=None, pad=1.0)})

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
    
    plt.savefig(os.path.join(save_folder, "figure_4.png") , bbox_inches='tight')
    plt.savefig(os.path.join(save_folder, "figure_4.pdf") , bbox_inches='tight')
    plt.savefig(os.path.join(save_folder, "figure_4.svg") , bbox_inches='tight')
    plt.savefig(os.path.join(save_folder, "figure_4.eps") , bbox_inches='tight')


    plt.close()

plot_figure_4()