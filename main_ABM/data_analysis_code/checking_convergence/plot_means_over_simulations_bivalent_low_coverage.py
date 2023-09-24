from means_and_medians_convergence import *

###############################################################
# running
max_days = 52*3*7
immune_escape_times = [728]
param_list = [2,5]#  list(range(0,12+1))
days_all =  list(range(original_program_time ,max_days)) 
days_name = "_1.5-3years"


for mean_or_median in ["mean"]:#,"median"]:
    for immune_escape_time in immune_escape_times:
        bivalent_start_time = immune_escape_time
        
        folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "outputs", "bivalent_boosting","low_coverage_immune_escape_t" + str(immune_escape_time) +"_bivalent_t"+str(bivalent_start_time)))
        
        presim_parameters_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..","..", "presim_code","parameter_files_annual_boosting_1_younger"))
        
        
        plot_clinical_outcomes_over_simulations(
            TP_list = ["1.05", "1.95"],
            TP_type_list = ['TP_low','TP_high'],
            param_list =  param_list,
            population_type_list = ["younger"],
            boosting_group_names =  {'none':'no further vaccination', '5-15': 'further primary vaccination pediatric','65+':'further boosting high risk','primary':'further primary vaccination random'},
            immune_escape_time = immune_escape_time,
            presim_parameters_folder =presim_parameters_folder,
            folder = folder,
            days_all = days_all,
            days_name = days_name,
            mean_or_median = mean_or_median ,
            )