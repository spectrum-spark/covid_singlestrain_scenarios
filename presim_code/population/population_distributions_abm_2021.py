
# The western pacific region includes:
# Australia, Brunei, Cambodia, China, Cook Islands, Fiji, Japan, Kiribati, Laos, Malaysia, Marshall Islands, Micronesia, Mongolia, Nauru, New Zealand, Niue, Palau, Papua New Guinea, Philippines, Samoa, Singapore, Solomon Islands, South Korea, Tonga, Tuvalu, Vanuatu, Vietnam. 

# see list here https://www.who.int/westernpacific/about/where-we-work

# population data obtained from https://population.un.org/wpp/DataQuery/
# (not all WHO named countries could be found)

import pandas as pd
import json
import os

import math
import numpy as np
from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'serif'})
import matplotlib.pyplot as plt
plt.switch_backend('agg')

file_path = os.path.join(os.path.dirname(__file__),'PopulationAgeSex-20220412011050.xlsx')

df = pd.read_excel(file_path,sheet_name='Data', skiprows=[0])
df = df.drop(columns=['ISO 3166-1 numeric code','Sex', 'Note'])
df=df.dropna(subset=['0-4'])

# for each, calculate the total population across ages, and calculate the total 65+
# (done directly in the excel file)


# OADR (old-age dependency ratio) = (total 65+) / (total 20-64) *100
# YADR (young-age dependency ratio) = (total 19-) / (total 20-64) *100

# older population: let me define as OADR> 15 (to include French Polynesia)
# while younger population is OADR < 12 (to include PNG)
# and I will discard the others

OADR_old = 15
OADR_young = 12

gathered_dictionary = {'older':{},'younger':{}}

for year in [2021]:
    
    gathered_dictionary['older'][year]=df.loc[(df['OADR'] >= OADR_old ) & (df['Time'] == year)].to_dict(orient="index")
    
    gathered_dictionary['younger'][year] = df.loc[(df['OADR']<= OADR_young ) & (df['Time'] == year)].to_dict(orient="index")

age_bands = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90-94', '95-99', '100+']

age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']

# change all population values in each country to PROPORTIONS 
population_proportions_full = {'older':{2021:{}},'younger':{2021:{}}}
population_proportions_abm = {'older':{2021:{}},'younger':{2021:{}}}


for year in [2021]:
    for population_type in ['older','younger']:

        num_countries = len(gathered_dictionary[population_type][year].keys())

        for index in gathered_dictionary[population_type][year].keys():
            tot_pop = gathered_dictionary[population_type][year][index]['Total Population']
            country_name = gathered_dictionary[population_type][year][index]['Location'].lstrip()

            population_dictionary = dict()
            for age_band in age_bands:
                population_dictionary[age_band] = gathered_dictionary[population_type][year][index][age_band]/tot_pop

            population_proportions_full[population_type][year][country_name] = population_dictionary

            # for ABM population groupings
            param_set = dict()
            for age_band in ["0-4", '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79']:
                param_set[age_band] = population_dictionary[age_band] 

            param_set["5-11"] = population_dictionary["5-9"] + (2/5)*population_dictionary["10-14"]

            param_set["12-15"] = (3/5)*population_dictionary["10-14"] + (1/5)*population_dictionary["15-19"]

            param_set["16-19"] =(4/5)*population_dictionary["15-19"]

            param_set["80+"] = population_dictionary['80-84']+population_dictionary['85-89']+population_dictionary['90-94']+population_dictionary['95-99']+population_dictionary['100+']

            population_proportions_abm[population_type][year][country_name] = param_set

#print(population_proportions_abm)

averaged_population_proportions_abm = {'older':{2021:{}},'younger':{2021:{}}}
for year in [2021]:
    for population_type in ['older','younger']:

        ##  ABM age bands
        ave_population_dictionary = dict()
        for age_band in age_bands_abm:

            list_pop = [population_proportions_abm[population_type][year][country][age_band] for country in population_proportions_abm[population_type][year]]
            ave_population_dictionary[age_band] = sum(list_pop)/len(list_pop)

        averaged_population_proportions_abm[population_type][year] = ave_population_dictionary

print(averaged_population_proportions_abm)

# write averaged populations to file
folder_path = os.path.join(os.path.dirname(__file__))
for year in [2021]:
    for population_type in ['older','younger']:
        param_set =averaged_population_proportions_abm[population_type][year]

        file_save_name = "abm_population_" + str(population_type) +"_year_" +str(year)+".json"
        fullfilename = os.path.join(folder_path,file_save_name)

        # Serializing json 
        json_object = json.dumps(param_set, indent = 4)
        
        # Writing to sample.json
        with open(fullfilename, "w") as outfile:
            outfile.write(json_object)


# abm age distribution plots
for year in [2021]:
    for population_type in ['older','younger']:
        if population_type =="younger":
            plotting_colour_0 = 'navy'
            plotting_colour_1 = 'dodgerblue'
            plotting_colour_2 = 'lightskyblue'
        elif population_type=="older":
            plotting_colour_0 = 'firebrick'
            plotting_colour_1 = 'red'
            plotting_colour_2 = 'salmon'
        
        num_countries = len(population_proportions_abm[population_type][year].keys())

        fig, ax_list = plt.subplots(math.ceil(num_countries/4),4, figsize=(3.5*4,3.5*math.ceil(num_countries/4)),sharex=True, sharey=True)
        ax_index = 0
        ax_list = [j for sub in ax_list for j in sub] # flattening list

        for country in population_proportions_abm[population_type][year].keys():
            ax =ax_list[ax_index]

            if population_type =="younger":
                if ax_index%3==0:
                    plotting_colour= 'navy'
                elif ax_index%3==1:
                    plotting_colour = 'dodgerblue'
                else:
                    plotting_colour = 'lightskyblue'
            elif population_type=="older":
                if ax_index%3==0:
                    plotting_colour = 'firebrick'
                elif ax_index%3==1:
                    plotting_colour = 'red'
                else:
                    plotting_colour = 'salmon'

            population = [population_proportions_abm[population_type][year][country][age] for age in age_bands_abm]
            

            y_pos = (np.arange(len(age_bands_abm)))

            # print(country)
            # print(population_proportions_abm[population_type][year][country])
            # print(population)

            ax.barh(y_pos,population,color=plotting_colour)
            ax.set_yticks(y_pos) 
            ax.set_yticklabels(age_bands_abm)
            #ax.invert_yaxis() # labels read top-to-bottom
            if ax_index > num_countries-4:
                ax.set_xlabel('Population proportion')
                ax.xaxis.set_tick_params(labelbottom=True)
            if ax_index%4==0:
                ax.set_ylabel("Age band")
            # ax.set_title(country)
            ax.xaxis.grid()
            ax.set_axisbelow(True)
            ax.legend([],title=country)
            ax.set_ylim([-0.4,16.4])
            
            ax_index+=1
        
        
        # now for the averaged
        population = [averaged_population_proportions_abm[population_type][year][age] for age in age_bands_abm]
        y_pos = (np.arange(len(age_bands_abm)))

        ax =ax_list[ax_index]
        ax.barh(y_pos,population,color=[plotting_colour_0,plotting_colour_1,plotting_colour_2])
        ax.set_facecolor('grey')
        ax.set_yticks(y_pos) 
        ax.set_yticklabels(age_bands_abm)
        #ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Population proportion')
        #ax.set_ylabel("Age band")

        ax.xaxis.grid()
        ax.set_axisbelow(True)
        ax.legend([],title="Averaged")
        ax.set_ylim([-0.4,16.4])

        if population_type =='younger':
            ax_list[-1].set_visible(False)
            ax_list[-2].set_visible(False)
        
        file_save_name = "ABM_population_" + str(population_type) +"_year_" +str(year)+".png"
        fullfilename = os.path.join(folder_path,file_save_name)
        # plt.tight_layout()
        plt.subplots_adjust(wspace=0.1, hspace=0.1)
        plt.savefig(fullfilename, bbox_inches='tight')
        plt.close()
