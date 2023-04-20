#
# Produces plots for "bivalent boosting" scenarios (low coverage younger population)
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




presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1_younger/'

bivalent_folder = "/scratch/cm37/tpl/bivalent_boosting/low_coverage_immune_escape_t" + str(immune_escape_time) +"_bivalent_t"+str(bivalent_start_time) +"_outputs/"

monovalent_folder = "/scratch/cm37/tpl/annual_boosting_1_younger_immune_escape_t" + str(immune_escape_time) +"_outputs/"




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

def plot_ribbon_infections_comparison():
    max_infections=5000 

    for TP,TP_type in zip(TP_list,TP_type_list):

        for vaccination_coverage  in [0.2,0.5]:
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

            for population_type in population_type_list:

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

            leg = Legend(ax, legend_points, ["no further boosting","monovalent high risk boosting (65+ first)", "bivalent high risk boosting (65+ first)"],title=population_type +" population",bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)
            leg._legend_box.align = "left"
            ax.add_artist(leg)
            
            ax.set_ylabel('number of infections')
            
            plt.savefig(os.path.join(bivalent_folder, "ribbon_infections_over_time_plus_"+population_type+ "_vax_"+str(vaccination_coverage)+ "_boosting_"+str(boosting_time)+ "_TP_"+str(TP) + ".png") , bbox_inches='tight')
            plt.close()



def total_deaths_histograms_with_mean(boosting_time,immune_escape_time,ICU_or_death='death',younger_or_older=["older"],timeframe =local_days,minimum_age = 0):

    for TP in TP_list:
        for vaccination_coverage  in [0.2,0.5]:
            fig, ((ax2,ax_table),(ax3,ax5),(ax4,ax6)) = plt.subplots(3,2,gridspec_kw={'height_ratios': [7, 1,1],'width_ratios':[1,1]}, figsize=(13,5))

            ax_table.axis("off")
            ax5.axis("off")
            ax6.axis("off")

            legend_points = []
            marker = "o" # "s"
            total_severe_disease_statistics = {group:[] for group in boosting_scenarios} 
            for population_type in younger_or_older:
                # making the legend
                for group in boosting_scenarios:
                    legend_points.append(ax2.scatter(-10000,-10000,color=boosting_colours[group], s=100, marker= 'o', alpha=1.0, edgecolors=boosting_edge_colours[group]))

                # total_infections_local_days =  {group:[] for group in boosting_groups} 
                total_severe_disease_local_days = {group:[] for group in boosting_scenarios} 


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

                    if total_vaccination_rate== vaccination_coverage and boosting_group==boosting_group_wanted: # checking that the vaccination coverage and scenario is correct
                        pass
                    else: continue 

                    filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                    print(filename)
            

                    clinical_filename = "_full_outcomes_dataframe.csv"
                    clinical_file = os.path.join(monovalent_folder,filename,clinical_filename)

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
                        total_severe_disease_local_days[boosting_scenario_here] = daily_deaths
                        print("=============daily deaths")
                        print(daily_deaths)
                    elif ICU_or_death =='ICU':
                        daily_ICU_admissions =clinical_pd_obj['daily_ICU_admissions'].to_list()
                        total_severe_disease_local_days[boosting_scenario_here] = daily_ICU_admissions
                
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

                    clinical_filename = "_full_outcomes_dataframe.csv"
                    clinical_file = os.path.join(monovalent_folder,filename,clinical_filename)

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
                        total_severe_disease_local_days[boosting_scenario_here] = daily_deaths
                        print("=============daily deaths")
                        print(daily_deaths)
                    elif ICU_or_death =='ICU':
                        daily_ICU_admissions =clinical_pd_obj['daily_ICU_admissions'].to_list()
                        total_severe_disease_local_days[boosting_scenario_here] = daily_ICU_admissions


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

                    clinical_filename = "_full_outcomes_dataframe.csv"
                    clinical_file = os.path.join(bivalent_folder,filename,clinical_filename)

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
                        total_severe_disease_local_days[boosting_scenario_here] = daily_deaths
                        print("=============daily deaths")
                        print(daily_deaths)
                    elif ICU_or_death =='ICU':
                        daily_ICU_admissions =clinical_pd_obj['daily_ICU_admissions'].to_list()
                        total_severe_disease_local_days[boosting_scenario_here] = daily_ICU_admissions





                outline = 'none'
                for boosting_group in boosting_scenarios:
                    plot_colour = boosting_colours[boosting_group]
                    outline =  plot_colour
                    
                    # ax.hist(total_infections_local_days[boosting_group], bins=10, alpha=0.5, color=plot_colour)
                    mean = np.mean(total_severe_disease_local_days[boosting_group])
                    median = np.median(total_severe_disease_local_days[boosting_group])
                    lower_quantile = np.quantile(total_severe_disease_local_days[boosting_group],0.025)
                    upper_quantile = np.quantile(total_severe_disease_local_days[boosting_group],0.975)
                    total_severe_disease_statistics[boosting_group] = [median,lower_quantile,upper_quantile,mean]

                    ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, alpha=0.5, color=plot_colour,histtype='bar')
                    ax2.hist(total_severe_disease_local_days[boosting_group],bins=10, facecolor="none", edgecolor=outline, histtype='step')
            

            ax2.set_ylabel('Count')
            ax2.set_xlim(0,80)
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
            
            print(total_severe_disease_statistics)
            # n_rows = 4
            columns = ("Mean","Median","95\% quantiles")
            rows =   ["no further boosting", "monovalent high risk boosting", "bivalent high risk boosting"]
            colors = [no_boosting_colour ,monovalent_boosting ,bivalent_boosting]
            cell_text = [[round(values[3],2),round(values[0],2),(round(values[1],2),round(values[2],2))] for boosting_group,values in total_severe_disease_statistics.items()]

            ####### table of statistics instead of legend 
            the_table = ax_table.table(cellText=cell_text,
                        rowLabels=rows,
                        rowColours=colors,
                        colLabels=columns,
                        loc='center',
                        colWidths=[0.11,0.11,0.22])
            cell = the_table[2,-1]
            cell.get_text().set_color('white')
            cell = the_table[3,-1]
            cell.get_text().set_color('white')
            

            for i in [1,2,3]:
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
            
            plt.savefig(os.path.join(bivalent_folder, "total_" + ICU_or_death+"_histogram_with_mean_"+"_".join(younger_or_older) + "_vax_" + str(vaccination_coverage)+ "_"+"_boosting_"+str(boosting_time)+ "_TP_"+str(TP) +"_time"+str(round(timeframe[0]/(52*7),2))+"-" + str(round(timeframe[-1]/(52*7),2))+"years_minimum-age-"+str(minimum_age)+ ".png") , bbox_inches='tight')
            plt.close()


################################################################################################
# PLOTTING
################################################################################################

total_deaths_histograms_with_mean(boosting_time,immune_escape_time,ICU_or_death='death',younger_or_older=["younger"],timeframe =list(range(original_program_time,max_days)),minimum_age = 0)

plot_ribbon_infections_comparison()





