sev_mat=[0.6,1/5,1/15];


% for simnum = 12:20
%     for params = 1:12
%         filename = strcat('C:/Users/thaophuongl/winter_outputs/abm_simulation_people_params_',num2str(params),'_output_winter_sims_younger_init10/sim_number_', num2str(simnum));
%         clinical_pathways_immunity_relsev2_func('NSW',filename,sev_mat,1)
%     end
% 
%     for params = 13:24
%         filename = strcat('C:/Users/thaophuongl/winter_outputs/abm_simulation_people_params_',num2str(params),'_output_winter_sims_older_init10/sim_number_', num2str(simnum));
%         clinical_pathways_immunity_relsev2_func('NSW',filename,sev_mat,1)
%     end
% 
% end


for params = 7:12
    params
    filename = strcat('C:/Users/thaophuongl/winter_outputs/abm_simulation_people_params_',num2str(params),'_output_winter_sims_younger_init10/');
    clinical_knitting_relsev_func(filename,sev_mat,20);
    
    combined_output_plotter2(filename,sev_mat,'k');
    plotting_filename = strcat('C:/Users/thaophuongl/winter_outputs/abm_simulation_people_params_',num2str(params),'_output_younger_sims_older_init10_clinical_pathways.png');
    saveas(gcf, plotting_filename);
    pause(2)
    clf;
    pause(2)
end

for params = 13:24
    params
    filename = strcat('C:/Users/thaophuongl/winter_outputs/abm_simulation_people_params_',num2str(params),'_output_winter_sims_older_init10/');
    clinical_knitting_relsev_func(filename,sev_mat,20);
    
    combined_output_plotter2(filename,sev_mat,'k');
    plotting_filename = strcat('C:/Users/thaophuongl/winter_outputs/abm_simulation_people_params_',num2str(params),'_output_winter_sims_older_init10_clinical_pathways.png');
    saveas(gcf, plotting_filename);
    pause(2)
    clf;
    pause(2)
end


