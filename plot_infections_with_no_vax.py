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


def plot_combined_infections_over_time_older_80_booster():

    max_days = 650 
    date_values = list(range(0,max_days+1,10))
    date_names = [str(x) for x in date_values]

    days = list(range(0,max_days+1))
    xlim_values= [0,max_days]
    max_infections=5000 

    fig, ax = plt.subplots(1,1, figsize=(10,4)) # 16:9

    for population_type in ["older"]:

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
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    infections_over_time_list = list_conversion_nans(infections_over_time, days)
                    ax.plot(days,infections_over_time_list,alpha=0.025,color="black") 

    ax.set_ylim([0,max_infections])
    ax.set_xlim([0,max_days])
    ax.grid(color='lightgray', linestyle='dashed')

    ax.set_xlabel('time (days)')
    ax.set_ylabel('number of infections')
    
    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_combined_older_80_booster_pop_infections_over_time.png") , bbox_inches='tight')
    plt.close()


def plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger","older"],x_limits=[15,85],y_limits = [-1,60],filter=False,aspect_ratio = 'equal'):
    if y_limits[1]>80:
        fig, ax = plt.subplots(1,1, figsize=(8,7.75)) # for the second strain
    else:
        fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    
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

    ax.plot([20, 80], [20, 80],linestyle='--',color="black")
    
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
    ax.set_xlabel('past attack rate (before t = 450)')
    

    xticks = [15,20,30,40,50,60,70,80,85]
    for x0, x1 in zip(xticks[::2], xticks[1::2]):
        plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]   

    plt.savefig(os.path.join(folder, "with_novax_infections_past_immunity_combined_population_80booster_only_horizontal_" + addition+ ".png") , bbox_inches='tight')
    plt.close()




def plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated(ICU_or_death,OG="",population_type_list = ["younger","older"],ylimits = [0,28],y_ticks = list(range(0,29,2)),x_limits=[15,85],filter=False): # or "OG_"
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
                    colour = 'white' 
                    outline ='lightskyblue'
                else:
                    colour = 'white'
                    outline='salmon'
                
                datafilename = filename + ".csv"
                data_file = os.path.join(novax_folder, datafilename)
                pd_obj = pd.read_csv(data_file)

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')
                df_dict = df.to_dict()
                infections_per_sim_before = []
                infections_per_sim_after = []

                severe_disease_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
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
                    ax.scatter(percent_infected_before, severe_disease_after, color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)
                    max_y = max(max_y,max( severe_disease_after))
                else:
                    percent_infected_before_filtered = []
                    severe_disease_after_filtered = []
                    for i in range(len(percent_infected_before)):
                        element = percent_infected_before[i]
                        if element>=20 and element<=80:
                            percent_infected_before_filtered.append(element)
                            severe_disease_after_filtered.append(severe_disease_after[i])

                    if severe_disease_after_filtered!=[]:
                        ax.scatter(percent_infected_before_filtered, severe_disease_after_filtered, color=colour, s=scale,marker= marker, alpha=0.8, edgecolors=outline)
                        max_y =max(max_y,max(severe_disease_after_filtered))



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

                severe_disease_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
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
                    ax.scatter(percent_infected_before, severe_disease_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
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
                        ax.scatter(percent_infected_before_filtered, severe_disease_after_filtered, color=colour, s=scale,marker= marker, alpha=0.8, edgecolors='none')
                        max_y = max(max_y,max( severe_disease_after_filtered))

    print(max_y)
    ax.set_xlim(x_limits)
    ax.set_ylim(ylimits)

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

    if len(population_type_list)==2:
        ax.legend(legend_points[:4], legendlist,title="younger population",bbox_to_anchor=(0.47, 1), loc=1)
        leg = Legend(ax,legend_points[4:], legendlist, title="older population",bbox_to_anchor=(0.47, 0.75), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points[:4], legendlist,title=population_type_list[0]+" population",bbox_to_anchor=(0.47, 1), loc=1)

    xticks = [15,20,30,40,50,60,70,80,85]
    for x0, x1 in zip(xticks[::2], xticks[1::2]):
        plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]  

    if ICU_or_death == 'death':
        ax.set_ylabel('near-future deaths (t = 450 to 650)')
        #ax.set_title('Deaths given past hybrid immunity',fontsize=14)

        plt.savefig(os.path.join(folder, "with_novax_deaths_vs_past_immunity"+OG+"_ages_80_booster_only_horizontal_"+addition+"_updated.png") , bbox_inches='tight')
        plt.close()
    elif ICU_or_death =='ICU':
        ax.set_ylabel('near-future ICU admissions (t = 450 to 650)')
        #ax.set_title('ICU admissions given past immunity',fontsize=14)

        plt.savefig(os.path.join(folder,"with_novax_ICU_admissions_vs_past_immunity"+OG+"_ages_80_booster_only_horizontal_"+addition+"_updated.png") , bbox_inches='tight')
        plt.close()
       

################################################################################################
# SAME VARIANT FOR BOTH WAVES (updated vaccine efficacy)
################################################################################################

folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_rerun_outputs")
presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files")
novax_folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_no_vax_outputs")
novax_presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files_no_vax")

plot_combined_infections_over_time_older_80_booster()

plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],x_limits=[19,81], y_limits = [-1,65],filter=True)
plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],x_limits=[19,81], y_limits = [-1,65],filter=True)


plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"],ylimits=[-1,30],y_ticks = list(range(0,31,5)),x_limits=[19,81],filter=True)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["older"],ylimits=[-1,30],y_ticks = list(range(0,31,5)),x_limits=[19,81],filter=True)

plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["younger"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["older"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)





################################################################################################
# NEW STRAIN FOR THE SECOND WAVE
################################################################################################

folder = '/scratch/cm37/tpl/covid_no_ttiq_450-2_ibm_4th_doses_newstrainBA45like_outputs/'
presim_parameters_folder  = '/fs02/cm37/prod/Le/covid-abm-presim/continuous_sim_param_files/'
novax_folder = '/scratch/cm37/tpl/covid_no_ttiq_450-2_ibm_4th_doses_newstrainBA45like_no_vax_outputs/'
novax_presim_parameters_folder =  '/fs02/cm37/prod/Le/covid-abm-presim/continuous_sim_param_files_no_vax/'

plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,100],x_limits=[19,81],filter=True)
plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],y_limits = [-1,100],x_limits=[19,81],filter=True)

plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["older"],ylimits=[-1,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["younger"],ylimits=[0,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["older"],ylimits=[0,50],y_ticks = list(range(0,51,5)),x_limits=[19,81],filter=True)




################################################################################################
# SAME VARIANT FOR BOTH WAVES, WORSE VACCINES
################################################################################################

folder = '/scratch/cm37/tpl/covid_continuous_simulations_double_exposure_no_ttiq_450-2_outputs/'
presim_parameters_folder  = '/fs02/cm37/prod/Le/covid-abm-presim/continuous_sim_param_files/'
novax_folder = '/scratch/cm37/tpl/covid_continuous_simulations_double_exposure_no_ttiq_450-2_no_vax_outputs/'
novax_presim_parameters_folder =  '/fs02/cm37/prod/Le/covid-abm-presim/continuous_sim_param_files_no_vax/'

plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"],y_limits = [-1,70],x_limits=[19,81],filter=True)
plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"],y_limits = [-1,70],x_limits=[19,81],filter=True)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["younger"],ylimits=[-1,90],y_ticks = list(range(0,91,10)),x_limits=[19,81],filter=True)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('death',OG="",population_type_list = ["older"],ylimits=[-1,90],y_ticks = list(range(0,91,10)),x_limits=[19,81],filter=True)

# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["younger"],ylimits=[-1,120],y_ticks = list(range(0,201,20)),x_limits=[19,81],filter=True)
# plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal_updated('ICU',OG="",population_type_list = ["older"],ylimits=[-1,120],y_ticks = list(range(0,201,20)),x_limits=[19,81],filter=True)