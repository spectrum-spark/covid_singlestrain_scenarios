
scenario_name = 'Example';

sim_table=readtable([scenario_name,'.csv'],'ReadVariableNames',true);
load(['clinical_pathwane_',scenario_name,'.mat'])

hosp_characteristics=individual_characteristics(hosp_indices,:);

%this is a workaround for the format Eamon gave me
num_infected=size(sim_table,1);
%a
aug_num = 5;
SimIndex=ones(aug_num*num_infected,1);
for ii=1:aug_num
    SimIndex((1+num_infected*(ii-1)):(num_infected*ii))=ii.*ones(num_infected,1);
end
sim_table=[table(SimIndex), repmat(sim_table,[aug_num,1])];




[~,n_cols]=size(sim_table);
symp_col=find(strcmp(sim_table.Properties.VariableNames,'symptomatic'));
asymp_table = sim_table(sim_table.symptomatic==0,[1:(symp_col-1),(symp_col+1):n_cols]);
sim_table=sim_table(sim_table.symptomatic==1,[1:(symp_col-1),(symp_col+1):n_cols]);

num_sims=length(unique(individual_characteristics(:,1)));

max_T = max(SIM_HOSP_DATA(:));

day_vec = (1:ceil(max_T))-0.5;

new_symp_series=zeros(num_sims, length(day_vec));
new_asymp_series=zeros(num_sims, length(day_vec));
new_admission_series=zeros(num_sims, length(day_vec));
new_ICU_series=zeros(num_sims, length(day_vec));
ward_OCC_series=zeros(num_sims, length(day_vec));
ICU_OCC_series=zeros(num_sims, length(day_vec));
daily_deaths=zeros(num_sims, length(day_vec));
daily_discharges=zeros(num_sims, length(day_vec));
for ii=1:num_sims
    %number of new symptomatic cases each day
    new_symp_series(ii,:) = hist(sim_table.time_symptoms(sim_table.SimIndex==ii),day_vec);
    
    % number of new asymptomatic cases each day
    new_asymp_series(ii,:) = hist(asymp_table.time_symptoms(asymp_table.SimIndex==ii),day_vec);
    
    %number of new hospitalisations each day
    discretized_sim=hist(SIM_HOSP_DATA(hosp_characteristics(:,1)==ii,:),day_vec);
    
    new_admission_series(ii,:)= discretized_sim(:,1);
    
    new_ICU_series(ii,:) = discretized_sim(:,4);
    
    %new hosp + discharge from ICU - death/discharge from ward - discharge
    %to ICU
    ward_OCC_series(ii,:) = cumsum(discretized_sim(:,1)+discretized_sim(:,6)+discretized_sim(:,7)-discretized_sim(:,2)-discretized_sim(:,3)-discretized_sim(:,4)-discretized_sim(:,8)-discretized_sim(:,9));
    
    %new to ICU - death/discharge from ICU 
    ICU_OCC_series(ii,:) = cumsum(discretized_sim(:,4) - discretized_sim(:,5) - discretized_sim(:,6) - discretized_sim(:,7));
    
    daily_deaths(ii,:) = discretized_sim(:,3) + discretized_sim(:,5) + discretized_sim(:,8);
    
    daily_discharges(ii,:) = discretized_sim(:,2) +  discretized_sim(:,9);
end

figure(8008)
day_vec=1:800;

subplot(3,2,1)
all_infections = new_symp_series+new_asymp_series;
all_infections=all_infections(:,1:800);
plot(day_vec,all_infections)
title('new infections')
xlim([300,800])
 hold on;

subplot(3,2,2)
new_admission_series=new_admission_series(:,1:800);
shadedErrorBar(day_vec, quantile(new_admission_series,0.5), [quantile(new_admission_series,0.95)-quantile(new_admission_series,0.5);quantile(new_admission_series,0.5)-quantile(new_admission_series,0.05)], 'lineprops',{'-b','LineWidth',2})
% 
% plot(day_vec, new_admission_series)
title('new hospitalisations')
xlim([300,800])
shadedErrorBar(day_vec, quantile(new_admission_series,0.5), [quantile(new_admission_series,0.9)-quantile(new_admission_series,0.5);quantile(new_admission_series,0.5)-quantile(new_admission_series,0.1)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(new_admission_series,0.5), [quantile(new_admission_series,0.85)-quantile(new_admission_series,0.5);quantile(new_admission_series,0.5)-quantile(new_admission_series,0.15)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(new_admission_series,0.5), [quantile(new_admission_series,0.80)-quantile(new_admission_series,0.5);quantile(new_admission_series,0.5)-quantile(new_admission_series,0.2)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(new_admission_series,0.5), [quantile(new_admission_series,0.75)-quantile(new_admission_series,0.5);quantile(new_admission_series,0.5)-quantile(new_admission_series,0.25)], 'lineprops',{'-b','LineWidth',0.1}) 

subplot(3,2,3)
ward_OCC_series=ward_OCC_series(:,1:800);
plot(day_vec, ward_OCC_series)
title('ward occupancy')
xlim([300,800])

subplot(3,2,4)
ICU_OCC_series=ICU_OCC_series(:,1:800);
plot(day_vec, ICU_OCC_series)
title('ICU occupancy')
xlim([300,800])

subplot(3,2,5)
daily_deaths=daily_deaths(:,1:800);
plot(day_vec,daily_deaths) 
title('daily deaths')
xlim([300,800])

subplot(3,2,6)
cum_deaths = cumsum(daily_deaths,2);
cum_deaths=cum_deaths(:,1:800);
plot(day_vec,cum_deaths)
title('cumulative deaths')
xlim([300,800])

figure(8009)

Neut_not_hosp = 10.^individual_characteristics(~hosp_indices,5);
Neut_hosp = 10.^individual_characteristics(hosp_indices,5);

ksdensity(Neut_not_hosp)
hold on
ksdensity(Neut_hosp)
title('Neuts')
legend('not hospitalised','hospitalised')


%subplot(,,)

%subplot(,,)
