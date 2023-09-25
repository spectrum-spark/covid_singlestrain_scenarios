#!/bin/sh

START=$(date "+%s")
NUM_SIMS=2 # CHANGE THIS APPROPRIATELY, 1000 originally

# First, run the individual simulations and clinical outcomes:
for POP in older younger # population demographic
do
    for BA45start in 546 910 # time when immune escape variant emerges (1.5 years, 2.5 years). Note that the complete set of times are 546 637 728 819 910
    do

        for TPvers in 1 #1 for high TP (results in main paper)
        do

            for (( i=1; i<=$NUM_SIMS; i++ ))
            do
                ./Run_BA1s_BA45s_cont_intros_many_boosters updated_omicron_parameters/omicron_May_2022_updates.json updated_omicron_parameters/transmission_escape_params.json simulation_params/annual_boosting_2_immune_escape_t${BA45start}/sim_params_${POP}_${TPvers}.json $i ../presim_code/parameter_files_annual_boosting_2 abm_continuous_simulation_parameters_${POP}


                matlab -batch "cd '../clinical_pathways';disp(pwd);sev_mat = [1/15,1/45,1/60];TP_list = {'1.95'};TP = TP_list{${TPvers}};disp(TP);population = '${POP}';disp(population);simnum='${i}';disp(simnum);BA45wavestart = '${BA45start}';foldername = strcat('../outputs/annual_boosting_2_immune_escape_t',BA45wavestart,'/');disp(foldername);filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',params,'_SOCRATES_TP',TP,'/sim_number_',simnum);disp(filename);clinical_pathways_immunity_relsev3_func('NSW',filename,sev_mat);disp('done?');quit()"

            done

            # Then, run the code to combine individual simulation files

            matlab -batch "cd '../clinical_pathways';disp(pwd);sev_mat = [1/15,1/45,1/60];numsims=${NUM_SIMS};TP_list = {'1.95'};TP = TP_list{${TPvers}};disp(TP);population = '${POP}';disp(population);BA45wavestart = '${BA45start}';foldername = strcat('../outputs/annual_boosting_2_immune_escape_t',BA45wavestart,'/');filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',params,'_SOCRATES_TP',TP,'/');disp(filename);clinical_knitting_relsev_func(filename,sev_mat,numsims);disp('done?');quit()"

            Rscript compress_outputs_continuous_reduced.R ../outputs/annual_boosting_2_immune_escape_t${BA45start}/ abm_continuous_simulation_parameters_${POP}_${diffparams}_SOCRATES_TP 2

        done


    done
done


# Then, plotting and creating suitable outputs for the cost-effectiveness analysis

python data_analysis_code/checking_convergence/plot_means_over_simulations_annual_boosting_2.py # for checking convergence

python data_analysis_code/plot_figures/plot_infections_annual_boosting_2.py # for plots (general)

python data_analysis_code/plot_figures/plot_main_manuscript_figure_4.py # for plots in the paper 

python data_analysis_code/output_clinical_outcomes/output_clinical_outcomes_annual_boosting_2.py # to produce outputs needed to feed into the cost-effectiveness analysis
python data_analysis_code/output_clinical_outcomes/output_clinical_outcomes_annual_boosting_2_median.py 

python data_analysis_code/output_clinical_outcomes/output_clinical_outcomes_annual_boosting_2_quantiles.py 



END=$(date "+%s")
echo -e "\n"
echo "ran in $((END-START)) seconds"
