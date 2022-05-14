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

folder = os.path.join(os.path.dirname(__file__),"..","covid_continuous_simulations_outputs")

presim_parameters_folder =  os.path.join(os.path.dirname(__file__),"..","covid-abm-presim","continuous_sim_param_files")

max_days = 646
date_values = list(range(0,max_days+1,10))
date_names = [str(x) for x in date_values]

# date_values = [363,393,424,454,485,516,546,577,607,638]
# date_names = ["April","May","June","July","Aug","Sept","Oct","Nov","Dec","Jan"]
# date_values = [363,393,424,454,485,516,546]
# date_names = ["April","May","June","July","Aug","Sept","Oct"]

days = list(range(0,max_days+1))
# days = list(range(350,545))
xlim_values= [0,max_days]
max_infections=1300
num_infected_per_age_group = 6000

age_categories = ['[0,5)','[5,12)', '[12,16)', '[16,20)', '[20,25)', '[25,30)', '[30,35)',
    '[35,40)', '[40,45)', '[45,50)', '[50,55)', '[55,60)',
    '[60,65)', '[65,70)', '[70,75)', '[75,80)', '[80,Inf]']
age_bands = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']


for population_type in ["younger","older"]:
    population_list = list(range(1,6+1))
    TP_list = ["1.2","1.625","2.05","2.4749999999999996","2.9"]

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
            info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction\n" + "with TP = " + TP
            


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

            for simnum in df_dict.keys():
                infections_over_time = df_dict[simnum]
                infections_over_time_list = list_conversion_nans(infections_over_time, days)
                ax.plot(days,infections_over_time_list)
            # ax.set_ylim([0,max_infections])
            # ax.set_xlim(xlim_values)

            ax.set_xlabel('days')
            ax.set_ylabel('number of infections')
            ax.set_title('winter covid wave')

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

        