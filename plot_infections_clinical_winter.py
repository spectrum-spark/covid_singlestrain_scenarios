# clinical pathways 
import os
import pandas as pd
import json
import scipy.io
import numpy as np
from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'sans-serif'})

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

days = list(range(350,545+1))

folder = os.path.join(os.path.dirname(__file__),"..","winter_outputs")
presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","presim_param_files")
param_list = {'younger':{'0.5':[1,5,9,3,7,11],'0.8':[2,6,10,4,8,12]},'older':{'0.5':[13,17,21,15,19,23],'0.8':[14,18,22,16,20,24]}}

plot_all_infections_box_plot = False

for population_type in ["younger","older"]:
    for booster_fraction in [0.5,0.8]:

        if plot_all_infections_box_plot:

            fig, ax = plt.subplots(1,1, figsize=(6,6.75))

            y_positions = np.arange(len(param_list[population_type][str(booster_fraction)]))
            median_values = []
            quantile_lower = []
            quantile_upper = []
            labels = []
            total_summed_infections = []

            for paramNum in param_list[population_type][str(booster_fraction)]:
                presim_parameters = "abm_pre-simulation_parameters_"+str(paramNum)+".json"
                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)
                total_population = presim_parameters["total_population"]
                population_type = presim_parameters["population_type"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                booster_fraction_param = presim_parameters["booster_fraction"]
                total_attack_rate  = presim_parameters["total_attack_rate"]
                info_text =  population_type +" population, "+ str(100*total_vaccination_rate )+"\% vax rate,\n" +str(100*total_attack_rate)+ "\% past attack rate, \n" + str(100*booster_fraction_param)+"\% booster fraction"

                info_text =  str(100*total_vaccination_rate )+"\% vax rate,\n" +str(100*total_attack_rate)+ "\% past attack rate" 

                filename = "abm_simulation_people_params_"+str(paramNum)+"_output_winter_sims_"+population_type+"_init10"
                datafilename = filename + ".csv"
                data_file = os.path.join(folder, datafilename)
                pd_obj = pd.read_csv(data_file)

                # clinical_filename = "_full_outcomes_dataframe.csv"
                # clinical_file = os.path.join(folder,filename,clinical_filename)
                # clinical_pd_obj = pd.read_csv(clinical_file)
                # print(clinical_pd_obj)

                # clinical_mat = "_0.6         0.2    0.066667_full.mat"
                # clinical_mat_file = os.path.join(folder,filename,clinical_mat)
                # mat = scipy.io.loadmat(clinical_mat_file)
                # print(mat)

                # total infections vs immunity combinations

                new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
                df = new_pd.pivot(index='day', columns='sim', values='n')
                df_dict = df.to_dict()
                infections_per_sim = []
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections = sum(list_conversion_nans(infections_over_time, days))
                    infections_per_sim.append(total_infections)
                
                print(infections_per_sim)
                infection_median = np.median(infections_per_sim)
                infection_std = np.std(infections_per_sim)
                infection_quant_lower = np.quantile(infections_per_sim,0.025)
                infection_quant_upper = np.quantile(infections_per_sim,0.975)
                print("infection_median:",infection_median)
                print("infection_std:",infection_std)
                print("infection_quant_lower:",infection_quant_lower)
                print("infection_quant_upper:",infection_quant_upper)

                median_values.append(infection_median)
                quantile_lower.append(infection_quant_lower)
                quantile_upper.append(infection_quant_upper)
                total_summed_infections.append(infections_per_sim)
                
                labels.append(info_text)

            # ax.barh(y_positions,median_values)
            

            boxes= ax.boxplot(total_summed_infections, vert=False, patch_artist=True,positions=[0,0.5,1,2,2.5,3],medianprops=dict(color="cyan"))
            
            colors = ['lightskyblue', 'dodgerblue', 'navy', 'lightskyblue', 'dodgerblue', 'navy']
            for patch, color in zip(boxes['boxes'], colors):
                patch.set_facecolor(color)
            
            # ax.set_yticks(y_positions)
            ax.set_yticklabels(labels)
            ax.invert_yaxis()  # labels read top-to-bottom
            ax.set_xlim([-1000,60000])


            ax.set_xlabel('Infected people')
            ax.set_title('Median infected people given past immunity \nfor a ' + population_type + ' population with '+str(100*booster_fraction_param)+"\% booster uptake",fontsize=14)

            plt.savefig(os.path.join(folder, filename+"_median_infections_past_immunity_" +population_type +"_booster_" + str(booster_fraction)+".png") , bbox_inches='tight')
            plt.close()


        
        total_summed_ICUs = []
        total_summed_deaths = []
        labels = []

        for paramNum in param_list[population_type][str(booster_fraction)]:
            presim_parameters = "abm_pre-simulation_parameters_"+str(paramNum)+".json"
            presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

            with open(presimfilename, "r") as f:
                presim_parameters = json.load(f)
            total_population = presim_parameters["total_population"]
            population_type = presim_parameters["population_type"]
            total_vaccination_rate = presim_parameters["total_vaccination_rate"]
            booster_fraction_param = presim_parameters["booster_fraction"]
            total_attack_rate  = presim_parameters["total_attack_rate"]
            info_text =  population_type +" population, "+ str(100*total_vaccination_rate )+"\% vax rate,\n" +str(100*total_attack_rate)+ "\% past attack rate, \n" + str(100*booster_fraction_param)+"\% booster fraction"

            info_text =  str(100*total_vaccination_rate )+"\% vax rate,\n" +str(100*total_attack_rate)+ "\% past attack rate" 

            filename = "abm_simulation_people_params_"+str(paramNum)+"_output_winter_sims_"+population_type+"_init10"
            datafilename = filename + ".csv"
            data_file = os.path.join(folder, datafilename)
            pd_obj = pd.read_csv(data_file)

            clinical_filename = "_full_outcomes_dataframe.csv"
            clinical_file = os.path.join(folder,filename,clinical_filename)
            clinical_pd_obj = pd.read_csv(clinical_file)

            # print(clinical_pd_obj)

            # clinical_mat = "_0.6         0.2    0.066667_full.mat"
            # clinical_mat_file = os.path.join(folder,filename,clinical_mat)
            # mat = scipy.io.loadmat(clinical_mat_file)
            # print(mat)

            for col in clinical_pd_obj.columns:
                print(col)
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
            
            new_pd_ICU = clinical_pd_obj.groupby('iteration').sum()
            # print(new_pd_ICU)
            # print(new_pd_ICU['daily_admissions'].to_list())
            print(new_pd_ICU['daily_ICU_admissions'].to_list())
            daily_ICU_admissions = new_pd_ICU['daily_ICU_admissions'].to_list()
            total_summed_ICUs.append(daily_ICU_admissions )
            total_summed_deaths.append(new_pd_ICU['daily_deaths'].to_list())

            labels.append(info_text)

        fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        y_positions = np.arange(len(param_list[population_type][str(booster_fraction)]))
        boxes= ax.boxplot(total_summed_ICUs, vert=False, patch_artist=True,positions=[0,0.5,1,2,2.5,3],medianprops=dict(color="orange"))
        colors = ['orangered', 'red', 'firebrick', 'orangered', 'red', 'firebrick']
        for patch, color in zip(boxes['boxes'], colors):
            patch.set_facecolor(color)
        
        # ax.set_yticks(y_positions)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlim([-5,175])
        ax.set_xlabel('Total ICU admissions')
        ax.set_title('Total ICU admissions given past immunity \nfor a ' + population_type + ' population with '+str(100*booster_fraction_param)+"\% booster uptake",fontsize=14)

        plt.savefig(os.path.join(folder, "total_ICU_admissions_past_immunity_" +population_type +"_booster_" + str(booster_fraction)+".png") , bbox_inches='tight')
        plt.close()

        fig, ax = plt.subplots(1,1, figsize=(6,6.75))
        y_positions = np.arange(len(param_list[population_type][str(booster_fraction)]))
        boxes= ax.boxplot(total_summed_deaths, vert=False, patch_artist=True,positions=[0,0.5,1,2,2.5,3],medianprops=dict(color="red"))
        colors = ['lightgrey', 'grey', 'black','lightgrey', 'grey', 'black']
        for patch, color in zip(boxes['boxes'], colors):
            patch.set_facecolor(color)
        
        # ax.set_yticks(y_positions)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlim([-2,60])
        ax.set_xlabel('Total deaths')
        ax.set_title('Total deaths given past immunity \nfor a ' + population_type + ' population with '+str(100*booster_fraction_param)+"\% booster uptake",fontsize=14)

        plt.savefig(os.path.join(folder, "total_deaths_past_immunity_" +population_type +"_booster_" + str(booster_fraction)+".png") , bbox_inches='tight')
        plt.close()

        

        



            
        