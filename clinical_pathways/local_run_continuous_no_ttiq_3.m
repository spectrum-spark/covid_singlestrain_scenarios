% sev_mat=[0.6,1/5,1/15];
sev_mat = [1/15,1/45,1/60]; % new one

population_type = {'younger','older'};


% TP_list = {'0.95','1.0','1.05', '1.1','1.15', '1.2000000000000002','1.25', '1.3','1.35', '1.4', '1.45','1.5','1.55','1.6','1.65','1.7','1.75','1.8','1.85','1.9','1.95'};
TP_list = {'0.85','0.9','0.95','1.0','1.05', '1.1','1.15', '1.2','1.25', '1.3','1.35', '1.4', '1.45','1.5','1.55','1.6','1.65','1.7','1.75','1.8','1.85','1.9','1.95','2.0','2.05'};

numsims = 5;

for p = 1:2
    population = population_type{p};
    for TP_i = 1:length(TP_list)
        TP = TP_list{TP_i};
        for params = 1:6
            disp(population)
            disp(TP_i)
            disp(params)

            %foldername = 'C:/Users/thaophuongl/covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_no_vax_outputs/';
            foldername = 'C:/Users/thaophuongl/covid_continuous_simulations_double_exposure_no_ttiq_450-2_ibm_4th_doses_rerun_outputs/';
            mainfilename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',num2str(params),'_SOCRATES_TP',TP,'/_0.066667    0.022222    0.016667_full.mat');
            
            if isfile(mainfilename)
                continue
            end

            for simnum = 1:numsims
                filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',num2str(params),'_SOCRATES_TP',TP,'/sim_number_', num2str(simnum));
                clinical_pathways_immunity_relsev3_func('NSW',filename,sev_mat);
            end

            filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',num2str(params),'_SOCRATES_TP',TP,'/');
            clinical_knitting_relsev_func(filename,sev_mat,numsims);
        end
    end
end

% 
% for params = 7:12
%     combined_output_plotter2(filename,sev_mat,'k');
%     plotting_filename = strcat('C:/Users/thaophuongl/winter_outputs/abm_simulation_people_params_',num2str(params),'_output_younger_sims_older_init10_clinical_pathways.png');
%     saveas(gcf, plotting_filename);
%     pause(2)
%     clf;
%     pause(2)
% end



