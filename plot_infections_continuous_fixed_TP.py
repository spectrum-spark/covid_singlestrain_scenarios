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

# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_3_outputs")
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_400_outputs")

# TP_list = ["1.75","2.0","2.25","2.5","2.75"]

# TP_list = ["0.95","1.0","1.05", "1.1","1.15", "1.2000000000000002","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95"]

# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs")

# TP_list = ["0.8","0.9","1.0", "1.1","1.2000000000000002","1.3","1.4","1.5","1.6"]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_outputs")

TP_list = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_rerun_outputs")
population_list = list(range(1,6+1))
presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files")
SIM_NUMBER = 10

folder =  os.path.join(os.path.dirname(__file__),"..","covid_no_ttiq_450-2_ibm_4th_doses_newstrain_outputs")




def plot_before_vs_after_infections():

    for population_type in ["younger","older"]:
        fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        # first, some plotting to get some fake legends...
        ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='navy', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='grey', s=100, marker= 'o', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='grey', s=100, marker= 'x', alpha=1.0, edgecolors='none')
        legend_list = ["20\% vaccination", "50\% vaccination","80\% vaccination","50\% booster-new primary division","80\% booster-new primary division"]


        for paramNum in population_list:
            for TP in TP_list:

                # colour = colour_list[colour_counter]

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if total_vaccination_rate == 0.2:
                    colour = 'lightskyblue'
                elif total_vaccination_rate == 0.5:
                    colour = 'dodgerblue'
                elif total_vaccination_rate == 0.8:
                    colour = 'navy'
                
                if booster_fraction == 0.5:
                    marker = "o"
                elif booster_fraction ==0.8:
                    marker = "x"


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

                scale = 50
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)
                
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]
                ax.scatter(percent_infected_before, percent_infected_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


        ax.set_xlim([0,100])
        ax.set_ylim([0,100])

        
        ax.grid(True)
        ax.legend(legend_list)
        ax.set_ylabel('\% of infected people after t = ' +str(time_split))
        ax.set_xlabel('\% of infected people before t = ' +str(time_split)+'("past infection")')
        ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

        plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_" +population_type +".png") , bbox_inches='tight')
        plt.close()
        


def plot_before_vs_after_infections_combined_ages():
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    # first, some plotting to get some fake legends...
    ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='navy', s=100, marker= 's', alpha=1.0, edgecolors='none')

    ax.scatter(-10000,-10000,color='salmon', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='red', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 's', alpha=1.0, edgecolors='none')
    # ax.scatter(-10000,-10000,color='yellowgreen', s=100, marker= 's', alpha=1.0, edgecolors='none')
    # ax.scatter(-10000,-10000,color='limegreen', s=100, marker= 's', alpha=1.0, edgecolors='none')
    # ax.scatter(-10000,-10000,color='darkgreen', s=100, marker= 's', alpha=1.0, edgecolors='none')


    ax.scatter(-10000,-10000,color='grey', s=100, marker= 'o', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='grey', s=100, marker= 'x', alpha=1.0, edgecolors='none')
    legend_list = ["20\% vaccination in younger population", "50\% vaccination in younger population","80\% vaccination in younger population","20\% vaccination in older population", "50\% vaccination in older population","80\% vaccination in older population","50\% booster vs new primary doses division","80\% booster vs new primary doses division"]

    for population_type in ["younger","older"]:
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
                    # if total_vaccination_rate == 0.2:
                    #     colour = 'yellowgreen'
                    # elif total_vaccination_rate == 0.5:
                    #     colour = 'limegreen'
                    # elif total_vaccination_rate == 0.8:
                    #     colour = 'darkgreen'
                    if total_vaccination_rate == 0.2:
                        colour = 'salmon'
                    elif total_vaccination_rate == 0.5:
                        colour = 'red'
                    elif total_vaccination_rate == 0.8:
                        colour = 'firebrick'

                if booster_fraction == 0.5:
                    marker = "o"
                elif booster_fraction ==0.8:
                    marker = "x"


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
                ax.scatter(percent_infected_before, percent_infected_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


    ax.set_xlim([0,85])
    ax.set_ylim([-1,60])

    ax. set_aspect('equal')
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray', linestyle='dashed')
    ax.legend(legend_list)
    ax.set_ylabel('attack rate post second infection seeding')
    ax.set_xlabel('attack rate prior second infection seeding')
    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population.png") , bbox_inches='tight')
    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population.pdf") , bbox_inches='tight')
    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population.svg") , bbox_inches='tight')
    plt.close()
        
def plot_before_vs_after_infections_older_demographic_only():
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    # first, some plotting to get some fake legends...
    ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='navy', s=100, marker= 's', alpha=1.0, edgecolors='none')


    ax.scatter(-10000,-10000,color='grey', s=100, marker= 'o', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='grey', s=100, marker= 'x', alpha=1.0, edgecolors='none')
    legend_list = ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage","50\% booster : 50\% new primary doses division","80\% booster : 20\% new primary doses division"]

    for population_type in ["older"]:
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

                
                if total_vaccination_rate == 0.2:
                    colour = 'lightskyblue'
                elif total_vaccination_rate == 0.5:
                    colour = 'dodgerblue'
                elif total_vaccination_rate == 0.8:
                    colour = 'navy'
                

                if booster_fraction == 0.5:
                    marker = "o"
                elif booster_fraction ==0.8:
                    marker = "x"


                # info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP

                info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                
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
                ax.scatter(percent_infected_before, percent_infected_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


    ax.set_xlim([19,81])
    ax.set_ylim([-1,51])

    x_ticks = [20,30,40,50,60,70,80]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    y_ticks = [0,10,20,30,40,50]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

    ax. set_aspect('equal')
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray', linestyle='dashed')
    ax.legend(legend_list)
    ax.set_ylabel('future attack rate (second wave)')
    ax.set_xlabel('past attack rate (first wave)')
    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_older_population.png") , bbox_inches='tight')
    # plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_older_population.pdf") , bbox_inches='tight')
    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_older_population.svg") , bbox_inches='tight')
    plt.close()

def plot_infection_population_breakdown():  
    for population_type in ["younger","older"]:
            
        for paramNum in population_list:
            for TP in TP_list:
                

                # colour = colour_list[colour_counter]

                # filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                # data_file = os.path.join(folder, filename)
                # pd_obj = pd.read_csv(data_file)
                # new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                # df = new_pd.pivot(index='day', columns='sim', values='n')

                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)


                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if booster_fraction ==0.5:
                    continue
                

                fig, ax = plt.subplots(1,1, figsize=(6,6.75))
                # info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate" +"\n"+ str(100*booster_fraction)+"\% booster fraction"
                info_text = population_type +" population with "+ str(100*total_vaccination_rate )+"\% vaccination coverage"
                
                sim_folder = "abm_continuous_simulation_parameters_" +population_type +"_" +str(paramNum)+"_SOCRATES_TP"+TP

                collected_simulated_population_by_age_band=[]

                collected_unvaxxed_uninfected_before_by_age_band=[]
                collected_unvaxxed_infected_before_by_age_band=[]
                collected_vaxxed_uninfected_before_by_age_band=[]
                collected_vaxxed_infected_before_by_age_band=[]

                collected_after_never_vaxxed_never_infected_by_age_band=[]
                collected_after_never_vaxxed_preinfection_no_postinfection_by_age_band=[]
                collected_after_never_vaxxed_no_preinfection_postinfection_by_age_band=[]
                collected_after_never_vaxxed_preinfection_postinfection_by_age_band=[]

                collected_prevaxxed_never_infected_by_age_band=[]
                collected_prevaxxed_preinfected_no_postinfection_by_age_band=[]
                collected_prevaxxed_no_preinfection_postinfection_by_age_band=[]
                collected_prevaxxed_preinfection_postinfection_by_age_band=[]

                collected_after_vaxxed_never_infected_by_age_band=[]
                collected_after_vaxxed_preinfected_no_postinfection_by_age_band=[]
                collected_after_vaxxed_no_preinfection_postinfection_by_age_band=[]
                collected_after_vaxxed_preinfection_postinfection_by_age_band=[]

                for sim_number in range(1,SIM_NUMBER+1):

                    filename_individuals = "sim_number_" + str(sim_number)+"_individuals.csv"

                    list_of_all_people = []
                    
                    individuals_file = os.path.join(folder,sim_folder,filename_individuals )
                    with open(individuals_file, newline='') as csvfile:
                        ind_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                        line_count = 0
                        
                        for row in ind_reader:
                            # print(line_count+1)
                            if line_count == 0:
                                # print(f'Column names are {", ".join(row)}')
                                line_count += 1
                            else:
                                # print(row)
                                age,age_bracket,dose_times,infection_times,symptom_onset_times = row 
                                new_row = [float(age),int(age_bracket),convert_to_array(dose_times),convert_to_array(infection_times),convert_to_array(symptom_onset_times)]
                                # if new_row[-1]!=[]:
                                #     print(new_row)
                                list_of_all_people.append(new_row)
                                line_count += 1


                    individuals_by_age_band = dict()
                    simulated_population_by_age_band=[0]*len(age_bands_abm)

                    unvaxxed_uninfected_before_by_age_band=[0]*len(age_bands_abm)
                    unvaxxed_infected_before_by_age_band=[0]*len(age_bands_abm)
                    vaxxed_uninfected_before_by_age_band=[0]*len(age_bands_abm)
                    vaxxed_infected_before_by_age_band=[0]*len(age_bands_abm)

                    after_never_vaxxed_never_infected_by_age_band=[0]*len(age_bands_abm)
                    after_never_vaxxed_preinfection_no_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_never_vaxxed_no_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_never_vaxxed_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)

                    prevaxxed_never_infected_by_age_band=[0]*len(age_bands_abm)
                    prevaxxed_preinfected_no_postinfection_by_age_band=[0]*len(age_bands_abm)
                    prevaxxed_no_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)
                    prevaxxed_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)

                    after_vaxxed_never_infected_by_age_band=[0]*len(age_bands_abm)
                    after_vaxxed_preinfected_no_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_vaxxed_no_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_vaxxed_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)

                    num_unvaxxed_people = 0
                    num_people = 0
                    for person in list_of_all_people:
                        age,age_band,dose_times,infection_times,symptom_onset_times = person
                        simulated_population_by_age_band[age_band]= simulated_population_by_age_band[age_band]+1

                        # first, during the prewinter stage: (pre-time split stage)
                        vaxxed = False
                        infected = False
                        if dose_times!= [] and dose_times[1]<time_split:
                            # if they do get vaccinated, then must have at least two doses; if the second dose is before the time split at 400, then they're in the "prewinter" vaxxed group
                            vaxxed = True
                        
                        if symptom_onset_times!=[] and symptom_onset_times[0]< time_split:
                            # then in the infected before [winter] group
                            infected = True
                        
                        if vaxxed and infected:
                            vaxxed_infected_before_by_age_band[age_band]+=1
                        elif vaxxed and (not infected):
                            vaxxed_uninfected_before_by_age_band[age_band]+=1
                        elif (not vaxxed) and infected:
                            unvaxxed_infected_before_by_age_band[age_band]+=1
                        else:
                            unvaxxed_uninfected_before_by_age_band[age_band]+=1

                        # second, the winter stage (post-time split stage)

                        vaxxed_after = False
                        infected_after = False 

                        if dose_times!= [] and dose_times[1]>time_split:
                            # if they do get vaccinated, then must have at least two doses; if the second dose is after the time split at 400, then they're in the "winter" vaxxed group
                            vaxxed_after = True
                        
                        if symptom_onset_times!=[] and symptom_onset_times[-1] > time_split:
                            # then was infected after the time split
                            # technically could have had multiple infections... 
                            infected_after = True

                        if (not vaxxed) and (not vaxxed_after):
                            num_unvaxxed_people+=1
                            if (not infected) and (not infected_after):
                                after_never_vaxxed_never_infected_by_age_band[age_band]+=1
                                num_people+=1
                            elif infected and (not infected_after):
                                after_never_vaxxed_preinfection_no_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            elif (not infected) and infected_after:
                                after_never_vaxxed_no_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            else:
                                after_never_vaxxed_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                        elif vaxxed and (not vaxxed_after):
                            # if vaxxed during the pre-winter stage, did it help them or not?
                            if  (not infected) and (not infected_after):
                                prevaxxed_never_infected_by_age_band[age_band]+=1
                                num_people+=1
                            elif infected and (not infected_after):
                                prevaxxed_preinfected_no_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            elif (not infected) and infected_after:
                                prevaxxed_no_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            else:
                                prevaxxed_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                        elif vaxxed_after and (not vaxxed):
                            if (not infected) and (not infected_after):
                                after_vaxxed_never_infected_by_age_band[age_band]+=1
                                num_people+=1
                            elif infected and (not infected_after):
                                after_vaxxed_preinfected_no_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            elif (not infected) and infected_after:
                                after_vaxxed_no_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            else:
                                after_vaxxed_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                        else:
                            print("there shouldn't be a double course of vaccinations!")
                            exit(1)
                        
                    
                    collected_simulated_population_by_age_band.append(simulated_population_by_age_band)

                    collected_unvaxxed_uninfected_before_by_age_band.append(unvaxxed_uninfected_before_by_age_band)
                    collected_unvaxxed_infected_before_by_age_band.append(unvaxxed_infected_before_by_age_band)
                    collected_vaxxed_uninfected_before_by_age_band.append(vaxxed_uninfected_before_by_age_band)
                    collected_vaxxed_infected_before_by_age_band.append(vaxxed_infected_before_by_age_band)

                    
                    

                    collected_after_never_vaxxed_never_infected_by_age_band.append(after_never_vaxxed_never_infected_by_age_band)
                    collected_after_never_vaxxed_preinfection_no_postinfection_by_age_band.append(after_never_vaxxed_preinfection_no_postinfection_by_age_band)
                    collected_after_never_vaxxed_no_preinfection_postinfection_by_age_band.append(after_never_vaxxed_no_preinfection_postinfection_by_age_band)
                    collected_after_never_vaxxed_preinfection_postinfection_by_age_band.append(after_never_vaxxed_preinfection_postinfection_by_age_band)

                    collected_prevaxxed_never_infected_by_age_band.append(prevaxxed_never_infected_by_age_band)
                    collected_prevaxxed_preinfected_no_postinfection_by_age_band.append(prevaxxed_preinfected_no_postinfection_by_age_band)
                    collected_prevaxxed_no_preinfection_postinfection_by_age_band.append(prevaxxed_no_preinfection_postinfection_by_age_band)
                    collected_prevaxxed_preinfection_postinfection_by_age_band.append(prevaxxed_preinfection_postinfection_by_age_band)

                    collected_after_vaxxed_never_infected_by_age_band.append(after_vaxxed_never_infected_by_age_band)
                    collected_after_vaxxed_preinfected_no_postinfection_by_age_band.append(after_vaxxed_preinfected_no_postinfection_by_age_band)
                    collected_after_vaxxed_no_preinfection_postinfection_by_age_band.append(after_vaxxed_no_preinfection_postinfection_by_age_band)
                    collected_after_vaxxed_preinfection_postinfection_by_age_band.append(after_vaxxed_preinfection_postinfection_by_age_band)

                    # print(sum(simulated_population_by_age_band))
                    # print(num_people)

                
                ####### MEDIAN #############################################################################################################
                
                median_simulated_population_by_age_band = np.median(np.array(collected_simulated_population_by_age_band), axis=0)
                median_unvaxxed_uninfected_before_by_age_band = np.median(np.array(collected_unvaxxed_uninfected_before_by_age_band), axis=0)
                median_unvaxxed_infected_before_by_age_band = np.median(np.array(collected_unvaxxed_infected_before_by_age_band), axis=0)
                median_vaxxed_uninfected_before_by_age_band = np.median(np.array(collected_vaxxed_uninfected_before_by_age_band), axis=0)
                median_vaxxed_infected_before_by_age_band = np.median(np.array(collected_vaxxed_infected_before_by_age_band), axis=0)

                median_preinfection = sum(median_unvaxxed_infected_before_by_age_band) + sum(median_vaxxed_infected_before_by_age_band)

                median_after_never_vaxxed_never_infected_by_age_band = np.median(np.array(collected_after_never_vaxxed_never_infected_by_age_band), axis=0)
                median_after_never_vaxxed_preinfection_no_postinfection_by_age_band = np.median(np.array(collected_after_never_vaxxed_preinfection_no_postinfection_by_age_band), axis=0)
                median_after_never_vaxxed_no_preinfection_postinfection_by_age_band = np.median(np.array(collected_after_never_vaxxed_no_preinfection_postinfection_by_age_band), axis=0)
                median_after_never_vaxxed_preinfection_postinfection_by_age_band = np.median(np.array(collected_after_never_vaxxed_preinfection_postinfection_by_age_band), axis=0)

                median_prevaxxed_never_infected_by_age_band = np.median(np.array(collected_prevaxxed_never_infected_by_age_band), axis=0)
                median_prevaxxed_preinfected_no_postinfection_by_age_band = np.median(np.array(collected_prevaxxed_preinfected_no_postinfection_by_age_band), axis=0)
                median_prevaxxed_no_preinfection_postinfection_by_age_band = np.median(np.array(collected_prevaxxed_no_preinfection_postinfection_by_age_band), axis=0)
                median_prevaxxed_preinfection_postinfection_by_age_band = np.median(np.array(collected_prevaxxed_preinfection_postinfection_by_age_band), axis=0)

                median_after_vaxxed_never_infected_by_age_band = np.median(np.array(collected_after_vaxxed_never_infected_by_age_band), axis=0)
                median_after_vaxxed_preinfected_no_postinfection_by_age_band = np.median(np.array(collected_after_vaxxed_preinfected_no_postinfection_by_age_band), axis=0)
                median_after_vaxxed_no_preinfection_postinfection_by_age_band = np.median(np.array(collected_after_vaxxed_no_preinfection_postinfection_by_age_band), axis=0)
                median_after_vaxxed_preinfection_postinfection_by_age_band = np.median(np.array(collected_after_vaxxed_preinfection_postinfection_by_age_band), axis=0)

                #####################################################
                # infections over ages and vaccine -- percentage: prewinter; median

                
                fig, ax = plt.subplots(1,1, figsize=(6,6.75))

                y_pos = np.arange(len(age_bands_abm))

                df_median_novaccine_list = [x/y*100 for x,y in zip(median_unvaxxed_infected_before_by_age_band,median_simulated_population_by_age_band)]
                uninfected_unvaxxed_list = [x/y*100 for x,y in zip(median_unvaxxed_uninfected_before_by_age_band,median_simulated_population_by_age_band)]
                df_median_doseany_list = [x/y*100 for x,y in zip(median_vaxxed_infected_before_by_age_band,median_simulated_population_by_age_band)]
                uninfected_vaccinated_list = [x/y*100 for x,y in zip(median_vaxxed_uninfected_before_by_age_band,median_simulated_population_by_age_band)]
                ax.barh(y_pos,df_median_novaccine_list,color="firebrick")
                ax.barh(y_pos,uninfected_unvaxxed_list,left=df_median_novaccine_list,color="pink")

                ax.barh(y_pos, df_median_doseany_list, left=[x+y for x,y in zip(uninfected_unvaxxed_list,df_median_novaccine_list)],color="midnightblue")
                ax.barh(y_pos,uninfected_vaccinated_list,left=[x+y+z for x,y,z in zip(df_median_doseany_list,df_median_novaccine_list,uninfected_unvaxxed_list)] ,color="lightskyblue")
                


                ax.set_yticks(y_pos)
                ax.set_yticklabels(age_bands_abm)
                # ax.invert_yaxis()  # labels read top-to-bottom
                ax.set_xlabel('Proportion \%')
                ax.set_title('(Median Infected) Population Breakdown: Past ['+str(round(median_preinfection/100000*100,1))+'\% past attack rate]')
                # ax.set_xlim([0,15500])
                x_pos = list(range(0,101,10))
                ax.set_xticks(x_pos)
                ax.set_xticklabels([str(x)+"\%" for x in x_pos])

                ax.legend(["Unvaccinated \& Infected", "Unvaccinated \& Uninfected", "Vaccinated \& Infected","Vaccinated \& Uninfected"],title=info_text,bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)

                plt.savefig(os.path.join(folder,sim_folder+"_infections_by_age_brackets_vax_median_STACKED_proportion_prewinter.png") , bbox_inches='tight')
                plt.close()

                #####################################################
                # infections over ages and vaccine -- percentage: winter; median

                
                fig, ax = plt.subplots(1,1, figsize=(6,6.75))

                y_pos = np.arange(len(age_bands_abm))

                df_median_novaccine_list = [x/y*100 for x,y in zip(median_unvaxxed_infected_before_by_age_band,median_simulated_population_by_age_band)]
                uninfected_unvaxxed_list = [x/y*100 for x,y in zip(median_unvaxxed_uninfected_before_by_age_band,median_simulated_population_by_age_band)]
                df_median_doseany_list = [x/y*100 for x,y in zip(median_vaxxed_infected_before_by_age_band,median_simulated_population_by_age_band)]
                uninfected_vaccinated_list = [x/y*100 for x,y in zip(median_vaxxed_uninfected_before_by_age_band,median_simulated_population_by_age_band)]
                
                list_2 = [median_after_never_vaxxed_never_infected_by_age_band,median_after_never_vaxxed_preinfection_no_postinfection_by_age_band,median_after_never_vaxxed_no_preinfection_postinfection_by_age_band,median_after_never_vaxxed_preinfection_postinfection_by_age_band,median_prevaxxed_never_infected_by_age_band,median_prevaxxed_preinfected_no_postinfection_by_age_band,median_prevaxxed_no_preinfection_postinfection_by_age_band,median_prevaxxed_preinfection_postinfection_by_age_band,median_after_vaxxed_never_infected_by_age_band,median_after_vaxxed_preinfected_no_postinfection_by_age_band,median_after_vaxxed_no_preinfection_postinfection_by_age_band,median_after_vaxxed_preinfection_postinfection_by_age_band ]
                median_pop = [0]*len(age_bands_abm)
                for i in range(len(list_2)):
                    median_pop = [x+y for x,y in zip(median_pop,list_2[i])]
                print(sum(median_pop))

                # not-vaxed, not-vaxed[winter], not-infected, not infected[winter]
                nvnv_nini = [x/y*100 for x,y in zip(median_after_never_vaxxed_never_infected_by_age_band,median_pop)]
                # not-vaxed, not-vaxed, yes-infected, not-infected
                nvnv_yini = [x/y*100 for x,y in zip(median_after_never_vaxxed_preinfection_no_postinfection_by_age_band,median_pop)]
                nvnv_niyi = [x/y*100 for x,y in zip(median_after_never_vaxxed_no_preinfection_postinfection_by_age_band,median_pop)]
                nvnv_yiyi =  [x/y*100 for x,y in zip(median_after_never_vaxxed_preinfection_postinfection_by_age_band,median_pop)]
                
                yvnv_nini= [x/y*100 for x,y in zip(median_prevaxxed_never_infected_by_age_band,median_pop)]
                yvnv_yini= [x/y*100 for x,y in zip(median_prevaxxed_preinfected_no_postinfection_by_age_band,median_pop)]
                yvnv_niyi= [x/y*100 for x,y in zip(median_prevaxxed_no_preinfection_postinfection_by_age_band,median_pop)]
                yvnv_yiyi= [x/y*100 for x,y in zip(median_prevaxxed_preinfection_postinfection_by_age_band,median_pop)]

                nvyv_nini= [x/y*100 for x,y in zip(median_after_vaxxed_never_infected_by_age_band,median_pop)]
                nvyv_yini= [x/y*100 for x,y in zip(median_after_vaxxed_preinfected_no_postinfection_by_age_band ,median_pop)]
                nvyv_niyi= [x/y*100 for x,y in zip(median_after_vaxxed_no_preinfection_postinfection_by_age_band ,median_pop)]
                nvyv_yiyi= [x/y*100 for x,y in zip(median_after_vaxxed_preinfection_postinfection_by_age_band,median_pop)]
                
                lists_of_values_order = [nvnv_yiyi,nvnv_niyi,nvnv_yini,nvnv_nini,nvyv_yiyi,nvyv_niyi,nvyv_yini,nvyv_nini,yvnv_yiyi,yvnv_niyi,yvnv_yini,yvnv_nini]
                colours = ["darkred","firebrick","crimson","pink",
                            "darkgreen","green","mediumseagreen","palegreen", #"indigo","purple","darkviolet","plum",
                            "midnightblue","blue","royalblue","lightskyblue"]
                left_list = [0]*len(nvnv_yiyi)
                for i in range(len(lists_of_values_order)):
                    ax.barh(y_pos,lists_of_values_order[i],left=left_list,color=colours[i])
                    left_list = [x+y for x,y in zip(left_list,lists_of_values_order[i])]
                print(left_list)
                

                ax.set_yticks(y_pos)
                ax.set_yticklabels(age_bands_abm)
                # ax.invert_yaxis()  # labels read top-to-bottom
                ax.set_xlabel('Proportion \%')
                ax.set_title('Median infected population by vaccination status')
                # ax.set_xlim([0,15500])
                x_pos = list(range(0,101,10))
                ax.set_xticks(x_pos)
                ax.set_xticklabels([str(x)+"\%" for x in x_pos])
                ax.set_ylim([-0.5,16.5])

                ax.legend([
                    "Unvaccinated \& Infected Before + After", "Unvaccinated \& Infected After", "Unvaccinated \& Infected Before", "Unvaccinated \& Never Infected",
                    "Vaccinated After \& Infected Before + After","Vaccinated After \& Infected  After", "Vaccinated After \& Infected Before", "Vaccinated After \& Never Infected",
                    "Vaccinated Before \& Infected Before + After","Vaccinated Before \& Infected After","Vaccinated Before \& Infected Before","Vaccinated Before \& Never Infected"],title=info_text,bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)

                plt.savefig(os.path.join(folder, sim_folder+"_infections_by_age_brackets_vax_median_STACKED_proportion_winter.png") , bbox_inches='tight')
                plt.close()
                

def plot_ICU_and_deaths_vs_before_infections(ICU_or_death):
    for population_type in ["younger","older"]:
        fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        # first, some plotting to get some fake legends...
        ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='navy', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='grey', s=100, marker= 'o', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='grey', s=100, marker= 'x', alpha=1.0, edgecolors='none')
        legend_list = ["20\% vaccination", "50\% vaccination","80\% vaccination","50\% booster-new primary division","80\% booster-new primary division"]

        max_y= 0

        for paramNum in population_list:
            for TP in TP_list:

                # colour = colour_list[colour_counter]

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if total_vaccination_rate == 0.2:
                    colour = 'lightskyblue'
                elif total_vaccination_rate == 0.5:
                    colour = 'dodgerblue'
                elif total_vaccination_rate == 0.8:
                    colour = 'navy'
                
                if booster_fraction == 0.5:
                    marker = "o"
                elif booster_fraction ==0.8:
                    marker = "x"


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

                daily_deaths_after = []
                daily_ICU_admissions_after = []

                clinical_filename = "_full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
                clinical_pd_obj = pd.read_csv(clinical_file)

                # for col in clinical_pd_obj.columns:
                    # print(col)
                    # age
                    # iteration (aka "sims?")
                    # day
                    # daily_total_infections
                    # daily_symptomatic_infections
                    # daily_admissions
                    # ward_occupancy
                    # daily_ICU_admissions
                    # ICU_occupancy
                    # daily_deaths
                
                # new_pd_ICU = clinical_pd_obj.groupby('iteration').sum()
                # print(new_pd_ICU)
                # print(new_pd_ICU['daily_admissions'].to_list())

                scale = 50
                aug_num = 5
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']>=simnum*aug_num) & (clinical_pd_obj['iteration']<(simnum+1)*aug_num)& (clinical_pd_obj['day']>time_split)]

                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())/aug_num
                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())/aug_num

                    daily_deaths_after.append(daily_deaths)
                    daily_ICU_admissions_after.append(daily_ICU_admissions)
                
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                percent_daily_deaths_after = [x/total_population*100 for x in daily_deaths_after]
                percent_daily_ICU_admissions_after = [x/total_population*100 for x in daily_ICU_admissions_after]
                
                if ICU_or_death == 'death':
                    ax.scatter(percent_infected_before, daily_deaths_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max( daily_deaths_after))
                elif ICU_or_death =='ICU':
                    ax.scatter(percent_infected_before, daily_ICU_admissions_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max(daily_ICU_admissions_after))


        ax.set_xlim([0,100])
        ax.set_ylim([0,max_y+10])

        
        ax.grid(True)
        ax.legend(legend_list)
        ax.set_xlabel('\% of infected people before t = ' + str(time_split)+'("past infection")')

        if ICU_or_death == 'death':
            ax.set_ylabel('number of deaths after t = ' + str(time_split))
            ax.set_title('Deaths given past immunity \nfor a ' + population_type + ' population',fontsize=14)

            plt.savefig(os.path.join(folder, filename+"_deaths_vs_past_immunity_" +population_type +".png") , bbox_inches='tight')
            plt.close()
        elif ICU_or_death =='ICU':
            ax.set_ylabel('number of ICU admissions after t= ' + str(time_split))
            ax.set_title('ICU admissions given past immunity \nfor a ' + population_type + ' population',fontsize=14)

            plt.savefig(os.path.join(folder, filename+"_ICU_admissions_vs_past_immunity_" +population_type +".png") , bbox_inches='tight')
            plt.close()
    return   

def plot_ICU_and_deaths_vs_before_infections_combined(ICU_or_death,OG=""): # or "OG_"
    fig, ax = plt.subplots(1,1, figsize=(6,5))

    # first, some plotting to get some fake legends...
    ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='navy', s=100, marker= 's', alpha=1.0, edgecolors='none')

    ax.scatter(-10000,-10000,color='salmon', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='red', s=100, marker= 's', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 's', alpha=1.0, edgecolors='none')
    # ax.scatter(-10000,-10000,color='yellowgreen', s=100, marker= 's', alpha=1.0, edgecolors='none')
    # ax.scatter(-10000,-10000,color='limegreen', s=100, marker= 's', alpha=1.0, edgecolors='none')
    # ax.scatter(-10000,-10000,color='darkgreen', s=100, marker= 's', alpha=1.0, edgecolors='none')


    ax.scatter(-10000,-10000,color='grey', s=100, marker= 'o', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='grey', s=100, marker= 'x', alpha=1.0, edgecolors='none')
    legend_list = ["20\% vaccination in younger population", "50\% vaccination in younger population","80\% vaccination in younger population","20\% vaccination in older population", "50\% vaccination in older population","80\% vaccination in older population","50\% booster vs new primary doses division","80\% booster vs new primary doses division"]
    max_y= 0

    for population_type in ["younger","older"]:
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
                    # if total_vaccination_rate == 0.2:
                    #     colour = 'yellowgreen'
                    # elif total_vaccination_rate == 0.5:
                    #     colour = 'limegreen'
                    # elif total_vaccination_rate == 0.8:
                    #     colour = 'darkgreen'
                    if total_vaccination_rate == 0.2:
                        colour = 'salmon'
                    elif total_vaccination_rate == 0.5:
                        colour = 'red'
                    elif total_vaccination_rate == 0.8:
                        colour = 'firebrick'
                
                if booster_fraction == 0.5:
                    marker = "o"
                elif booster_fraction ==0.8:
                    marker = "x"


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

                daily_deaths_after = []
                daily_ICU_admissions_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
                clinical_pd_obj = pd.read_csv(clinical_file)

                scale = 40
                aug_num = 5
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']>=simnum*aug_num) & (clinical_pd_obj['iteration']<(simnum+1)*aug_num)& (clinical_pd_obj['day']>time_split)]

                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())/aug_num
                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())/aug_num

                    daily_deaths_after.append(daily_deaths)
                    daily_ICU_admissions_after.append(daily_ICU_admissions)
                
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                percent_daily_deaths_after = [x/total_population*100 for x in daily_deaths_after]
                percent_daily_ICU_admissions_after = [x/total_population*100 for x in daily_ICU_admissions_after]
                
                if ICU_or_death == 'death':
                    ax.scatter(percent_infected_before, daily_deaths_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max( daily_deaths_after))
                elif ICU_or_death =='ICU':
                    ax.scatter(percent_infected_before, daily_ICU_admissions_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max(daily_ICU_admissions_after))


    ax.set_xlim([0,85])
    ax.set_ylim([0,max_y+10])

    
    # ax.grid(True)
    ax.legend(legend_list)
    ax.set_xlabel('past attack rate')
    ax.grid(True, which='major',color='gray', linestyle='dashed')
    ax.set_axisbelow(True)

    if ICU_or_death == 'death':
        ax.set_ylabel('future deaths (number of deaths after t = ' + str(time_split) +")")
        ax.set_title('Deaths given past immunity',fontsize=14)

        plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_deaths_vs_past_immunity"+OG+".png") , bbox_inches='tight')
        plt.close()
    elif ICU_or_death =='ICU':
        ax.set_ylabel('future ICU admissions (number of ICU admissions after t= ' + str(time_split) +")")
        ax.set_title('ICU admissions given past immunity',fontsize=14)

        plt.savefig(os.path.join(folder,"abm_continuous_simulation_parameters_ICU_admissions_vs_past_immunity"+OG+".png") , bbox_inches='tight')
        plt.close()
       


def plot_infection_numbers(total_sims=20):
    for population_type in ["younger","older"]:
            
        for paramNum in population_list:
            for TP in TP_list:
                fig, (ax1,ax2) = plt.subplots(2,1, figsize=(6,6.75))

                # colour = colour_list[colour_counter]

                # filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                # data_file = os.path.join(folder, filename)
                # pd_obj = pd.read_csv(data_file)
                # new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                # df = new_pd.pivot(index='day', columns='sim', values='n')

                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)


                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]
                info_text =  population_type +" population, "+ str(100*total_vaccination_rate )+"\% vax rate" +", "+ str(100*booster_fraction)+"\% booster fraction"
                
                sim_folder = "abm_continuous_simulation_parameters_" +population_type +"_" +str(paramNum)+"_SOCRATES_TP"+TP


                if population_type == "older":
                    ax1.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, total_sims))))
                    ax2.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, total_sims))))
                else:
                    ax1.set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 0.5,total_sims))))
                    ax2.set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 0.5,total_sims))))
                

                for sim_number in range(1,total_sims+1):
                    infection_number = list(range(1,11))
                    infections_total = [0]*10 # assuming 10 maximum infections, going from infection = index+1
                    infections_after = [0]*10

                    filename_individuals = "sim_number_" + str(sim_number)+"_individuals.csv"

                    
                    
                    individuals_file = os.path.join(folder,sim_folder,filename_individuals )
                    with open(individuals_file, newline='') as csvfile:
                        ind_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                        line_count = 0
                        
                        for row in ind_reader:
                            # print(line_count+1)
                            if line_count == 0:
                                # print(f'Column names are {", ".join(row)}')
                                line_count += 1
                            else:
                                # print(row)
                                age,age_bracket,dose_times,infection_times,symptom_onset_times = row
                                symptom_onset_times = convert_to_array(symptom_onset_times)

                                if symptom_onset_times!=[]:
                                    num_infections_pre_split = 0
                                    num_infections_post_split = 0
                                    for time in symptom_onset_times:
                                        if time<time_split:
                                            num_infections_pre_split +=1
                                        else:
                                            num_infections_post_split+=1
                                    num_infections_total = num_infections_pre_split + num_infections_post_split
                                    if num_infections_total!= len(symptom_onset_times):
                                        print("error in total number of infections per person!")
                                        exit(1)
                                    if num_infections_total>0:
                                        infections_total[num_infections_total-1]+=1
                                    if num_infections_post_split >0:
                                        infections_after[num_infections_post_split-1] +=1
                    ax1.plot(infection_number,infections_total)
                    ax2.plot(infection_number,infections_after)

                ax1.set_xticks(infection_number)
                ax2.set_xticks(infection_number)
                ax1.set_xlabel('Infection numbers')
                ax2.set_xlabel('Infection numbers')
                ax1.set_ylabel('Number of people infected x times')
                ax2.set_ylabel('Number of people infected x times')

                ax1.set_title('Number of people infected multiple times (total) for \n a '+info_text )
                ax2.set_title('Number of people infected multiple times (after t = '+str(time_split)+')')
                # ax.set_xlim([0,15500])
                
                plt.tight_layout()
                ax1.grid()
                ax2.grid()

                plt.savefig(os.path.join(folder,sim_folder+"_multiple_infections.png") , bbox_inches='tight')
                plt.close()




def plot_infection_numbers_combined(total_sims=20):
    for population_type in ["younger","older"]:
        fig, (ax1,ax2) = plt.subplots(2,1, figsize=(6,6.75))
        for paramNum in population_list:
            for TP in TP_list:
                
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)


                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]
                info_text =  population_type +" population, "+ str(100*total_vaccination_rate )+"\% vax rate" +", "+ str(100*booster_fraction)+"\% booster fraction"
                
                sim_folder = "abm_continuous_simulation_parameters_" +population_type +"_" +str(paramNum)+"_SOCRATES_TP"+TP


                # if population_type == "older":
                #     ax1.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, total_sims))))
                #     ax2.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, total_sims))))
                # else:
                #     ax1.set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 0.5,total_sims))))
                #     ax2.set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 0.5,total_sims))))
                

                for sim_number in range(1,total_sims+1):
                    infection_number = list(range(1,11))
                    infections_total = [0]*10 # assuming 10 maximum infections, going from infection = index+1
                    infections_after = [0]*10

                    filename_individuals = "sim_number_" + str(sim_number)+"_individuals.csv"

                    
                    
                    individuals_file = os.path.join(folder,sim_folder,filename_individuals )
                    with open(individuals_file, newline='') as csvfile:
                        ind_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                        line_count = 0
                        
                        for row in ind_reader:
                            # print(line_count+1)
                            if line_count == 0:
                                # print(f'Column names are {", ".join(row)}')
                                line_count += 1
                            else:
                                # print(row)
                                age,age_bracket,dose_times,infection_times,symptom_onset_times = row
                                symptom_onset_times = convert_to_array(symptom_onset_times)

                                if symptom_onset_times!=[]:
                                    num_infections_pre_split = 0
                                    num_infections_post_split = 0
                                    for time in symptom_onset_times:
                                        if time<time_split:
                                            num_infections_pre_split +=1
                                        else:
                                            num_infections_post_split+=1
                                    num_infections_total = num_infections_pre_split + num_infections_post_split
                                    if num_infections_total!= len(symptom_onset_times):
                                        print("error in total number of infections per person!")
                                        exit(1)
                                    if num_infections_total>0:
                                        infections_total[num_infections_total-1]+=1
                                    if num_infections_post_split >0:
                                        infections_after[num_infections_post_split-1] +=1
                    ax1.plot(infection_number,infections_total,alpha=0.025,color="black")
                    ax2.plot(infection_number,infections_after,alpha=0.025,color="black")

        ax1.set_xticks(infection_number)
        ax2.set_xticks(infection_number)
        ax1.set_xlabel('Infection numbers')
        ax2.set_xlabel('Infection numbers')
        ax1.set_ylabel('Number of people infected x times')
        ax2.set_ylabel('Number of people infected x times')

        ax1.set_title('Number of people infected multiple times (total)' )
        ax2.set_title('Number of people infected multiple times (after t = '+str(time_split)+')')
        # ax.set_xlim([0,15500])
        
        plt.tight_layout()
        ax1.grid()
        ax2.grid()

        plt.savefig(os.path.join(folder,"abm_continuous_simulation_parameters_" +population_type +"_multiple_infections.png") , bbox_inches='tight')
        plt.close()

def plot_peak_height():
    for population_type in ["younger","older"]:
        fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        # first, some plotting to get some fake legends...
        ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='navy', s=100, marker= 's', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='grey', s=100, marker= 'o', alpha=1.0, edgecolors='none')
        ax.scatter(-10000,-10000,color='grey', s=100, marker= 'x', alpha=1.0, edgecolors='none')
        legend_list = ["20\% vaccination", "50\% vaccination","80\% vaccination","50\% booster-new primary division","80\% booster-new primary division"]


        for paramNum in population_list:
            for TP in TP_list:

                # colour = colour_list[colour_counter]

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if total_vaccination_rate == 0.2:
                    colour = 'lightskyblue'
                elif total_vaccination_rate == 0.5:
                    colour = 'dodgerblue'
                elif total_vaccination_rate == 0.8:
                    colour = 'navy'
                
                if booster_fraction == 0.5:
                    marker = "o"
                elif booster_fraction ==0.8:
                    marker = "x"


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

                scale = 50
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    peak_infections_before = max(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(peak_infections_before)

                    peak_infections_after = max(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(peak_infections_after)
                
                # percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                # percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]
                ax.scatter(infections_per_sim_before, infections_per_sim_after , color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


        ax.set_xlim([0,max(infections_per_sim_before)])
        ax.set_ylim([0,max(infections_per_sim_after)])

        
        ax.grid(True)
        ax.legend(legend_list)
        ax.set_ylabel('Number of infected people at peak after t = ' + str(time_split))
        ax.set_xlabel('Number of infected people at peak before t = '+str(time_split)+' ("past infection")')
        ax.set_title('Number of infected people at wave peaks given past immunity \nfor a ' + population_type + ' population',fontsize=14)

        plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_peak_infections_past_immunity_" +population_type +".png") , bbox_inches='tight')
        plt.close()
        
def plot_before_and_after_infections_older_80_booster_only():
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    # first, some plotting to get some fake legends...
    ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none')
    ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none')

    # ax.scatter(-10000,-10000,color='grey', s=100, marker= 'o', alpha=1.0, edgecolors='none')
    # ax.scatter(-10000,-10000,color='grey', s=100, marker= 'x', alpha=1.0, edgecolors='none')
    legend_list = ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"]#,"50\% booster : 50\% new primary doses division","80\% booster : 20\% new primary doses division"]

    for population_type in ["older"]:
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

                
                if total_vaccination_rate == 0.2:
                    colour = 'lightskyblue'
                elif total_vaccination_rate == 0.5:
                    colour = 'dodgerblue'
                elif total_vaccination_rate == 0.8:
                    colour = 'navy'
                

                if booster_fraction == 0.5:
                    marker = "o"
                    continue
                elif booster_fraction ==0.8:
                    #marker = "x"
                    marker = "o"


                # info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP

                info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                
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
                ax.scatter(percent_infected_before, percent_infected_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


    ax.set_xlim([19,81])
    ax.set_ylim([-1,51])

    x_ticks = [20,30,40,50,60,70,80]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    y_ticks = [0,10,20,30,40,50]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

    ax. set_aspect('equal')
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray', linestyle='dashed')
    ax.legend(legend_list)
    ax.set_ylabel('future attack rate (from t = 450 to 650)')
    ax.set_xlabel('past attack rate (before t = 450)')
    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_older_population_80_booster.png") , bbox_inches='tight')
    # plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_older_population.pdf") , bbox_inches='tight')
    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_older_population_80_booster.svg") , bbox_inches='tight')
    plt.close()



def plot_before_vs_after_infections_combined_ages_80_booster_only(population_type_list = ["younger","older"]):
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    # first, some plotting to get some fake legends...
    legend_points = []

    # legend_list = ["20\% vaccination coverage, younger population", "50\% vaccination coverage, younger population","80\% vaccination coverage, younger population","20\% vaccination coverage, older population", "50\% vaccination coverage, older population","80\% vaccination coverage, older population"]

    for population_type in population_type_list:
        if population_type == "younger":
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))


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
                ax.scatter(percent_infected_after, percent_infected_before, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


    
    ax.set_ylim([15,85])
    ax.set_xlim([-1,60])

    x_ticks = [0,10,20,30,40,50,60]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    y_ticks = [20,30,40,50,60,70,80]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

    ax.set_aspect('equal')
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray')
    # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

    if len(population_type_list)==2:
        ax.legend(legend_points[:3], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(1, 1), loc=1)
        leg = Legend(ax,legend_points[3:], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(1, 0.8), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points, ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0]+" population",bbox_to_anchor=(1, 1), loc=1)



    ax.set_xlabel('near-future attack rate (t = 450 to 650)')
    ax.set_title('near-future attack rate (t = 450 to 650)')
    ax.set_ylabel('past attack rate (before t = 450)')
    ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    ax.invert_yaxis()

    

    yticks = [15,20,30,40,50,60,70,80,85]
    for y0, y1 in zip(yticks[::2], yticks[1::2]):
        plt.axhspan(y0, y1, color='black', alpha=0.1, zorder=0)

    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]     

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population_80booster_only_"+ addition+ ".png") , bbox_inches='tight') 
    # plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population.pdf") , bbox_inches='tight')
    # plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population.svg") , bbox_inches='tight')
    plt.close()
        




def plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger","older"]):
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))
    # first, some plotting to get some fake legends...
    legend_points = []

    # legend_list = ["20\% vaccination coverage, younger population", "50\% vaccination coverage, younger population","80\% vaccination coverage, younger population","20\% vaccination coverage, older population", "50\% vaccination coverage, older population","80\% vaccination coverage, older population"]

    for population_type in population_type_list :
        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

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
                ax.scatter( percent_infected_before, percent_infected_after,color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')


    
    ax.set_xlim([15,85])
    ax.set_ylim([-1,60])

    y_ticks = [0,10,20,30,40,50,60]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

    x_ticks = [20,30,40,50,60,70,80]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    ax.set_aspect('equal')
    # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='gray')
    # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)


    if len(population_type_list)==2:
        ax.legend(legend_points[:3], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.47, 1), loc=1)
        leg = Legend(ax,legend_points[3:], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.47, 0.75), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points, ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0] +" population",bbox_to_anchor=(0.47, 1), loc=1)

    ax.set_ylabel('near-future attack rate (t = 450 to 650)')
    #ax.set_title('past attack rate (before t = 450)')
    ax.set_xlabel('past attack rate (before t = 450)')
    #ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    

    xticks = [15,20,30,40,50,60,70,80,85]
    for x0, x1 in zip(xticks[::2], xticks[1::2]):
        plt.axvspan(x0, x1, color='black', alpha=0.1, zorder=0)

    # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]   

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population_80booster_only_horizontal_" + addition+ ".png") , bbox_inches='tight') 
    # plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population.pdf") , bbox_inches='tight')
    # plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population.svg") , bbox_inches='tight')
    plt.close()
        

def plot_before_vs_after_infections_combined_ages_80_booster_only_boxplot(population_type_list = ["younger","older"],bucket_list ={20:[0,20],40:[20,40],60:[40,60],80:[60,80],100:[80,100]}):
    fig, ax = plt.subplots(1,1, figsize=(7,7))
    # first, some plotting to get some fake legends...
    legend_points = []

    marker = "s"

    box_counter = 0

    # starting_positions = [0,6,12,18,24]
    starting_positions = []
    for i in range(len(bucket_list)):
        position =i*3*len(population_type_list)
        starting_positions.append(position)

    for population_type in population_type_list:
        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            
            
        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            
            

        for paramNum in reversed(population_list):
            # buckets for past ;
            # less than 15%, less than 25% etc.
            
            
            future_attack_rate_given_past_buckets = dict()
            for bucket,bucketrange in bucket_list.items():
                future_attack_rate_given_past_buckets [bucket] = []

            colour = "lightskyblue"

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

                    percent_infected_before = total_infections_before/total_population*100
                    percent_infected_after = total_infections_after/total_population*100

                    
                    for bucket,bucketrange in bucket_list.items():
                        if percent_infected_before>=bucketrange[0] and percent_infected_before < bucketrange[1]:
                            future_attack_rate_given_past_buckets[bucket].append(percent_infected_after)
                            break
            
            if booster_fraction == 0.8:
                total_summed_infections = [future_attack_rate_given_past_buckets[x] for x in bucket_list]

                positions = [x+box_counter for x in starting_positions ]
                print(positions)

                if population_type=='younger':
                    median_colour = "cyan"
                else:
                    median_colour = "cyan"

                boxes= ax.boxplot(total_summed_infections, vert=False, patch_artist=True,positions=positions,medianprops=dict(color=median_colour),boxprops=dict(facecolor=colour, color=colour),capprops=dict(color=colour),whiskerprops=dict(color=colour),flierprops=dict(color=colour, markeredgecolor=colour))

                for patch in boxes['boxes']:
                    patch.set_facecolor(colour)


                box_counter+=1
    
    #bucket_list ={20:[0,20],40:[20,40],60:[40,60],80:[60,80],100:[80,100]}
    ax.set_yticks( [x+(starting_positions[1]-starting_positions [0]-1)/2 for x in starting_positions ])
    ax.set_yticklabels([str(bucketrange[0]) + "\% - " + str(bucketrange[1]) +"\%\npast attack rate" for bucket,bucketrange in bucket_list.items()])
    # ax.invert_yaxis()  # labels read top-to-bottom # doesn't work

    ax.set_xlim([-5,85])
    ax.set_ylim([-1,max(positions)+1])

    x_ticks = [0,10,20,30,40,50,60,70]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    # ax.set_aspect('equal')
    # # ax.grid(True)
    ax.set_axisbelow(True)
    ax.grid(color='lightgray',axis='x')
    # # ax.legend(legend_list,bbox_to_anchor=(1, 1), loc=1)

    if len(population_type_list)==2:
        ax.legend(legend_points[:3], ["20\% vaccination coverage","50\% vaccination coverage","80\% vaccination coverage"],title="older population",bbox_to_anchor=(1, 0.2), loc=1)
        leg = Legend(ax,legend_points[3:],["20\% vaccination coverage","50\% vaccination coverage","80\% vaccination coverage"], title="younger population",bbox_to_anchor=(1, 0.4), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points[:3], ["20\% vaccination coverage","50\% vaccination coverage","80\% vaccination coverage"],title= population_type_list[0] +" population",bbox_to_anchor=(1, 0.2), loc=1)


    ax.set_xlabel('near-future attack rate (t = 450 to 650)')
    # #ax.set_title('past attack rate (before t = 450)')
    ax.set_ylabel('past attack rate (before t = 450)')
    # #ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    

    yticks =[x-0.5 for x in starting_positions ]
    yticks.append(starting_positions[-1]+5.5)
    for y0, y1 in zip(yticks[::2], yticks[1::2]):
        plt.axhspan(y0, y1, color='black', alpha=0.1, zorder=0)

    # # ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]   

    num_buckets = len(bucket_list)
    for bucket,bucketrange in bucket_list.items():
        bucket_range = bucketrange[1]-bucketrange[0]
        break

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_infections_past_immunity_combined_population_80booster_only_boxplot_buckets_"+str(num_buckets)+"-"+str(bucket_range)+"_"+addition+".png") , bbox_inches='tight') 
    plt.close()


def plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal(ICU_or_death,OG="",population_type_list = ["younger","older"]): # or "OG_"
    fig, ax = plt.subplots(1,1, figsize=(6,5))

    # first, some plotting to get some fake legends...
    legend_points = []

    


    
    max_y= 0

    for population_type in population_type_list:
        if population_type=='younger':
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
        if population_type=='older':
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))


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

                daily_deaths_after = []
                daily_ICU_admissions_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
                clinical_pd_obj = pd.read_csv(clinical_file)

                scale = 40
                aug_num = 5
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']>=simnum*aug_num) & (clinical_pd_obj['iteration']<(simnum+1)*aug_num)& (clinical_pd_obj['day']>time_split)]

                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())/aug_num
                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())/aug_num

                    daily_deaths_after.append(daily_deaths)
                    daily_ICU_admissions_after.append(daily_ICU_admissions)
                
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                percent_daily_deaths_after = [x/total_population*100 for x in daily_deaths_after]
                percent_daily_ICU_admissions_after = [x/total_population*100 for x in daily_ICU_admissions_after]
                
                if ICU_or_death == 'death':
                    ax.scatter(percent_infected_before, daily_deaths_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max( daily_deaths_after))
                elif ICU_or_death =='ICU':
                    ax.scatter(percent_infected_before, daily_ICU_admissions_after, color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max(daily_ICU_admissions_after))


    ax.set_xlim([15,85])
    if ICU_or_death == 'death':
        ax.set_ylim([0,20])
    else:
        ax.set_ylim([0,max_y+10])

    x_ticks = [20,30,40,50,60,70,80]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(x)+"\%" for x in x_ticks])

    
    # ax.grid(True)
    # ax.legend(legend_list)
    ax.set_xlabel('past attack rate (before t = 450)')
    ax.grid(True, which='major',color='gray')
    ax.set_axisbelow(True)

    if len(population_type_list)==2:
        ax.legend(legend_points[:3], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(0.47, 1), loc=1)
        leg = Legend(ax,legend_points[3:], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(0.47, 0.75), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points[:3], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0]+" population",bbox_to_anchor=(0.47, 1), loc=1)

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

        plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_deaths_vs_past_immunity"+OG+"_ages_80_booster_only_horizontal_"+addition+".png") , bbox_inches='tight')
        plt.close()
    elif ICU_or_death =='ICU':
        ax.set_ylabel('future ICU admissions (number of ICU admissions after t= ' + str(time_split) +")")
        #ax.set_title('ICU admissions given past immunity',fontsize=14)

        plt.savefig(os.path.join(folder,"abm_continuous_simulation_parameters_ICU_admissions_vs_past_immunity"+OG+"_ages_80_booster_only_horizontal_"+addition+".png") , bbox_inches='tight')
        plt.close()
       

def plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_vertical(ICU_or_death,OG="",population_type_list = ["younger","older"]): # or "OG_"
    fig, ax = plt.subplots(1,1, figsize=(6,6.75))

    # first, some plotting to get some fake legends...
    legend_points = []

    
    max_y= 0

    for population_type in population_type_list :
        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= 'o', alpha=1.0, edgecolors='none'))

        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= 'o', alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= 'o', alpha=1.0, edgecolors='none'))


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

                daily_deaths_after = []
                daily_ICU_admissions_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
                clinical_pd_obj = pd.read_csv(clinical_file)

                scale = 40
                aug_num = 5
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']>=simnum*aug_num) & (clinical_pd_obj['iteration']<(simnum+1)*aug_num)& (clinical_pd_obj['day']>time_split)]

                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())/aug_num
                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())/aug_num

                    daily_deaths_after.append(daily_deaths)
                    daily_ICU_admissions_after.append(daily_ICU_admissions)
                
                percent_infected_before = [x/total_population*100 for x in infections_per_sim_before]
                percent_infected_after = [x/total_population*100 for x in infections_per_sim_after ]

                percent_daily_deaths_after = [x/total_population*100 for x in daily_deaths_after]
                percent_daily_ICU_admissions_after = [x/total_population*100 for x in daily_ICU_admissions_after]
                
                if ICU_or_death == 'death':
                    ax.scatter(daily_deaths_after,percent_infected_before,  color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max( daily_deaths_after))
                elif ICU_or_death =='ICU':
                    ax.scatter(daily_ICU_admissions_after,percent_infected_before,  color=colour, s=scale, label=info_text, marker= marker, alpha=0.8, edgecolors='none')
                    max_y = max(max_y,max(daily_ICU_admissions_after))


    ax.set_ylim([15,85])
    if ICU_or_death == 'death':
        ax.set_xlim([0,20])
    else:
        ax.set_xlim([0,max_y+10])

    y_ticks = [20,30,40,50,60,70,80]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([str(y)+"\%" for y in y_ticks])

    
    # ax.grid(True)
    # ax.legend(legend_list)
    ax.set_ylabel('past attack rate (before t = 450)')
    ax.grid(True, which='major',color='gray')
    ax.set_axisbelow(True)

    if len(population_type_list)==2:
        ax.legend(legend_points[:3], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title="younger population",bbox_to_anchor=(1,1), loc=1)
        leg = Legend(ax,legend_points[3:], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"], title="older population",bbox_to_anchor=(1,0.8), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points[:3], ["20\% vaccination coverage", "50\% vaccination coverage","80\% vaccination coverage"],title=population_type_list[0]+" population",bbox_to_anchor=(1,1), loc=1)

    yticks = [15,20,30,40,50,60,70,80,85]
    for y0, y1 in zip(yticks[::2], yticks[1::2]):
        plt.axhspan(y0, y1, color='black', alpha=0.1, zorder=0)
    
    ax.invert_yaxis()

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]  

    if ICU_or_death == 'death':
        ax.set_xlabel('near-future deaths (t = 450 to 650)')
        #ax.set_title('Deaths given past hybrid immunity',fontsize=14)

        plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_deaths_vs_past_immunity"+OG+"_ages_80_booster_only_vertical_"+ addition+ ".png") , bbox_inches='tight')
        plt.close()
    elif ICU_or_death =='ICU':
        ax.set_xlabel('future ICU admissions (number of ICU admissions after t= ' + str(time_split) +")")
        #ax.set_title('ICU admissions given past immunity',fontsize=14)

        plt.savefig(os.path.join(folder,"abm_continuous_simulation_parameters_ICU_admissions_vs_past_immunity"+OG+"_ages_80_booster_only_vertical_"+ addition+ ".png") , bbox_inches='tight')
        plt.close()
       



def plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_boxplot(ICU_or_death,OG="",population_type_list = ["younger","older"],bucket_list ={20:[0,20],40:[20,40],60:[40,60],80:[60,80],100:[80,100]}): # or "OG_"
    fig, ax = plt.subplots(1,1, figsize=(7,7))

    # first, some plotting to get some fake legends...
    legend_points = []

    marker = "s"

    # starting_positions = [0,6,12,18,24]
    starting_positions = []
    for i in range(len(bucket_list)):
        position =i*3*len(population_type_list)
        starting_positions.append(position)
    
    max_y= 0
    box_counter = 0

    for population_type in population_type_list :
        if population_type=="younger":
            legend_points.append(ax.scatter(-10000,-10000,color='lightskyblue', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='dodgerblue', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='navy', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            
            
        if population_type=="older":
            legend_points.append(ax.scatter(-10000,-10000,color='salmon', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='red', s=100, marker= marker, alpha=1.0, edgecolors='none'))
            legend_points.append(ax.scatter(-10000,-10000,color='firebrick', s=100, marker= marker, alpha=1.0, edgecolors='none'))



        for paramNum in reversed(population_list):

            future_given_past_buckets = dict()
            for bucket,bucketrange in bucket_list.items():
                future_given_past_buckets [bucket] = []

            colour = "lightskyblue"

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

                daily_deaths_after = []
                daily_ICU_admissions_after = []

                clinical_filename = "_" + OG + "full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)
                clinical_pd_obj = pd.read_csv(clinical_file)

                scale = 40
                aug_num = 5
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']>=simnum*aug_num) & (clinical_pd_obj['iteration']<(simnum+1)*aug_num)& (clinical_pd_obj['day']>time_split)]

                    daily_deaths = sum(new_pd_ICU['daily_deaths'].to_list())/aug_num
                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())/aug_num

                    daily_deaths_after.append(daily_deaths)
                    daily_ICU_admissions_after.append(daily_ICU_admissions)

                    percent_infected_before = total_infections_before/total_population*100

                    if ICU_or_death == 'death':
                        after = daily_deaths
                    elif ICU_or_death =='ICU':
                        after = daily_ICU_admissions

                    for bucket,bucketrange in bucket_list.items():
                        if percent_infected_before>=bucketrange[0] and percent_infected_before < bucketrange[1]:
                            future_given_past_buckets[bucket].append(after)
                            break

                
                if booster_fraction == 0.8:
                    if ICU_or_death == 'death':
                        max_y = max(max_y,max( daily_deaths_after))
                    elif ICU_or_death =='ICU':
                        max_y = max(max_y,max(daily_ICU_admissions_after))
                    
            if booster_fraction == 0.8:
                total_summed_infections = [future_given_past_buckets[x] for x in bucket_list]

                positions = [x+box_counter for x in starting_positions ]
                print(positions)

                boxes= ax.boxplot(total_summed_infections, vert=False, patch_artist=True,positions=positions,medianprops=dict(color="cyan"),boxprops=dict(facecolor=colour, color=colour),
            capprops=dict(color=colour),
            whiskerprops=dict(color=colour),
            flierprops=dict(color=colour, markeredgecolor=colour))

                for patch in boxes['boxes']:
                    patch.set_facecolor(colour)
                box_counter+=1


    ax.set_ylim([-1,max(positions)+1])
    if ICU_or_death == 'death':
        ax.set_xlim([-2,20])
    else:
        ax.set_xlim([0,max_y+10])

    ax.set_yticks( [x+(starting_positions[1]-starting_positions [0]-1)/2 for x in starting_positions ])
    ax.set_yticklabels([str(bucketrange[0]) + "\% - " + str(bucketrange[1]) +"\%\npast attack rate" for bucket,bucketrange in bucket_list.items()])

    
    # ax.grid(True)
    # ax.legend(legend_list)
    ax.grid(True, which='major',color='gray',axis='x')
    ax.set_axisbelow(True)


    if len(population_type_list)==2:
        ax.legend(legend_points[:3], ["20\% vaccination coverage","50\% vaccination coverage","80\% vaccination coverage"],title="older population",bbox_to_anchor=(1, 0.2), loc=1)
        leg = Legend(ax,legend_points[3:],["20\% vaccination coverage","50\% vaccination coverage","80\% vaccination coverage"], title="younger population",bbox_to_anchor=(1, 0.4), loc=1)
        ax.add_artist(leg)
    else:
        ax.legend(legend_points[:3], ["20\% vaccination coverage","50\% vaccination coverage","80\% vaccination coverage"],title= population_type_list[0] +" population",bbox_to_anchor=(1, 0.2), loc=1)
    
    ax.set_ylabel('past attack rate (before t = 450)')


    yticks =[x-0.5 for x in starting_positions ]
    yticks.append(starting_positions[-1]+5.5)
    for y0, y1 in zip(yticks[::2], yticks[1::2]):
        plt.axhspan(y0, y1, color='black', alpha=0.1, zorder=0)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]   

    num_buckets = len(bucket_list)
    for bucket,bucketrange in bucket_list.items():
        bucket_range = bucketrange[1]-bucketrange[0]
        break

    if ICU_or_death == 'death':
        ax.set_xlabel('near-future deaths (t = 450 to 650)')
        #ax.set_title('Deaths given past hybrid immunity',fontsize=14)

        plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_deaths_vs_past_immunity"+OG+"_ages_80_booster_only_boxplot_buckets_"+str(num_buckets)+"-"+str(bucket_range)+"_"+addition+".png") , bbox_inches='tight')
        plt.close()
    elif ICU_or_death =='ICU':
        ax.set_xlabel('future ICU admissions (number of ICU admissions after t= ' + str(time_split) +")")
        ax.set_title('ICU admissions given past immunity',fontsize=14)

        plt.savefig(os.path.join(folder,"abm_continuous_simulation_parameters_ICU_admissions_vs_past_immunity"+OG+"_ages_80_booster_only_boxplot_buckets_"+str(num_buckets)+"-"+str(bucket_range)+"_"+addition+".png") , bbox_inches='tight')
        plt.close()
       

def plot_infection_population_breakdown_mean(population_type_list,local_param_list=population_list,local_TP_list=TP_list):  
    for population_type in population_type_list:
            
        for paramNum in local_param_list:
            for TP in local_TP_list:
                

                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)


                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]

                if booster_fraction ==0.5:
                    continue
                

                fig, ax = plt.subplots(1,1, figsize=(6,6.75))
                # info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate" +"\n"+ str(100*booster_fraction)+"\% booster fraction"
                info_text = population_type +" population with "+ str(100*total_vaccination_rate )+"\% vaccination coverage"
                
                sim_folder = "abm_continuous_simulation_parameters_" +population_type +"_" +str(paramNum)+"_SOCRATES_TP"+TP

                collected_simulated_population_by_age_band=[]

                collected_unvaxxed_uninfected_before_by_age_band=[]
                collected_unvaxxed_infected_before_by_age_band=[]
                collected_vaxxed_uninfected_before_by_age_band=[]
                collected_vaxxed_infected_before_by_age_band=[]

                collected_after_never_vaxxed_never_infected_by_age_band=[]
                collected_after_never_vaxxed_preinfection_no_postinfection_by_age_band=[]
                collected_after_never_vaxxed_no_preinfection_postinfection_by_age_band=[]
                collected_after_never_vaxxed_preinfection_postinfection_by_age_band=[]

                collected_prevaxxed_never_infected_by_age_band=[]
                collected_prevaxxed_preinfected_no_postinfection_by_age_band=[]
                collected_prevaxxed_no_preinfection_postinfection_by_age_band=[]
                collected_prevaxxed_preinfection_postinfection_by_age_band=[]

                collected_after_vaxxed_never_infected_by_age_band=[]
                collected_after_vaxxed_preinfected_no_postinfection_by_age_band=[]
                collected_after_vaxxed_no_preinfection_postinfection_by_age_band=[]
                collected_after_vaxxed_preinfection_postinfection_by_age_band=[]

                for sim_number in range(1,SIM_NUMBER+1):

                    filename_individuals = "sim_number_" + str(sim_number)+"_individuals.csv"

                    list_of_all_people = []
                    
                    individuals_file = os.path.join(folder,sim_folder,filename_individuals )
                    with open(individuals_file, newline='') as csvfile:
                        ind_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                        line_count = 0
                        
                        for row in ind_reader:
                            # print(line_count+1)
                            if line_count == 0:
                                # print(f'Column names are {", ".join(row)}')
                                line_count += 1
                            else:
                                # print(row)
                                age,age_bracket,dose_times,infection_times,symptom_onset_times = row 
                                new_row = [float(age),int(age_bracket),convert_to_array(dose_times),convert_to_array(infection_times),convert_to_array(symptom_onset_times)]
                                # if new_row[-1]!=[]:
                                #     print(new_row)
                                list_of_all_people.append(new_row)
                                line_count += 1


                    individuals_by_age_band = dict()
                    simulated_population_by_age_band=[0]*len(age_bands_abm)

                    unvaxxed_uninfected_before_by_age_band=[0]*len(age_bands_abm)
                    unvaxxed_infected_before_by_age_band=[0]*len(age_bands_abm)
                    vaxxed_uninfected_before_by_age_band=[0]*len(age_bands_abm)
                    vaxxed_infected_before_by_age_band=[0]*len(age_bands_abm)

                    after_never_vaxxed_never_infected_by_age_band=[0]*len(age_bands_abm)
                    after_never_vaxxed_preinfection_no_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_never_vaxxed_no_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_never_vaxxed_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)

                    prevaxxed_never_infected_by_age_band=[0]*len(age_bands_abm)
                    prevaxxed_preinfected_no_postinfection_by_age_band=[0]*len(age_bands_abm)
                    prevaxxed_no_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)
                    prevaxxed_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)

                    after_vaxxed_never_infected_by_age_band=[0]*len(age_bands_abm)
                    after_vaxxed_preinfected_no_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_vaxxed_no_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)
                    after_vaxxed_preinfection_postinfection_by_age_band=[0]*len(age_bands_abm)

                    num_unvaxxed_people = 0
                    num_people = 0
                    for person in list_of_all_people:
                        age,age_band,dose_times,infection_times,symptom_onset_times = person
                        simulated_population_by_age_band[age_band]= simulated_population_by_age_band[age_band]+1

                        # first, during the prewinter stage: (pre-time split stage)
                        vaxxed = False
                        infected = False
                        if dose_times!= [] and dose_times[1]<time_split:
                            # if they do get vaccinated, then must have at least two doses; if the second dose is before the time split at 400, then they're in the "prewinter" vaxxed group
                            vaxxed = True
                        
                        if symptom_onset_times!=[] and symptom_onset_times[0]< time_split:
                            # then in the infected before [winter] group
                            infected = True
                        
                        if vaxxed and infected:
                            vaxxed_infected_before_by_age_band[age_band]+=1
                        elif vaxxed and (not infected):
                            vaxxed_uninfected_before_by_age_band[age_band]+=1
                        elif (not vaxxed) and infected:
                            unvaxxed_infected_before_by_age_band[age_band]+=1
                        else:
                            unvaxxed_uninfected_before_by_age_band[age_band]+=1

                        # second, the winter stage (post-time split stage)

                        vaxxed_after = False
                        infected_after = False 

                        if dose_times!= [] and dose_times[1]>time_split:
                            # if they do get vaccinated, then must have at least two doses; if the second dose is after the time split at 400, then they're in the "winter" vaxxed group
                            vaxxed_after = True
                        
                        if symptom_onset_times!=[] and symptom_onset_times[-1] > time_split:
                            # then was infected after the time split
                            # technically could have had multiple infections... 
                            infected_after = True

                        if (not vaxxed) and (not vaxxed_after):
                            num_unvaxxed_people+=1
                            if (not infected) and (not infected_after):
                                after_never_vaxxed_never_infected_by_age_band[age_band]+=1
                                num_people+=1
                            elif infected and (not infected_after):
                                after_never_vaxxed_preinfection_no_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            elif (not infected) and infected_after:
                                after_never_vaxxed_no_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            else:
                                after_never_vaxxed_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                        elif vaxxed and (not vaxxed_after):
                            # if vaxxed during the pre-winter stage, did it help them or not?
                            if  (not infected) and (not infected_after):
                                prevaxxed_never_infected_by_age_band[age_band]+=1
                                num_people+=1
                            elif infected and (not infected_after):
                                prevaxxed_preinfected_no_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            elif (not infected) and infected_after:
                                prevaxxed_no_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            else:
                                prevaxxed_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                        elif vaxxed_after and (not vaxxed):
                            if (not infected) and (not infected_after):
                                after_vaxxed_never_infected_by_age_band[age_band]+=1
                                num_people+=1
                            elif infected and (not infected_after):
                                after_vaxxed_preinfected_no_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            elif (not infected) and infected_after:
                                after_vaxxed_no_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                            else:
                                after_vaxxed_preinfection_postinfection_by_age_band[age_band]+=1
                                num_people+=1
                        else:
                            print("there shouldn't be a double course of vaccinations!")
                            exit(1)
                        
                    
                    collected_simulated_population_by_age_band.append(simulated_population_by_age_band)

                    collected_unvaxxed_uninfected_before_by_age_band.append(unvaxxed_uninfected_before_by_age_band)
                    collected_unvaxxed_infected_before_by_age_band.append(unvaxxed_infected_before_by_age_band)
                    collected_vaxxed_uninfected_before_by_age_band.append(vaxxed_uninfected_before_by_age_band)
                    collected_vaxxed_infected_before_by_age_band.append(vaxxed_infected_before_by_age_band)

                    
                    

                    collected_after_never_vaxxed_never_infected_by_age_band.append(after_never_vaxxed_never_infected_by_age_band)
                    collected_after_never_vaxxed_preinfection_no_postinfection_by_age_band.append(after_never_vaxxed_preinfection_no_postinfection_by_age_band)
                    collected_after_never_vaxxed_no_preinfection_postinfection_by_age_band.append(after_never_vaxxed_no_preinfection_postinfection_by_age_band)
                    collected_after_never_vaxxed_preinfection_postinfection_by_age_band.append(after_never_vaxxed_preinfection_postinfection_by_age_band)

                    collected_prevaxxed_never_infected_by_age_band.append(prevaxxed_never_infected_by_age_band)
                    collected_prevaxxed_preinfected_no_postinfection_by_age_band.append(prevaxxed_preinfected_no_postinfection_by_age_band)
                    collected_prevaxxed_no_preinfection_postinfection_by_age_band.append(prevaxxed_no_preinfection_postinfection_by_age_band)
                    collected_prevaxxed_preinfection_postinfection_by_age_band.append(prevaxxed_preinfection_postinfection_by_age_band)

                    collected_after_vaxxed_never_infected_by_age_band.append(after_vaxxed_never_infected_by_age_band)
                    collected_after_vaxxed_preinfected_no_postinfection_by_age_band.append(after_vaxxed_preinfected_no_postinfection_by_age_band)
                    collected_after_vaxxed_no_preinfection_postinfection_by_age_band.append(after_vaxxed_no_preinfection_postinfection_by_age_band)
                    collected_after_vaxxed_preinfection_postinfection_by_age_band.append(after_vaxxed_preinfection_postinfection_by_age_band)

                    # print(sum(simulated_population_by_age_band))
                    # print(num_people)

                
                ####### MEAN #############################################################################################################
                
                mean_simulated_population_by_age_band = np.mean(np.array(collected_simulated_population_by_age_band), axis=0)
                mean_unvaxxed_uninfected_before_by_age_band = np.mean(np.array(collected_unvaxxed_uninfected_before_by_age_band), axis=0)
                mean_unvaxxed_infected_before_by_age_band = np.mean(np.array(collected_unvaxxed_infected_before_by_age_band), axis=0)
                mean_vaxxed_uninfected_before_by_age_band = np.mean(np.array(collected_vaxxed_uninfected_before_by_age_band), axis=0)
                mean_vaxxed_infected_before_by_age_band = np.mean(np.array(collected_vaxxed_infected_before_by_age_band), axis=0)

                mean_preinfection = sum(mean_unvaxxed_infected_before_by_age_band) + sum(mean_vaxxed_infected_before_by_age_band)

                mean_after_never_vaxxed_never_infected_by_age_band = np.mean(np.array(collected_after_never_vaxxed_never_infected_by_age_band), axis=0)
                mean_after_never_vaxxed_preinfection_no_postinfection_by_age_band = np.mean(np.array(collected_after_never_vaxxed_preinfection_no_postinfection_by_age_band), axis=0)
                mean_after_never_vaxxed_no_preinfection_postinfection_by_age_band = np.mean(np.array(collected_after_never_vaxxed_no_preinfection_postinfection_by_age_band), axis=0)
                mean_after_never_vaxxed_preinfection_postinfection_by_age_band = np.mean(np.array(collected_after_never_vaxxed_preinfection_postinfection_by_age_band), axis=0)

                mean_prevaxxed_never_infected_by_age_band = np.mean(np.array(collected_prevaxxed_never_infected_by_age_band), axis=0)
                mean_prevaxxed_preinfected_no_postinfection_by_age_band = np.mean(np.array(collected_prevaxxed_preinfected_no_postinfection_by_age_band), axis=0)
                mean_prevaxxed_no_preinfection_postinfection_by_age_band = np.mean(np.array(collected_prevaxxed_no_preinfection_postinfection_by_age_band), axis=0)
                mean_prevaxxed_preinfection_postinfection_by_age_band = np.mean(np.array(collected_prevaxxed_preinfection_postinfection_by_age_band), axis=0)

                mean_after_vaxxed_never_infected_by_age_band = np.mean(np.array(collected_after_vaxxed_never_infected_by_age_band), axis=0)
                mean_after_vaxxed_preinfected_no_postinfection_by_age_band = np.mean(np.array(collected_after_vaxxed_preinfected_no_postinfection_by_age_band), axis=0)
                mean_after_vaxxed_no_preinfection_postinfection_by_age_band = np.mean(np.array(collected_after_vaxxed_no_preinfection_postinfection_by_age_band), axis=0)
                mean_after_vaxxed_preinfection_postinfection_by_age_band = np.mean(np.array(collected_after_vaxxed_preinfection_postinfection_by_age_band), axis=0)

                #####################################################

                y_pos = np.arange(len(age_bands_abm))
                #####################################################
                # infections over ages and vaccine -- percentage: winter; mean

                
                fig, ax = plt.subplots(1,1, figsize=(6,6.75))

                y_pos = np.arange(len(age_bands_abm))

                df_mean_novaccine_list = [x/y*100 for x,y in zip(mean_unvaxxed_infected_before_by_age_band,mean_simulated_population_by_age_band)]
                uninfected_unvaxxed_list = [x/y*100 for x,y in zip(mean_unvaxxed_uninfected_before_by_age_band,mean_simulated_population_by_age_band)]
                df_mean_doseany_list = [x/y*100 for x,y in zip(mean_vaxxed_infected_before_by_age_band,mean_simulated_population_by_age_band)]
                uninfected_vaccinated_list = [x/y*100 for x,y in zip(mean_vaxxed_uninfected_before_by_age_band,mean_simulated_population_by_age_band)]
                
                list_2 = [mean_after_never_vaxxed_never_infected_by_age_band,mean_after_never_vaxxed_preinfection_no_postinfection_by_age_band,mean_after_never_vaxxed_no_preinfection_postinfection_by_age_band,mean_after_never_vaxxed_preinfection_postinfection_by_age_band,mean_prevaxxed_never_infected_by_age_band,mean_prevaxxed_preinfected_no_postinfection_by_age_band,mean_prevaxxed_no_preinfection_postinfection_by_age_band,mean_prevaxxed_preinfection_postinfection_by_age_band,mean_after_vaxxed_never_infected_by_age_band,mean_after_vaxxed_preinfected_no_postinfection_by_age_band,mean_after_vaxxed_no_preinfection_postinfection_by_age_band,mean_after_vaxxed_preinfection_postinfection_by_age_band ]
                mean_pop = [0]*len(age_bands_abm)
                for i in range(len(list_2)):
                    mean_pop = [x+y for x,y in zip(mean_pop,list_2[i])]
                print(sum(mean_pop))

                # not-vaxed, not-vaxed[winter], not-infected, not infected[winter]
                nvnv_nini = [x/y*100 for x,y in zip(mean_after_never_vaxxed_never_infected_by_age_band,mean_pop)]
                # not-vaxed, not-vaxed, yes-infected, not-infected
                nvnv_yini = [x/y*100 for x,y in zip(mean_after_never_vaxxed_preinfection_no_postinfection_by_age_band,mean_pop)]
                nvnv_niyi = [x/y*100 for x,y in zip(mean_after_never_vaxxed_no_preinfection_postinfection_by_age_band,mean_pop)]
                nvnv_yiyi =  [x/y*100 for x,y in zip(mean_after_never_vaxxed_preinfection_postinfection_by_age_band,mean_pop)]
                
                yvnv_nini= [x/y*100 for x,y in zip(mean_prevaxxed_never_infected_by_age_band,mean_pop)]
                yvnv_yini= [x/y*100 for x,y in zip(mean_prevaxxed_preinfected_no_postinfection_by_age_band,mean_pop)]
                yvnv_niyi= [x/y*100 for x,y in zip(mean_prevaxxed_no_preinfection_postinfection_by_age_band,mean_pop)]
                yvnv_yiyi= [x/y*100 for x,y in zip(mean_prevaxxed_preinfection_postinfection_by_age_band,mean_pop)]

                nvyv_nini= [x/y*100 for x,y in zip(mean_after_vaxxed_never_infected_by_age_band,mean_pop)]
                nvyv_yini= [x/y*100 for x,y in zip(mean_after_vaxxed_preinfected_no_postinfection_by_age_band ,mean_pop)]
                nvyv_niyi= [x/y*100 for x,y in zip(mean_after_vaxxed_no_preinfection_postinfection_by_age_band ,mean_pop)]
                nvyv_yiyi= [x/y*100 for x,y in zip(mean_after_vaxxed_preinfection_postinfection_by_age_band,mean_pop)]
                
                lists_of_values_order = [nvnv_yiyi,nvnv_niyi,nvnv_yini,nvnv_nini,nvyv_yiyi,nvyv_niyi,nvyv_yini,nvyv_nini,yvnv_yiyi,yvnv_niyi,yvnv_yini,yvnv_nini]
                colours = ["darkred","firebrick","crimson","pink",
                            "darkgreen","green","mediumseagreen","palegreen", #"indigo","purple","darkviolet","plum",
                            "midnightblue","blue","royalblue","lightskyblue"]
                left_list = [0]*len(nvnv_yiyi)
                for i in range(len(lists_of_values_order)):
                    ax.barh(y_pos,lists_of_values_order[i],left=left_list,color=colours[i])
                    left_list = [x+y for x,y in zip(left_list,lists_of_values_order[i])]
                print(left_list)
                

                ax.set_yticks(y_pos)
                ax.set_yticklabels(age_bands_abm)
                # ax.invert_yaxis()  # labels read top-to-bottom
                ax.set_xlabel('Proportion \%')
                ax.set_title('Mean infected population by vaccination status')
                # ax.set_xlim([0,15500])
                x_pos = list(range(0,101,10))
                ax.set_xticks(x_pos)
                ax.set_xticklabels([str(x)+"\%" for x in x_pos])
                ax.set_ylim([-0.5,16.5])

                ax.legend([
                    "Unvaccinated \& Infected Before + After", "Unvaccinated \& Infected After", "Unvaccinated \& Infected Before", "Unvaccinated \& Never Infected",
                    "Vaccinated After \& Infected Before + After","Vaccinated After \& Infected  After", "Vaccinated After \& Infected Before", "Vaccinated After \& Never Infected",
                    "Vaccinated Before \& Infected Before + After","Vaccinated Before \& Infected After","Vaccinated Before \& Infected Before","Vaccinated Before \& Never Infected"],title=info_text,bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)

                plt.savefig(os.path.join(folder, sim_folder+"_infections_by_age_brackets_vax_mean_STACKED_proportion_winter.png") , bbox_inches='tight')
                plt.close()
# plot_before_vs_after_infections()
# plot_before_vs_after_infections_combined_ages()
# plot_infection_population_breakdown()
# plot_ICU_and_deaths_vs_before_infections('death')
# plot_ICU_and_deaths_vs_before_infections('ICU')
# plot_infection_numbers(total_sims=5)

# plot_before_vs_after_infections_older_demographic_only()
# plot_before_and_after_infections_older_80_booster_only()

# plot_peak_height()

# plot_infection_numbers_combined(total_sims=5)
# plot_ICU_and_deaths_vs_before_infections_combined('death',OG="OG_")
# plot_ICU_and_deaths_vs_before_infections_combined('death',OG="")


# plot_before_vs_after_infections_combined_ages_80_booster_only(population_type_list = ["younger","older"])
# plot_before_vs_after_infections_combined_ages_80_booster_only(population_type_list = ["younger"])
# plot_before_vs_after_infections_combined_ages_80_booster_only(population_type_list = ["older"])
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger","older"])
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["younger"])
# plot_before_vs_after_infections_combined_ages_80_booster_only_horizontal(population_type_list = ["older"])

# bucket_list ={20:[0,20],40:[20,40],60:[40,60],80:[60,80],100:[80,100]}
# plot_before_vs_after_infections_combined_ages_80_booster_only_boxplot(["older","younger"],bucket_list)
# plot_before_vs_after_infections_combined_ages_80_booster_only_boxplot( ["younger"],bucket_list)
# plot_before_vs_after_infections_combined_ages_80_booster_only_boxplot(["older"],bucket_list)

# bucket_list ={20:[15,25],50:[45,55],80:[75,85]}
# plot_before_vs_after_infections_combined_ages_80_booster_only_boxplot(["older","younger"],bucket_list)
# plot_before_vs_after_infections_combined_ages_80_booster_only_boxplot( ["younger"],bucket_list)
# plot_before_vs_after_infections_combined_ages_80_booster_only_boxplot(["older"],bucket_list)


# plot_infection_population_breakdown_mean(["younger","older"],local_param_list=[2,6],local_TP_list=["0.85","2.05"])

plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal('death',OG="",population_type_list = ["younger","older"])
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal('death',OG="",population_type_list = ["younger"])
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_horizontal('death',OG="",population_type_list = ["older"])

plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_vertical('death',OG="",population_type_list = ["younger","older"])
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_vertical('death',OG="",population_type_list = ["younger"])
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_vertical('death',OG="",population_type_list = ["older"])


bucket_list ={20:[0,20],40:[20,40],60:[40,60],80:[60,80],100:[80,100]}
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_boxplot('death',"",["older","younger"],bucket_list)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_boxplot('death',"",["older"],bucket_list)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_boxplot('death',"",["younger"],bucket_list)

bucket_list ={20:[15,25],50:[45,55],80:[75,85]}
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_boxplot('death',"",["older","younger"],bucket_list)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_boxplot('death',"",["older"],bucket_list)
plot_ICU_and_deaths_vs_before_infections_combined_ages_80_booster_only_boxplot('death',"",["younger"],bucket_list)


