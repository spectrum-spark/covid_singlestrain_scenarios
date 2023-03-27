from means_and_medians_convergence import *

###############################################################
# running
max_days = 52*3*7
immune_escape_times = [original_program_time + 26*7]
param_list = list(range(0,7+1))
days_all =  list(range(original_program_time ,max_days)) 
days_name = "_1.5-3years"

for mean_or_median in ["median"]:#,"mean",]:
    for immune_escape_time in immune_escape_times:
        folder = "/scratch/cm37/tpl/annual_boosting_age_scenarios_immune_escape_t" + str(immune_escape_time) +"_outputs/"
        presim_parameters_folder  = '/fs04/cm37/prod/Le/WHO/covid-abm-presim/parameter_files_annual_boosting_age_scenarios/'
        
        
        plot_clinical_outcomes_over_simulations(
            TP_list = [ "1.05", "1.95"],
            TP_type_list = [ 'TP_low','TP_high'],
            param_list =  param_list,
            population_type_list = ["older","younger"],
            boosting_group_names = {'none':'no further boosting', '65+': 'boosting 65+','55+':'boosting 55+','45+':'boosting 45+','35+':'boosting 35+','25+':'boosting 25+','16+':'boosting 16+','5+':'boosting 5+'},
            immune_escape_time = immune_escape_time,
            presim_parameters_folder =presim_parameters_folder,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )
        
