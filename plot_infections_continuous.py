from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'sans-serif'})

import matplotlib.pyplot as plt
plt.switch_backend('agg')

import os
import sys
# import csv
import pandas as pd
import numpy as np
import json


# folder = sys.argv[1]
# file = sys.argv[2]

def list_conversion(dictionary, xvalues):
    new_list = []
    for x in xvalues:
        try:
            new_list.append(dictionary[x])
        except:
            new_list.append(0)
    return new_list

population_list = list(range(1,6+1))
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_outputs")
TP_list = ["1.2","1.625","2.05","2.4749999999999996","2.9"]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_outputs")
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_2_outputs")
# TP_list = ["2.0","2.25","2.5","2.75","3.0"]

# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_3_outputs")
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_outputs")
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_400_outputs")
# TP_list = ["1.75","2.0","2.25","2.5","2.75"]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_first_then_cont_exposure_outputs")

# TP_list = ["1.05","1.225","1.4","1.575"]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_400-2_outputs")
# population_list = [1,2,3,4,5]

# TP_list = ["1.1","1.2000000000000002","1.3","1.4","1.5"]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_outputs")


# TP_list = ["0.95","1.0","1.05", "1.1","1.15", "1.2000000000000002","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95"]
# TP_list = ["0.95","1.0","1.05", "1.1","1.15", "1.2000000000000002","1.25", "1.3","1.35"]
R0_ratio= 1.1131953802735288
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs")


TP_list = ["0.85","0.9","0.95","1.0","1.05", "1.1","1.15", "1.2","1.25", "1.3","1.35", "1.4", "1.45","1.5","1.55","1.6","1.65","1.7","1.75","1.8","1.85","1.9","1.95","2.0","2.05"]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_rerun_outputs")
folder = os.path.join(os.path.dirname(__file__),"..","covid_no_ttiq_450-2_ibm_4th_doses_newstrain_outputs")

population_list = [1,2,3,4,5,6]
presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files")

# TP_list = ["1.75","2.75"]
# population_list = [1,6]
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_cont_exposure_outputs_daily")
# folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_cont_exposure_outputs_weekly")




days_per_stage = 7*26 # 26 weeks

max_days = 650 #550 #646
date_values = list(range(0,max_days+1,10))
date_names = [str(x) for x in date_values]

# date_values = [363,393,424,454,485,516,546,577,607,638]
# date_names = ["April","May","June","July","Aug","Sept","Oct","Nov","Dec","Jan"]
# date_values = [363,393,424,454,485,516,546]
# date_names = ["April","May","June","July","Aug","Sept","Oct"]

days = list(range(0,max_days+1))
# days = list(range(350,545))
xlim_values= [0,max_days]
max_infections=5000 # 2000
num_infected_per_age_group = 6000

age_categories = ['[0,5)','[5,12)', '[12,16)', '[16,20)', '[20,25)', '[25,30)', '[30,35)',
    '[35,40)', '[40,45)', '[45,50)', '[50,55)', '[55,60)',
    '[60,65)', '[65,70)', '[70,75)', '[75,80)', '[80,Inf]']
age_bands = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']

def plot_individual():

    for population_type in ["older","younger"]:

        for paramNum in population_list:
            for TP in TP_list:

                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                print(filename)

                datafilename = filename + ".csv"

                if population_type =="younger":
                    plotting_colour =  "lightskyblue"
                    
                elif population_type=="older":
                    plotting_colour =  "lightcoral"

                data_file = os.path.join(folder, datafilename)

                pd_obj = pd.read_csv(data_file)
                # print(pd_obj)


                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)


                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction = presim_parameters["booster_fraction"]
                if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                else:
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))


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

                fig, ax = plt.subplots(1,1, figsize=(6,3.375)) # 16:9

                # colormap = plt.cm.get_cmap('inferno')
                num_plots = len(list(df_dict.keys()))
                if population_type == "older":
                    ax.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, num_plots))))
                else:
                    ax.set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 0.5, num_plots))))

                pre_infections = []
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    infections_over_time_list = list_conversion_nans(infections_over_time, days)
                    ax.plot(days,infections_over_time_list)
                    pre_infections.append(sum(infections_over_time_list[:400]))

                ax.set_ylim([0,max_infections])
                # ax.set_xlim(xlim_values)

                ax.set_xlabel('days')
                ax.set_ylabel('number of infections')
                ax.set_title('winter covid wave with ' + str(np.mean(pre_infections)) + " mean first-wave infections pre t=400")

                # ax.set_xticks(date_values)
                # ax.set_xticklabels(date_names)

                ax.text(0.2,0.8,info_text,fontsize='large', multialignment ='left', ha='center', va='center', transform=ax.transAxes)
                

                plt.savefig(os.path.join(folder, filename+"_infections_over_time.png") , bbox_inches='tight')
                plt.close()

                

                
                

                #####################################################
                # infections over ages and vaccine 

                novaccine = pd_obj[pd_obj['vaccine'] =='Unvaccinated']
                vaxxed = pd_obj[pd_obj['vaccine'] !='Unvaccinated']

                # c(0,5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80,Inf)
                

                # no vaccine
                new_pd = novaccine.groupby(['bracket','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='bracket', columns='sim', values='n')
                # df['index'] = pd.Categorical(df.index, categories=age_categories, ordered=True)
                # df.sort_values('bracket')
                df_median_novax = (df.median(axis='columns')).to_dict()
                median_total_infections_novax = sum(df_median_novax.values())

                new_pd = vaxxed.groupby(['bracket','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='bracket', columns='sim', values='n')
                # df['index'] = pd.Categorical(df.index, categories=age_categories, ordered=True)
                # df.sort_values('bracket')
                df_median_vaxxed = (df.median(axis='columns')).to_dict()
                median_total_infections_vaxxed = sum(df_median_vaxxed.values())

                fig, ax = plt.subplots(1,1, figsize=(6,6.75))

                y_pos = np.arange(len(age_bands))

                df_median_vaxxed_list = list_conversion(df_median_vaxxed,age_categories)
                df_median_unvaxxed_list = list_conversion(df_median_novax,age_categories)
                
                # print(df_median_novax)
                # print(df_median_unvaxxed_list)

                ax.barh(y_pos,df_median_unvaxxed_list,color="plum")
                ax.barh(y_pos,df_median_vaxxed_list, left=df_median_unvaxxed_list,color="mediumpurple")

                ax.set_yticks(y_pos)
                ax.set_yticklabels(age_bands )
                # ax1.invert_yaxis()  # labels read top-to-bottom
                ax.set_xlabel('Number of people')
                ax.set_title('Median number of unvaccinated ('+str(median_total_infections_novax)+') and \n vaccinated ('+str(median_total_infections_vaxxed)+') infected people in each age group',fontsize=14)

                ax.legend(["Unvaccinated", "Vaccinated (during prewinter)"],title=info_text)

                #ax.text(0.2,0.8,info_text,fontsize='large', multialignment ='left', ha='center', va='center', transform=ax.transAxes)

                # ax.set_xlim([0,num_infected_per_age_group])

                plt.savefig(os.path.join(folder, filename+"_infections_by_age_brackets_vaxstatus_median.png") , bbox_inches='tight')
                plt.close()


    
####################
def plot_combined():

    fig, ax = plt.subplots(1,1, figsize=(10,4)) # 16:9

    for population_type in ["older","younger"]:

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

                if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                else:
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))

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
                    ax.plot(days,infections_over_time_list,alpha=0.025,color="black") # for poster: alpha = 0.025, alpha = 0.1 for the others
                    #pre_infections.append(sum(infections_over_time_list[:400]))

    ax.set_ylim([0,max_infections])
    ax.set_xlim([0,max_days])
    ax.grid(color='lightgray', linestyle='dashed')

    ax.set_xlabel('time (days)')
    ax.set_ylabel('number of infections')
    # ax.set_title('winter covid wave with ' + str(np.mean(pre_infections)) + " mean first-wave infections pre t=400")

    # ax.set_xticks(date_values)
    # ax.set_xticklabels(date_names)

    # ax.text(0.2,0.8,info_text,fontsize='large', multialignment ='left', ha='center', va='center', transform=ax.transAxes)
                

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_combined_pop_infections_over_time.png") , bbox_inches='tight')
    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_combined_pop_infections_over_time.svg") , bbox_inches='tight')
    plt.close()

def plot_combined_older_80_booster():
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

                if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                else:
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))

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
                    ax.plot(days,infections_over_time_list,alpha=0.08,color="black") # for poster: alpha = 0.025, alpha = 0.1 for the others
                    #pre_infections.append(sum(infections_over_time_list[:400]))

    ax.set_ylim([0,max_infections])
    ax.set_xlim([0,max_days])
    ax.grid(color='lightgray', linestyle='dashed')

    ax.set_xlabel('time (days)')
    ax.set_ylabel('number of infections')
    # ax.set_title('winter covid wave with ' + str(np.mean(pre_infections)) + " mean first-wave infections pre t=400")

    # ax.set_xticks(date_values)
    # ax.set_xticklabels(date_names)

    # ax.text(0.2,0.8,info_text,fontsize='large', multialignment ='left', ha='center', va='center', transform=ax.transAxes)
                

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_combined_older_80_booster_pop_infections_over_time.png") , bbox_inches='tight')
    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_combined_older_80_booster_pop_infections_over_time.svg") , bbox_inches='tight')
    plt.close()


def plot_combined_80_booster(population_type_list = ["younger","older"]):
    fig, ax = plt.subplots(1,1, figsize=(10,4)) # 16:9

    for population_type in population_type_list:

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

                if folder != os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_outputs"):
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                else:
                    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + str(round(float(TP)*R0_ratio,3))

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

                # if len(population_type_list)==2:
                #     if total_vaccination_rate == 0.2:
                #         colour = "darkorchid"
                #     else:
                #         colour = "forestgreen"

                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    infections_over_time_list = list_conversion_nans(infections_over_time, days)
                    ax.plot(days,infections_over_time_list,alpha=0.05,color=colour)#"black") # for poster: alpha = 0.025, alpha = 0.1 for the others
                    #pre_infections.append(sum(infections_over_time_list[:400]))

    ax.set_ylim([0,max_infections])
    ax.set_xlim([0,max_days])
    ax.grid(color='lightgray', linestyle='dashed')

    ax.set_xlabel('time (days)')
    ax.set_ylabel('number of infections')
    # ax.set_title('winter covid wave with ' + str(np.mean(pre_infections)) + " mean first-wave infections pre t=400")

    # ax.set_xticks(date_values)
    # ax.set_xticklabels(date_names)

    # ax.text(0.2,0.8,info_text,fontsize='large', multialignment ='left', ha='center', va='center', transform=ax.transAxes)

    if len(population_type_list)==2:
        addition = "combined"
    else:
        addition = population_type_list[0]                

    plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_combined_80_booster_pop_infections_over_time_" + addition +".png") , bbox_inches='tight')
    # plt.savefig(os.path.join(folder, "abm_continuous_simulation_parameters_combined_older_80_booster_pop_infections_over_time.svg") , bbox_inches='tight')
    plt.close()



plot_combined()
# plot_combined_older_80_booster()
# plot_combined_80_booster(population_type_list = ["younger","older"])
# plot_combined_80_booster(population_type_list = ["younger"])
# plot_combined_80_booster(population_type_list = ["older"])