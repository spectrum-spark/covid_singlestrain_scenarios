sev_mat=[0.6,1/5,1/15];

% for simnum = 1:50
%     clinical_pathways_immunity_relsev2_func('NSW',strcat('C:/Users/thaophuongl/covid-abm/winter_wave_scenarios/initial-and-during_vax_infect_scenario1_older_sim_params_v1/sim_number_', num2str(simnum)),sev_mat,1)
% end
% 
% clinical_knitting_relsev_func('C:/Users/thaophuongl/covid-abm/winter_wave_scenarios/initial-and-during_vax_infect_scenario1_older_sim_params_v1/',sev_mat,50)

combined_output_plotter2('C:/Users/thaophuongl/covid-abm/winter_wave_scenarios/initial-and-during_vax_infect_scenario1_older_sim_params_v1/',sev_mat,'k');

saveas(gcf,'C:/Users/thaophuongl/covid-abm/winter_wave_scenarios/initial-and-during_vax_infect_scenario1_older_sim_params_v1_clinical_pathways.png')
