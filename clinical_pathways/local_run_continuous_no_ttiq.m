sev_mat=[0.6,1/5,1/15];

% TP_list = {'0.95','1.0','1.05', '1.1','1.15', '1.2000000000000002','1.25', '1.3','1.35', '1.4', '1.45','1.5','1.55','1.6','1.65'};
TP_list = {'0.8','0.9','1.0', '1.1', '1.2000000000000002', '1.3', '1.4','1.5','1.6'};

population_type = {'younger','older'};

for p = 1:2
    population = population_type{p};
    for simnum = 1:5
        for params = 1:6
            for TP_i = 9 % 1:length(TP_list)
                TP = TP_list{TP_i};
                foldername = 'C:/Users/thaophuongl/covid_continuous_simulations_double_exposure_no_ttiq_450-2_outputs/';
                filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',num2str(params),'_SOCRATES_TP',TP,'/sim_number_', num2str(simnum));
                clinical_pathways_immunity_relsev2_func('NSW',filename,sev_mat,1)
            end
        end
    
    
    end
end


for p = 1:2
    population = population_type{p};
    for params = 1:6
        for TP_i = 1:length(TP_list)
            TP = TP_list{TP_i};
            foldername = 'C:/Users/thaophuongl/covid_continuous_simulations_double_exposure_no_ttiq_450-2_outputs/';
            filename = strcat(foldername,'abm_continuous_simulation_parameters_',population,'_',num2str(params),'_SOCRATES_TP',TP,'/');
            clinical_knitting_relsev_func(filename,sev_mat,5);
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



