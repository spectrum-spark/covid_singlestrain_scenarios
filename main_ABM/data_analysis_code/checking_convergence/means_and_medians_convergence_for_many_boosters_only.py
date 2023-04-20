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
import random


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


def create_mega_data_frame(
        TP_list = ["1.05", "1.95"],
        TP_type_list = ['TP_low','TP_high'],
        population_type_list = ["younger","older"],
        immune_escape_time = 0,
        days_all = list(range(0,100)),
        folder = '/scratch/cm37/tpl/', # need to put immune escape times
        ):
    mega_DF_list_iterated = dict()

    # for different sub-scenarios (TPs, population type, and param nums), gather the clinical outcomes into a huge dataframe 
    for TP_type, TP_val in zip(TP_type_list,TP_list):
        for population_type in population_type_list:

            # load in clinical data file
            filename = "abm_continuous_simulation_parameters_"+population_type+"_SOCRATES_TP"+TP_val

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
            dictionary_index = population_type+ " population, " + 'immune escape '+str(round(immune_escape_time/one_year,2))+" years" 

            
            dictionary_index = dictionary_index + ", " + TP_type

            print(dictionary_index)
            
            mega_DF_list_iterated[dictionary_index] = iterated_clinical_DF

    return mega_DF_list_iterated

def plot_mean_or_median(mega_DF_list_iterated,starting_x = 251,
        clinical_outcome_columns =  [ 'total_infections_all_ages', 'total_symptomatic_infections_all_ages', 'total_admissions_all_ages', 'total_ward_occupancy_all_ages', 'total_ICU_admissions_all_ages', 'total_ICU_occupancy_all_ages', 'total_deaths_all_ages', 'total_deaths_ages_0-9', 'total_deaths_ages_10-19', 'total_deaths_ages_20-29', 'total_deaths_ages_30-39', 'total_deaths_ages_40-49', 'total_deaths_ages_50-59', 'total_deaths_ages_60-69', 'total_deaths_ages_70-79', 'total_deaths_ages_80+'],
        folder = '/scratch/cm37/tpl/', # need to put immune escape times
        days_all = list(range(0,100)),
        days_name = "100_days",
        mean_or_median = "mean",
        random_shuffle = False):
    
    for clinical_outcome in clinical_outcome_columns:
        fig, (ax,ax2) = plt.subplots(1,2, figsize=(14,6.75))
        # legend_names = []

        plt.set_cmap('jet')

        for scenario, DF in mega_DF_list_iterated.items():
            relevant_list = DF[clinical_outcome].tolist()
            if random_shuffle:
                random.shuffle(relevant_list)

            x_num_included_sims = list(range(starting_x,len(relevant_list)+1))
            x_num_main = [x/5 for x in x_num_included_sims] # this is because 5 clinical pathways sims are made per main simulation

            if mean_or_median =="mean":
                y = [np.mean(relevant_list[:x]) for x in x_num_included_sims]
                final_mean_or_median = np.mean(relevant_list)
            elif mean_or_median =="median":
                y = [np.median(relevant_list[:x]) for x in x_num_included_sims]
                final_mean_or_median = np.median(relevant_list)

            else:
                print("invalid mean_or_median parameter")
                exit(1)
            
            ax.plot(x_num_main,y,label = scenario)
            # legend_names.append(scenario)

            # calculate the *percentage change* between the mean with x samples and the mean with x+1 samples, and plot that over time too.
            percentage_change = [np.abs(y[i] - final_mean_or_median)/final_mean_or_median if final_mean_or_median!=0 else np.abs(y[i] - final_mean_or_median)  for i in range(len(y))]
            
            ax2.plot(x_num_main,percentage_change,label = scenario)
        

        # formatting the first subplot
        # ax.set_ylabel(mean_or_median + " of " + clinical_outcome)
        ax.set_title(mean_or_median + " of " + clinical_outcome)
        ax.grid()
        ax.set_xlabel("number of simulations included")
        if random_shuffle:
            ax.set_xlabel("number of simulations included (random shuffle)")

        # ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

          
        # formatting the second subplot
        ax2.axhline(y=0.01,linestyle ='dashed')
        ax2.grid()
        # ax.set_ylabel(mean_or_median + " of " + clinical_outcome)
        ax2.set_title("Absolute percentage change of " + mean_or_median + " of " + clinical_outcome)
        vals = ax2.get_yticks()
        ax2.set_yticklabels([str(round(y*100,2)) + "\%" for y in vals])
        ax2.set_xlabel("number of simulations included")
        # ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

        days_name = "_" + str(round(days_all[0]/one_year,1))+"-"+str(round(days_all[-1]/one_year,1))+"years"

        if not random_shuffle:
            plt.savefig(os.path.join(folder, "all_scenarios_"+ mean_or_median + "_of_"+ clinical_outcome +days_name +"_with_percentage_change.png") , bbox_inches='tight')
        else:
            plt.savefig(os.path.join(folder, "all_scenarios_"+ mean_or_median + "_of_"+ clinical_outcome +days_name +"_with_percentage_change_different_order.png") , bbox_inches='tight')
        plt.close()


def plot_clinical_outcomes_over_simulations(
        TP_list = ["1.05", "1.95"],
        TP_type_list = ['TP_low','TP_high'],
        population_type_list = ["younger","older"],
        immune_escape_time = 0,
        folder = '/scratch/cm37/tpl/', # need to put immune escape times
        days_all = list(range(0,100)),
        days_name = "100_days",
        mean_or_median = "mean",
        ):

    mega_DF_list_iterated = create_mega_data_frame(
        TP_list = TP_list,
        TP_type_list = TP_type_list ,
        population_type_list =  population_type_list,
        folder =folder, 
        days_all = days_all)
    

    clinical_outcome_columns = [ 'total_infections_all_ages', 'total_symptomatic_infections_all_ages', 'total_admissions_all_ages', 'total_ward_occupancy_all_ages', 'total_ICU_admissions_all_ages', 'total_ICU_occupancy_all_ages', 'total_deaths_all_ages', 'total_deaths_ages_0-9', 'total_deaths_ages_10-19', 'total_deaths_ages_20-29', 'total_deaths_ages_30-39', 'total_deaths_ages_40-49', 'total_deaths_ages_50-59', 'total_deaths_ages_60-69', 'total_deaths_ages_70-79', 'total_deaths_ages_80+']

    
    # then for each different clinical outcome
        # make a figure
        # for each scenario
            # plot the mean (or median) of outcome as you include more and more simulations 

    starting_x = 1

    plot_mean_or_median(mega_DF_list_iterated,
        starting_x = starting_x ,
        clinical_outcome_columns = clinical_outcome_columns ,
        folder =folder ,
        days_all =days_all,
        days_name = days_name ,
        mean_or_median =  mean_or_median,
        random_shuffle = False )
    
    # # DIFFERENT ORDER - random shuffle
    # plot_mean_or_median(mega_DF_list_iterated,
    #     starting_x = starting_x ,
    #     clinical_outcome_columns = clinical_outcome_columns ,
    #     folder =folder ,
    #     days_all =days_all,
    #     days_name = days_name ,
    #     mean_or_median =  mean_or_median,
    #     random_shuffle = True )
    


    clinical_outcome_columns = [ 'total_infections_all_ages']
    # plotting the individual results instead + histogram
    if mean_or_median=="mean":
        for clinical_outcome in clinical_outcome_columns:
            num_scenarios = len(mega_DF_list_iterated)
            fig, axs = plt.subplots(num_scenarios,2, figsize=(14,5*num_scenarios))
            # legend_names = []

            plt.set_cmap('jet')
            ax_count = 0

            for scenario, DF in mega_DF_list_iterated.items():
                relevant_list = DF[clinical_outcome].tolist()
                x_num_main = [x/5 for x in list(range(1,len(relevant_list)+1))] # this is because 5 clinical pathways sims are made per main simulation

                axs[ax_count,0].scatter(x_num_main,relevant_list,label = scenario)
                # legend_names.append(scenario)

                # then for the histogram
                axs[ax_count,1].hist(relevant_list,bins=20, alpha=0.5,histtype='bar',label = scenario) #  histtype='step'

                
            

                # formatting the first subplot
                # ax.set_ylabel(mean_or_median + " of " + clinical_outcome)
                axs[ax_count,0].set_title(clinical_outcome + " in different simulations")
                axs[ax_count,0].grid()
                axs[ax_count,0].set_xlabel("simulation number")
                # ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

                
                # formatting the second subplot
                axs[ax_count,1].grid()
                axs[ax_count,1].set_title("Histogram of " + clinical_outcome)
                axs[ax_count,1].set_xlabel(clinical_outcome)
                # ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

                ax_count +=1

            days_name = "_" + str(round(days_all[0]/one_year,1))+"-"+str(round(days_all[-1]/one_year,1))+"years"


            plt.savefig(os.path.join(folder, "all_scenarios_"+ clinical_outcome +days_name +"_per_sim_and_hist.png") , bbox_inches='tight')
            plt.close()

    # # output the sim number after which the percentage change is under the tolerance
    # tolerance_percentage = 0.01 
    # csv_file = os.path.join(folder, "all_scenarios_"+ mean_or_median + days_name +"_percentage_change_under_tolerance_"+str(tolerance_percentage)+".csv")
    # header = ["scenario","clinical outcome","sim number after which percentage change is under tolerance"]
    # with open(csv_file, 'w', newline='') as f:
    # # create the csv writer
    #     writer = csv.writer(f)

    #     # write the header
    #     writer.writerow(header)
    #     for clinical_outcome in clinical_outcome_columns:
    #         for scenario, DF in mega_DF_list_iterated.items():
    #             relevant_list = DF[clinical_outcome].tolist()
    #             x_num_included_sims = list(range(starting_x,len(relevant_list)+1))
    #             x_num_main = [x/5 for x in x_num_included_sims] # this is because 5 clinical pathways sims are made per main simulation

    #             if mean_or_median =="mean":
    #                 y = [np.mean(relevant_list[:x]) for x in x_num_included_sims]
    #                 final_mean_or_median = np.mean(relevant_list)
    #             elif mean_or_median =="median":
    #                 y = [np.median(relevant_list[:x]) for x in x_num_included_sims]
    #                 final_mean_or_median = np.median(relevant_list)

    #             else:
    #                 print("invalid mean_or_median parameter")
    #                 exit(1)

                 

    #             sim_number_under_tolerance = "not found"
    #             for i in reversed(range(len(y))):
    #                 if final_mean_or_median!=0:
    #                     percentage_change = np.abs(y[i] - final_mean_or_median)/final_mean_or_median
    #                 else:
    #                     percentage_change = np.abs(y[i] - final_mean_or_median)
                    
    #                 if percentage_change<tolerance_percentage:
    #                     sim_number_under_tolerance= x_num_main[i]
    #                 else:
    #                     break # the moment we find a percentage change this is no good, we break
                
    #             row = [scenario,clinical_outcome,sim_number_under_tolerance]

       
    #             writer.writerow(row)



    # # plot the difference between the mean and the median 
    # if mean_or_median=="mean":
    #     for clinical_outcome in clinical_outcome_columns:
    #         fig, ax = plt.subplots(1,1, figsize=(10,6.75))
    #         # legend_names = []

    #         plt.set_cmap('jet')

    #         for scenario, DF in mega_DF_list_iterated.items():
    #             relevant_list = DF[clinical_outcome].tolist()
    #             x_num_included_sims = list(range(starting_x,len(relevant_list)+1))
    #             x_num_main = [x/5 for x in x_num_included_sims] # this is because 5 clinical pathways sims are made per main simulation

    #             y_mean = [np.mean(relevant_list[:x]) for x in x_num_included_sims]
    #             y_median = [np.median(relevant_list[:x]) for x in x_num_included_sims]
    #             difference = [y_mean[i] - y_median[i] for i in range(len(y_mean))]
    #             percentange =  [difference[i]/y_mean[i]*100 for i in range(len(y_mean))]
                
    #             ax.plot(x_num_main,percentange,label = scenario)
    #             # legend_names.append(scenario)

    #         ax.axhline(y=1,linestyle ='dashed')
    #         ax.axhline(y=-1,linestyle ='dashed')

    #         ax.grid()

    #         # ax.set_ylabel(mean_or_median + " of " + clinical_outcome)
    #         ax.set_title("percentage difference (mean - median)/mean of " + clinical_outcome)
    #         vals = ax.get_yticks()
    #         ax.set_yticklabels([str(x)+"\%" for x in vals])

    #         ax.set_xlabel("number of simulations included")

    #         ax.legend(bbox_to_anchor=(1.01,0), loc="lower left",borderaxespad=0,frameon=False)

    #         days_name = "_" + str(round(days_all[0]/one_year,1))+"-"+str(round(days_all[-1]/one_year,1))+"years"

    #         plt.savefig(os.path.join(folder, "all_scenarios_difference_between_mean_and_median_of_"+ clinical_outcome +days_name +".png") , bbox_inches='tight')
    #         plt.close()

    