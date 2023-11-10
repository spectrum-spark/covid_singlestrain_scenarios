#!/bin/sh

START=$(date "+%s")
NUM_SIMS=2 # CHANGE THIS APPROPRIATELY, 1000 originally

# First, run the individual simulations and clinical outcomes:
for POP in younger # younger population demographic only
do
    for BA45start in 728 # time when immune escape variant emerges (2 years). Note that the complete set of times are 546 637 728 819 910
    do

        for BIVALENTSTART in 728
        do


            for diffparams in 2 5 # different boosting times and allocations
            do

                for TPvers in 1 2 #1 for low TP, 2 for high TP
                do

                    for (( i=1; i<=$NUM_SIMS; i++ ))
                    do

                        ./Run_BA1s_BA45s_bivalent_cont_intros updated_omicron_parameters/omicron_May_2022_updates_with_bivalent.json updated_omicron_parameters/transmission_escape_params_with_bivalent.json simulation_params/bivalent_boosting_jsons/low_coverage_immune_escape_t${BA45start}_bivalent_t${bivalent}/sim_params_${POP}_${TPvers}.json $i ../presim_code/parameter_files_annual_boosting_1_younger abm_continuous_simulation_parameters_${POP}_${diffparams}


                        matlab -batch "cd '../clinical_pathways';disp(pwd);sev_mat = [1/15,1/45,1/60];TP_list = {'1.05','1.95'};TP = TP_list{${TPvers}};disp(TP);population = '${POP}';disp(population);params = '${diffparams}';disp(params);simnum='${i}';disp(simnum);BA45wavestart = '${BA45start}';bivalent = '${bivalent}';foldername = strcat('../outputs/bivalent_boosting/low_coverage_immune_escape_t',BA45wavestart,'_bivalent_t',bivalent,'/');disp(foldername);filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',params,'_SOCRATES_TP',TP,'/sim_number_',simnum);disp(filename);clinical_pathways_immunity_relsev3_func('NSW',filename,sev_mat);disp('done?');quit()"

                    done

                    # Then, run the code to combine individual simulation files

                    matlab -batch "cd '../clinical_pathways';disp(pwd);sev_mat = [1/15,1/45,1/60];numsims=${NUM_SIMS};TP_list = {'1.05','1.95'};TP = TP_list{${TPvers}};disp(TP);population = '${POP}';disp(population);params = '${diffparams}';disp(params);BA45wavestart = '${BA45start}';bivalent = '${bivalent}';foldername = strcat('../outputs/bivalent_boosting/low_coverage_immune_escape_t',BA45wavestart,'_bivalent_t',bivalent,'/');filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',params,'_SOCRATES_TP',TP,'/');disp(filename);clinical_knitting_relsev_func(filename,sev_mat,numsims);disp('done?');quit()"

                    Rscript compress_outputs_continuous_reduced.R ../outputs/bivalent_boosting/low_coverage_immune_escape_t${BA45start}_bivalent_t_${bivalent}/ abm_continuous_simulation_parameters_${POP}_${diffparams}_SOCRATES_TP ${TPvers}

                done

            done
        done

    done
done


# Then, plotting and creating suitable outputs for the cost-effectiveness analysis

python data_analysis_code/checking_convergence/plot_means_over_simulations_bivalent_low_coverage.py # for checking convergence

python data_analysis_code/plot_figures/python plot_infections_annual_boosting_bivalent_low_coverage_comparisons.py # for plots (general)

python data_analysis_code/output_clinical_outcomes/output_clinical_outcomes_bivalent_boosting.py
 # to produce outputs needed to feed into the cost-effectiveness analysis



END=$(date "+%s")
echo -e "\n"
echo "ran in $((END-START)) seconds"
