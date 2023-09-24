from means_and_medians_convergence_for_many_boosters_only import *

###############################################################
# running
max_days = 52*3*7
immune_escape_times = [original_program_time, original_program_time + 52*7]
days_all =  list(range(original_program_time ,max_days)) 
days_name = "_1.5-3years"


for mean_or_median in ["mean"]:#,"median"]:
    for immune_escape_time in immune_escape_times:
        folder =  os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs","annual_boosting_2_immune_escape_t" + str(immune_escape_time)))
        
        presim_parameters_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "presim_code","parameter_files_annual_boosting_1"))
        
        
        plot_clinical_outcomes_over_simulations(
            TP_list = [ "1.95"],
            TP_type_list = ['TP_high'],
            population_type_list = ["older","younger"],
            immune_escape_time = immune_escape_time,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )
        
        