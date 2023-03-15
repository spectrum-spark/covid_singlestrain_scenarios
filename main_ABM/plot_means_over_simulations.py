import os
import csv
import json
import pandas as pd
import numpy as np
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

###############################################################
# fixed / universal parameters

age_bands_abm = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_bands_upper = [5,12,16,20,25,30,35,40,45,50,55,60,65,70,75,80]

age_bands_clinical =  [0,10,20,30,40,50,60,70,80]
age_bands_clinical_names =  ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]

days_per_stage = 7*26 
one_year = 52*7
first_exposure_time =225
original_program_time = 26*7*3
boosters_only_vaccination_duration = 13*7# i.e. about 3 months


###############################################################
# main function


def plot_clinical_outcomes_over_simulations(
        TP_list = ["1.05", "1.95"],
        TP_type_list = ['TP_low','TP_high'],
        param_list = [0,1,2,3,4,5,6,7],
        population_type_list = ["younger","older"],
        boosting_group_names = {'none':'no further boosting', '65+': 'boosting 65+','55+':'boosting 55+','45+':'boosting 45+','35+':'boosting 35+','25+':'boosting 25+','16+':'boosting 16+','5+':'boosting 5+'},
        presim_parameters_folder = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_age_scenarios/',
        folder = '/scratch/cm37/tpl/', # need to put immune escape times
        days_all = list(range(0,100)),
        days_name = "100_days",
        mean_or_median = "mean",
        ):

    mega_DF_list_iterated = dict()

    # for different sub-scenarios (TPs, population type, and param nums), gather the clinical outcomes into a huge dataframe 
    for TP_type, TP_val in zip(TP_type_list,TP_list):
        for population_type in population_type_list:
            for paramNum in param_list: 

                # load in parameters:
                presim_parameters = "abm_continuous_simulation_parameters_" + population_type+ "_" + str(paramNum)+".json"

                presimfilename = os.path.join(presim_parameters_folder,presim_parameters)

                with open(presimfilename, "r") as f:
                    presim_parameters = json.load(f)

                total_population = presim_parameters["total_population"]
                total_vaccination_rate = presim_parameters["total_vaccination_rate"]
                vaccination_start = presim_parameters["boosters_only_vaccination_start"]
                boosting_group = presim_parameters['boosting_group']

                # load in clinical data file
                filename = "abm_continuous_simulation_parameters_"+population_type+"_"+str(paramNum)+"_SOCRATES_TP"+TP_val

                clinical_filename = "_full_outcomes_dataframe.csv"
                clinical_file = os.path.join(folder,filename,clinical_filename)

                if os.path.isfile(clinical_file):
                    pass
                else:
                    print(clinical_file +" DOES NOT EXIST!")
                    continue

                clinical_pd_obj = pd.read_csv(clinical_file)

                # select the days that matter and then drop the days column
                clinical_pd_obj = clinical_pd_obj[clinical_pd_obj['day'].isin(days_all)]
                clinical_pd_obj = clinical_pd_obj.drop('day', axis=1)

                # summing up the relevant columns given age and simulation iteration
                clinical_pd_obj = clinical_pd_obj.groupby(['age','iteration']).agg({'daily_total_infections': "sum",'daily_symptomatic_infections':"sum",'daily_admissions':"sum",'ward_occupancy':'sum','daily_ICU_admissions':'sum','ICU_occupancy':'sum','daily_deaths':'sum'}).reset_index()

                # preparing the columns for results for all ages:
                simplified_clinical_pd = clinical_pd_obj.groupby(['iteration']).agg({'daily_total_infections': "sum",'daily_symptomatic_infections':"sum",'daily_admissions':"sum",'ward_occupancy':'sum','daily_ICU_admissions':'sum','ICU_occupancy':'sum','daily_deaths':'sum'}).reset_index() # these should now be all ages

                simplified_clinical_pd.rename(columns = {'daily_total_infections':'total_infections_all_ages',
                                                        'daily_symptomatic_infections':'total_symptomatic_infections_all_ages',
                                                        'daily_admissions':'total_admissions_all_ages',	
                                                        'ward_occupancy':'total_ward_occupancy_all_ages',
                                                        'daily_ICU_admissions':'total_ICU_admissions_all_ages',
                                                        'ICU_occupancy':'total_ICU_occupancy_all_ages',
                                                        'daily_deaths':'total_deaths_all_ages'}, 
                                                        inplace = True)
                # print(list(simplified_clinical_pd.columns))

                # now preparing the columns for deaths by iteration and age
                deaths_only = clinical_pd_obj[['age', 'iteration','daily_deaths']]
                # print(deaths_only)
                deaths_only = pd.pivot_table(deaths_only, index=['iteration'], columns=['age'],values="daily_deaths")
                
                deaths_only.reset_index(inplace=True ) 
                column_order = ['iteration']
                for age in age_bands_clinical:
                    column_order.append(str(age))
                deaths_only.reindex(column_order, axis=1) 

                rename_dict = {age_bands_clinical[i]:"total_deaths_ages_"+age_bands_clinical_names[i] for i in range(len(age_bands_clinical_names))}

                deaths_only.rename(columns=rename_dict,inplace = True)
                
                # print(deaths_only)

                # putting everything back together
                simplified_clinical_pd =  pd.merge(simplified_clinical_pd, deaths_only, on='iteration', how='left')

                # print(simplified_clinical_pd )
                # print(list(simplified_clinical_pd.columns))
                
                iterated_clinical_DF = simplified_clinical_pd

                # dictionary index that should contain all the (relevant) information about the scenario
                dictionary_index = population_type+ " population, " + str(total_vaccination_rate*100)+"%" + " initial coverage," + 'immune escape '+str(round(immune_escape_time/one_year,2))+" years" 


                
                if boosting_group=="none":
                    dictionary_index = dictionary_index + ", (none boosting)"
                else:
                    dictionary_index = dictionary_index + ", boosting from " + str(round(vaccination_start/one_year,2))+" years"
                
                dictionary_index = dictionary_index + ", " + boosting_group_names[boosting_group] + ", " + TP_type

                print(dictionary_index)
                
                mega_DF_list_iterated[dictionary_index] = iterated_clinical_DF


    clinical_outcome_columns = [ 'total_infections_all_ages', 'total_symptomatic_infections_all_ages', 'total_admissions_all_ages', 'total_ward_occupancy_all_ages', 'total_ICU_admissions_all_ages', 'total_ICU_occupancy_all_ages', 'total_deaths_all_ages', 'total_deaths_ages_0-9', 'total_deaths_ages_10-19', 'total_deaths_ages_20-29', 'total_deaths_ages_30-39', 'total_deaths_ages_40-49', 'total_deaths_ages_50-59', 'total_deaths_ages_60-69', 'total_deaths_ages_70-79', 'total_deaths_ages_80+']


    # then for each different clinical outcome
        # make a figure
        # for each scenario
            # plot the mean (or median) of outcome as you include more and more simulations 

    starting_x = 251
    
    for clinical_outcome in clinical_outcome_columns:
        fig, ax = plt.subplots(1,1, figsize=(10,6.75))
        # legend_names = []

        plt.set_cmap('jet')

        for scenario, DF in mega_DF_list_iterated.items():
            relevant_list = DF[clinical_outcome].tolist()
            x_num_included_sims = list(range(starting_x,len(relevant_list)+1))
            x_num_main = [x/5 for x in x_num_included_sims] # this is because 5 clinical pathways sims are made per main simulation

            if mean_or_median =="mean":
                y = [np.mean(relevant_list[:x]) for x in x_num_included_sims]
                pass # use mean 
            elif mean_or_median =="median":
                y = [np.median(relevant_list[:x]) for x in x_num_included_sims]
            else:
                print("invalid mean_or_median parameter")
                exit(1)
            
            ax.plot(x_num_main,y,label = scenario)
            # legend_names.append(scenario)

        # ax.set_ylabel(mean_or_median + " of " + clinical_outcome)
        ax.set_title(mean_or_median + " of " + clinical_outcome)

        ax.set_xlabel("number of simulations included")

        ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

        days_name = "_" + str(round(days_all[0]/one_year,1))+"-"+str(round(days_all[-1]/one_year,1))+"years"

        plt.savefig(os.path.join(folder, "all_scenarios_"+ mean_or_median + "_of_"+ clinical_outcome +days_name +".png") , bbox_inches='tight')
        plt.close()
    

    # calculate the *percentage change* between the mean with x samples and the mean with x+1 samples, and plot that over time too.
    for clinical_outcome in clinical_outcome_columns:
        fig, ax = plt.subplots(1,1, figsize=(10,6.75))
        # legend_names = []

        plt.set_cmap('jet')

        for scenario, DF in mega_DF_list_iterated.items():
            relevant_list = DF[clinical_outcome].tolist()
            x_num_included_sims = list(range(starting_x,len(relevant_list)+1))
            x_num_main = [x/5 for x in x_num_included_sims] # this is because 5 clinical pathways sims are made per main simulation

            if mean_or_median =="mean":
                y = [np.mean(relevant_list[:x]) for x in x_num_included_sims]
                pass # use mean 
            elif mean_or_median =="median":
                y = [np.median(relevant_list[:x]) for x in x_num_included_sims]
            else:
                print("invalid mean_or_median parameter")
                exit(1)

            percentage_change = [np.abs(y[i+1] - y[i])/y[i]*100 if y[i]!=0 else np.abs(y[i+1] - y[i])*100  for i in range(len(y)-1)]
            
            ax.plot(x_num_main[1:],percentage_change,label = scenario)
            # legend_names.append(scenario)
        
        ax.axhline(y=1,linestyle ='dashed')

        # ax.set_ylabel(mean_or_median + " of " + clinical_outcome)
        
        ax.set_title("Absolute percentage change of " + mean_or_median + " of " + clinical_outcome)

        vals = ax.get_yticks()
        ax.set_yticklabels([str(x)+"\%" for x in vals])

        ax.set_xlabel("number of simulations included")

        ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

        days_name = "_" + str(round(days_all[0]/one_year,1))+"-"+str(round(days_all[-1]/one_year,1))+"years"

        plt.savefig(os.path.join(folder, "all_scenarios_"+ mean_or_median + "_of_"+ clinical_outcome +days_name +"_percentage_change.png") , bbox_inches='tight')
        plt.close()


    # output the sim number after which the percentage change is under the tolerance
    tolerance_percentage = 1 
    csv_file = os.path.join(folder, "all_scenarios_"+ mean_or_median + days_name +"_percentage_change_under_tolerance_"+str(tolerance_percentage)+".csv")
    header = ["scenario","clinical outcome","sim number after which percentage change is under tolerance"]
    with open(csv_file, 'w', newline='') as f:
    # create the csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)
        for clinical_outcome in clinical_outcome_columns:
            for scenario, DF in mega_DF_list_iterated.items():
                relevant_list = DF[clinical_outcome].tolist()
                x_num_included_sims = list(range(starting_x,len(relevant_list)+1))
                x_num_main = [x/5 for x in x_num_included_sims] # this is because 5 clinical pathways sims are made per main simulation

                if mean_or_median =="mean":
                    y = [np.mean(relevant_list[:x]) for x in x_num_included_sims]
                    pass # use mean 
                elif mean_or_median =="median":
                    y = [np.median(relevant_list[:x]) for x in x_num_included_sims]
                else:
                    print("invalid mean_or_median parameter")
                    exit(1)

                sim_number_under_tolerance = "not found"
                for i in reversed(range(len(y)-1)):
                    if y[i]!=0:
                        percentage_change = np.abs(y[i+1] - y[i])/y[i]*100
                    else:
                        percentage_change = np.abs(y[i+1] - y[i])*100
                    
                    if percentage_change<tolerance_percentage:
                        sim_number_under_tolerance= x_num_main[i]
                    else:
                        break # the moment we find a percentage change this is no good, we break
                

                row = [scenario,clinical_outcome,sim_number_under_tolerance]

       
                writer.writerow(row)



    # plot the difference between the mean and the median 
    if mean_or_median=="mean":
        for clinical_outcome in clinical_outcome_columns:
            fig, ax = plt.subplots(1,1, figsize=(10,6.75))
            # legend_names = []

            plt.set_cmap('jet')

            for scenario, DF in mega_DF_list_iterated.items():
                relevant_list = DF[clinical_outcome].tolist()
                x_num_included_sims = list(range(starting_x,len(relevant_list)+1))
                x_num_main = [x/5 for x in x_num_included_sims] # this is because 5 clinical pathways sims are made per main simulation

                y_mean = [np.mean(relevant_list[:x]) for x in x_num_included_sims]
                y_median = [np.median(relevant_list[:x]) for x in x_num_included_sims]
                difference = [y_mean[i] - y_median[i] for i in range(len(y_mean))]
                percentange =  [difference[i]/y_mean[i]*100 for i in range(len(y_mean))]
                
                ax.plot(x_num_main,percentange,label = scenario)
                # legend_names.append(scenario)

            ax.axhline(y=1,linestyle ='dashed')
            ax.axhline(y=-1,linestyle ='dashed')

            # ax.set_ylabel(mean_or_median + " of " + clinical_outcome)
            ax.set_title("percentage difference (mean - median)/mean of " + clinical_outcome)
            vals = ax.get_yticks()
            ax.set_yticklabels([str(x)+"\%" for x in vals])

            ax.set_xlabel("number of simulations included")

            ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

            days_name = "_" + str(round(days_all[0]/one_year,1))+"-"+str(round(days_all[-1]/one_year,1))+"years"

            plt.savefig(os.path.join(folder, "all_scenarios_difference_between_mean_and_median_of_"+ clinical_outcome +days_name +".png") , bbox_inches='tight')
            plt.close()

    

###############################################################
# running
max_days = 52*3*7
immune_escape_times = [original_program_time, original_program_time + 52*7]
param_list =  list(range(0,12+1))
days_all =  list(range(original_program_time ,max_days)) 
days_name = "_1.5-3years"

for mean_or_median in ["mean","median"]:
    for immune_escape_time in immune_escape_times:
        folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"
        presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'
        
        
        plot_clinical_outcomes_over_simulations(
            TP_list = [ "1.95"],
            TP_type_list = ['TP_high'],
            param_list =  param_list,
            population_type_list = ["older"],
            boosting_group_names =  {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'},
            presim_parameters_folder =presim_parameters_folder,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )