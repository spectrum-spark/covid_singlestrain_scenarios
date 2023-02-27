function clinical_knitting_func(broad_scenario_name, num_sims)

%broad_scenario_name='scenario1';
%num_sims = 3;

trunc_T = 800;
max_T = 900;
aug_num = 5;

day_vec = (1:ceil(max_T))-0.5;

new_symp_series=zeros(num_sims*aug_num, length(day_vec));
new_asymp_series=zeros(num_sims*aug_num, length(day_vec));
new_admission_series=zeros(num_sims*aug_num, length(day_vec));
new_ICU_series=zeros(num_sims*aug_num, length(day_vec));
ward_OCC_series=zeros(num_sims*aug_num, length(day_vec));
ICU_OCC_series=zeros(num_sims*aug_num, length(day_vec));
daily_deaths=zeros(num_sims*aug_num, length(day_vec));
daily_discharges=zeros(num_sims*aug_num, length(day_vec));


for ii=1:num_sims
    %load([broad_scenario_name,'/sim_number_',num2str(ii)]);
    %this is a workaround for the format Eamon gave me
    
    
    sim_table=readtable([broad_scenario_name,'/sim_number_',num2str(ii),'.csv'],'ReadVariableNames',true);
    load([broad_scenario_name,'/sim_number_',num2str(ii),'.mat']);
    2+2
    hosp_characteristics=individual_characteristics(hosp_indices,:);
    
    %this is a workaround for the format Eamon gave me
    num_infected=size(sim_table,1);
    %a
    
    SimIndex=ones(aug_num*num_infected,1);
    for jj=1:aug_num
        SimIndex((1+num_infected*(jj-1)):(num_infected*jj))=jj.*ones(num_infected,1);
    end
    sim_table=[table(SimIndex), repmat(sim_table,[aug_num,1])];
    
    
    
    
    [~,n_cols]=size(sim_table);
    symp_col=find(strcmp(sim_table.Properties.VariableNames,'symptomatic'));
    asymp_table = sim_table(sim_table.symptomatic==0,[1:(symp_col-1),(symp_col+1):n_cols]);
    sim_table=sim_table(sim_table.symptomatic==1,[1:(symp_col-1),(symp_col+1):n_cols]);
    
    num_sims=length(unique(individual_characteristics(:,1)));
    
    
    for jj=1:aug_num
        %number of new symptomatic cases each day
        new_symp_series((ii-1)*aug_num+jj,:) = hist(sim_table.time_symptoms(sim_table.SimIndex==jj),day_vec);
        
        % number of new asymptomatic cases each day
        new_asymp_series((ii-1)*aug_num+jj,:) = hist(asymp_table.time_symptoms(asymp_table.SimIndex==jj),day_vec);
        
        %number of new hospitalisations each day
        discretized_sim=hist(SIM_HOSP_DATA(hosp_characteristics(:,1)==jj,:),day_vec);
        
        new_admission_series((ii-1)*aug_num+jj,:)= discretized_sim(:,1);
        
        new_ICU_series((ii-1)*aug_num+jj,:) = discretized_sim(:,4);
        
        %new hosp + discharge from ICU - death/discharge from ward - discharge
        %to ICU
        ward_OCC_series((ii-1)*aug_num+jj,:) = cumsum(discretized_sim(:,1)+discretized_sim(:,6)+discretized_sim(:,7)-discretized_sim(:,2)-discretized_sim(:,3)-discretized_sim(:,4)-discretized_sim(:,8)-discretized_sim(:,9));
        
        %new to ICU - death/discharge from ICU
        ICU_OCC_series((ii-1)*aug_num+jj,:) = cumsum(discretized_sim(:,4) - discretized_sim(:,5) - discretized_sim(:,6) - discretized_sim(:,7));
        
        daily_deaths((ii-1)*aug_num+jj,:) = discretized_sim(:,3) + discretized_sim(:,5) + discretized_sim(:,8);
        
        daily_discharges((ii-1)*aug_num+jj,:) = discretized_sim(:,2) +  discretized_sim(:,9);
    end
end


all_infections=new_symp_series+new_asymp_series;

all_infections=all_infections(:,1:trunc_T);
T = array2table(all_infections);
writetable(T,[broad_scenario_name,'all_infections_.csv'])

new_symp_series=new_symp_series(:,1:trunc_T);
T = array2table(new_symp_series);
writetable(T,[broad_scenario_name,'symptomatic_infections_.csv'])

new_admission_series=new_admission_series(:,1:trunc_T);
T = array2table(new_admission_series);
writetable(T,[broad_scenario_name,'ward_admissions_.csv'])

new_ICU_series=new_ICU_series(:,1:trunc_T);
T = array2table(new_ICU_series);
writetable(T,[broad_scenario_name,'ICU_admissions_.csv'])

ward_OCC_series=ward_OCC_series(:,1:trunc_T);
T = array2table(ward_OCC_series);
writetable(T,[broad_scenario_name,'ward_occupancy_.csv'])

ICU_OCC_series=ICU_OCC_series(:,1:trunc_T);
T = array2table(ICU_OCC_series);
writetable(T,[broad_scenario_name,'ICU_occupancy_.csv'])

daily_deaths=daily_deaths(:,1:trunc_T);
T = array2table(daily_deaths);
writetable(T,[broad_scenario_name,'daily_deaths_.csv'])

daily_discharges=daily_discharges(:,1:trunc_T);
T = array2table(daily_discharges);
writetable(T,[broad_scenario_name,'daily_discharges_.csv'])

clear sim_table asymp_table individual_characteristics hosp_characteristics Admission_Status SIM_HOSP_DATA SimIndex hosp_indices all_trans_probs

save([broad_scenario_name,'outputs_full_.mat'])%,all_infections,new_symp_series,new_admission_series,new_ICU_series,ward_OCC_series,ICU_OCC_series,daily_deaths,daily_discharges)


end