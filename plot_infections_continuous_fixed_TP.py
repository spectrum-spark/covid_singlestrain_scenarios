# clinical pathways 
import os
import pandas as pd
import json
import scipy.io
import numpy as np
import csv
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

time_split = 400
days_before = list(range(0,time_split))
days_after = list(range(time_split,650))

folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_double_exposure_3_outputs")
TP_list = ["1.75","2.0","2.25","2.5","2.75"]
population_list = list(range(1,6+1))

presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files")




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

                info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                
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
        ax.set_ylabel('\% of infected people after t = 400')
        ax.set_xlabel('\% of infected people before t = 400 ("past infection")')
        ax.set_title('Infected people given past immunity \nfor a ' + population_type + ' population',fontsize=14)

        plt.savefig(os.path.join(folder, filename+"_infections_past_immunity_" +population_type +".png") , bbox_inches='tight')
        plt.close()
        

def plot_infection_population_breakdown():  
    for population_type in ["younger","older"]:
            
            
        for paramNum in population_list:
            for TP in TP_list:
                fig, ax = plt.subplots(1,1, figsize=(6,6.75))

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
                info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate" +"\n"+ str(100*booster_fraction)+"\% booster fraction"
                
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

                for sim_number in range(1,21):

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
                ax.set_title('(Median Infected) Population Breakdown "Prewinter" ['+str(median_preinfection/100000*100)+'\% past attack rate]')
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
                ax.set_title('(Median Infected) Population Breakdown during "winter" ['+str(median_preinfection/100000*100)+'\% past attack rate]')
                # ax.set_xlim([0,15500])
                x_pos = list(range(0,101,10))
                ax.set_xticks(x_pos)
                ax.set_xticklabels([str(x)+"\%" for x in x_pos])

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

                info_text =  str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
                
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
                for simnum in df_dict.keys():
                    infections_over_time = df_dict[simnum]
                    total_infections_before = sum(list_conversion_nans(infections_over_time, days_before))
                    infections_per_sim_before.append(total_infections_before)

                    total_infections_after = sum(list_conversion_nans(infections_over_time, days_after))
                    infections_per_sim_after.append(total_infections_after)

                    new_pd_ICU = clinical_pd_obj.loc[(clinical_pd_obj['iteration']==simnum) & (clinical_pd_obj['day']>time_split)]

                    daily_deaths = sum(new_pd_ICU['daily_ICU_admissions'].to_list())
                    daily_ICU_admissions = sum(new_pd_ICU['daily_ICU_admissions'].to_list())

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
        ax.set_xlabel('\% of infected people before t = 400 ("past infection")')

        if ICU_or_death == 'death':
            ax.set_ylabel('number of deaths after t = 400')
            ax.set_title('Deaths given past immunity \nfor a ' + population_type + ' population',fontsize=14)

            plt.savefig(os.path.join(folder, filename+"_deaths_vs_past_immunity_" +population_type +".png") , bbox_inches='tight')
            plt.close()
        elif ICU_or_death =='ICU':
            ax.set_ylabel('number of ICU admissions after t= 400')
            ax.set_title('ICU admissions given past immunity \nfor a ' + population_type + ' population',fontsize=14)

            plt.savefig(os.path.join(folder, filename+"_ICU_admissions_vs_past_immunity_" +population_type +".png") , bbox_inches='tight')
            plt.close()
    return   
            
# plot_before_vs_after_infections()
# plot_infection_population_breakdown()
plot_ICU_and_deaths_vs_before_infections('death')
plot_ICU_and_deaths_vs_before_infections('ICU')