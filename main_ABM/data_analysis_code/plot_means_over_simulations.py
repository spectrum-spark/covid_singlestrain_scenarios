from means_and_medians_convergence import *

###############################################################
# running
max_days = 52*3*7
immune_escape_times = [original_program_time, original_program_time + 13*7, original_program_time + 26*7  , original_program_time + 39*7 , original_program_time + 52*7] 
immune_escape_times = [original_program_time, 819] 
param_list =  list(range(0,12+1))  #  [0,4,5,6]
days_all =  list(range(original_program_time ,max_days)) 
days_name = "_1.5-3years"


for mean_or_median in ["mean"]:#,"median"]:
    for immune_escape_time in immune_escape_times:
        folder = "/scratch/cm37/tpl/annual_boosting_1_immune_escape_t" + str(immune_escape_time) +"_outputs/"
        presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_1/'
        
        
        plot_clinical_outcomes_over_simulations(
            TP_list = [ "1.95"],
            TP_type_list = ['TP_high'],
            param_list =  param_list,
            population_type_list = ["older"],
            boosting_group_names =  {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'},
            immune_escape_time = immune_escape_time,
            presim_parameters_folder =presim_parameters_folder,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )
        
        plot_clinical_outcomes_over_simulations(
            TP_list = [ "1.95"],
            TP_type_list = ['TP_high'],
            param_list =  param_list,
            population_type_list = ["younger"],
            boosting_group_names =  {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'},
            immune_escape_time = immune_escape_time,
            presim_parameters_folder =presim_parameters_folder,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )
        
        plot_clinical_outcomes_over_simulations(
            TP_list = [ "1.05"],
            TP_type_list = ['TP_high'],
            param_list =  param_list,
            population_type_list = ["older"],
            boosting_group_names =  {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'},
            immune_escape_time = immune_escape_time,
            presim_parameters_folder =presim_parameters_folder,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )
        
        plot_clinical_outcomes_over_simulations(
            TP_list = [ "1.05"],
            TP_type_list = ['TP_high'],
            param_list =  param_list,
            population_type_list = ["younger"],
            boosting_group_names =  {'none':'no further boosting', '5-15': 'further boosting pediatric','65+':'further boosting high risk','random':'further boosting random'},
            immune_escape_time = immune_escape_time,
            presim_parameters_folder =presim_parameters_folder,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )