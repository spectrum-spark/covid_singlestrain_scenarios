function clinical_knitting_relsev_func(broad_scenario_name,rel_sev, num_sims)

%broad_scenario_name='scenario1';
%num_sims = 3;

trunc_T = 800;
max_T = 900;
aug_num = 5;

day_vec = (1:ceil(max_T))-0.5;

new_symp_series_big=zeros(num_sims*aug_num, length(day_vec));
new_asymp_series_big=zeros(num_sims*aug_num, length(day_vec));
new_admission_series_big=zeros(num_sims*aug_num, length(day_vec));
new_ICU_series_big=zeros(num_sims*aug_num, length(day_vec));
ward_OCC_series_big=zeros(num_sims*aug_num, length(day_vec));
ICU_OCC_series_big=zeros(num_sims*aug_num, length(day_vec));
daily_deaths_big=zeros(num_sims*aug_num, length(day_vec));
daily_discharges_big=zeros(num_sims*aug_num, length(day_vec));

for ii=1:num_sims
    load([broad_scenario_name,'/sim_number_',num2str(ii),'_',num2str(rel_sev),'_discrete.mat']);
    %this is a workaround for the format Eamon gave me
    
    
    
    
    
    %number of new symptomatic cases each day
    new_symp_series_big(((ii-1)*aug_num+1):(ii*aug_num),:) =  new_symp_series;
    
    % number of new asymptomatic cases each day
    new_asymp_series_big(((ii-1)*aug_num+1):(ii*aug_num),:) = new_asymp_series;
    %number of new hospitalisations each day
    
    new_admission_series_big(((ii-1)*aug_num+1):(ii*aug_num),:)= new_admission_series;
    
    new_ICU_series_big(((ii-1)*aug_num+1):(ii*aug_num),:) = new_ICU_series;
    
    %new hosp + discharge from ICU - death/discharge from ward - discharge
    %to ICU
    ward_OCC_series_big(((ii-1)*aug_num+1):(ii*aug_num),:) = ward_OCC_series;
    
    %new to ICU - death/discharge from ICU
    ICU_OCC_series_big(((ii-1)*aug_num+1):(ii*aug_num),:) =  ICU_OCC_series;
    
    daily_deaths_big(((ii-1)*aug_num+1):(ii*aug_num),:) = daily_deaths;
    
    daily_discharges_big(((ii-1)*aug_num+1):(ii*aug_num),:) = daily_discharges;
    
end


all_infections_big=new_symp_series_big+new_asymp_series_big;
% 
% all_infections=all_infections(:,1:trunc_T);
% T = array2table(all_infections);
% writetable(T,['all_infections_',broad_scenario_name,'.csv'])
% 
% new_symp_series=new_symp_series(:,1:trunc_T);
% T = array2table(new_symp_series);
% writetable(T,['symptomatic_infections_',broad_scenario_name,'.csv'])
% 
% new_admission_series=new_admission_series(:,1:trunc_T);
% T = array2table(new_admission_series);
% writetable(T,['ward_admissions_',broad_scenario_name,'.csv'])
% 
% new_ICU_series=new_ICU_series(:,1:trunc_T);
% T = array2table(new_ICU_series);
% writetable(T,['ICU_admissions_',broad_scenario_name,'.csv'])
% 
% ward_OCC_series=ward_OCC_series(:,1:trunc_T);
% T = array2table(ward_OCC_series);
% writetable(T,['ward_occupancy_',broad_scenario_name,'.csv'])
% 
% ICU_OCC_series=ICU_OCC_series(:,1:trunc_T);
% T = array2table(ICU_OCC_series);
% writetable(T,['ICU_occupancy_',broad_scenario_name,'.csv'])
% 
% daily_deaths=daily_deaths(:,1:trunc_T);
% T = array2table(daily_deaths);
% writetable(T,['daily_deaths_',broad_scenario_name,'.csv'])
% 
% daily_discharges=daily_discharges(:,1:trunc_T);
% T = array2table(daily_discharges);
% writetable(T,['daily_discharges_',broad_scenario_name,'.csv'])
% 
% clear sim_table asymp_table individual_characteristics hosp_characteristics Admission_Status SIM_HOSP_DATA SimIndex hosp_indices all_trans_probs

%save(['outputs_full_',broad_scenario_name,'.mat'])%,all_infections,new_symp_series,new_admission_series,new_ICU_series,ward_OCC_series,ICU_OCC_series,daily_deaths,daily_discharges)

save([broad_scenario_name,'_',num2str(rel_sev),'_full.mat'],'all_infections_big','new_symp_series_big','new_asymp_series_big','new_admission_series_big','new_ICU_series_big','ward_OCC_series_big','ICU_OCC_series_big','daily_deaths_big','daily_discharges_big','day_vec')

end
