function [SIM_HOSP_DATA,hosp_indices,individual_characteristics,all_trans_probs,vax_strata,Admission_Status]=clinical_pathways_immunity_relsev2_func(state_modelled,scenario_name,rel_sev)

%Hello Eamon

%% USE THE FOLLOWING INPUTS TO TEST THIS CODE
%state_modelled='National';
%scenario_name='Example';

tic;

%% Capacity related parameters
state_list = {'National','ACT','NSW','NT','QLD','SA','TAS','VIC','WA'};
state_index=strcmp(state_list,state_modelled);
% icu_caps = [1964, 37, 737, 24, 298, 197, 39, 515, 117];
% ward_caps = [25756, 448, 8832,	276,	5099,	1915,	557,	6158,	2471];
ed_consult_caps = [10935, 202,	3945,	172,	2071,	694,	222,	2456,	1173];
%gp_consult_caps = [202999, 2607, 66616, 1582, 43627, 14005, 3935, 51338, 19289];


%ED
%EDconsult_cap = 5; %(state_index); %maximum number of daily consultations possible at ED
EDconsult_cap =Inf; %ed_consult_caps(state_index);

% % ICU
% ICU_capacity = icu_caps(state_index);
%
% % beds
% num_ward_beds = ward_caps(state_index);



%% Read Data
%sim_table=readtable('sim_number_1.csv','ReadVariableNames',true);
sim_table=readtable([scenario_name,'.csv'],'ReadVariableNames',true);
sim_table = sim_table(sim_table.num_infections == 1, :);
%this is a workaround for the format Eamon gave me (plus increases the
%sample size)

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

%sorting the table in terms of simulation index and then symptom onset time
[~,shuffle]=sort(sim_table.time_symptoms);
temp=sim_table(shuffle,:);
[~,shuffle]=sort(temp.SimIndex);
sim_table=temp(shuffle,:);

total_cases=size(sim_table,1);
num_sims = length(unique(sim_table.SimIndex));

vax_full = strcat(sim_table.vaccine);
vax_strata = unique(vax_full);
%%vax_strata = vax_strata([5,1,2,6,7,3,4]) %AlWAYS CHECK THIS ORDERING WORKS
num_vax = length(vax_strata);



%% Save factors related to individuals (these are largely going to relate to the individuals severity)
individual_characteristics = zeros(size(sim_table,1),9);

% save simulation index (these will only be seperated in prior sampling and in displaying outputs)
individual_characteristics(:,1) = sim_table.SimIndex;


%this is how we specify age categories in the CP model (this does not need to be fixed at discrete bins)
num_ages = 17;
age_widths = 5;
age_grouping_function = @(raw_age) min(ceil(raw_age./age_widths),num_ages);

% save ages (grouped according to age grouping function, which need not
% change the ages)
individual_characteristics(:,2) = age_grouping_function(sim_table.age);
individual_characteristics(:,3) = sim_table.age; %save raw ages (easier for some tables)

%set numeric for vaccine type (this may not be used but we'll save this for
%now anyway
for vv=1:num_vax
    individual_characteristics(strcmp(vax_full,vax_strata{vv}),4) = vv;
end

%save the log10 neut titres
log10_neuts = sim_table.log10_neuts;
individual_characteristics(:,5) = log10_neuts;

%compute VE's against: infection, symptoms (given infection), hospitalisation
%(given infection) and death (given infection).
log_k = 1.202;
c50 = [0.077,-0.568, -0.619, -1.377, -1.345];
individual_characteristics(:,6)=log10neut_to_VE(log10_neuts,log_k,c50(2));
individual_characteristics(:,7)=log10neut_to_VE(log10_neuts,log_k,c50(3));
individual_characteristics(:,8)=log10neut_to_VE(log10_neuts,log_k,c50(4));
individual_characteristics(:,9)=log10neut_to_VE(log10_neuts,log_k,c50(5));



%% The Delay Distribution for the Immunity model

mean_delay_by_age = [5.8;5.8;5.8;5.8;5.8;5.8;5.8;5.8;5.8;5.8;6.37;6.37;6.37;6.37;4.21;4.21;4.21];
shape_delay_by_age = [1.7;1.7;1.7;1.7;1.7;1.7;1.7;1.7;1.7;1.7;1.9;1.9;1.9;1.9;1.3;1.3;1.3];
rate_delay_by_age = mean_delay_by_age ./ shape_delay_by_age;

delay_distribution_func = @(individual_characteristics) gamrnd(shape_delay_by_age(individual_characteristics(:,2)), rate_delay_by_age(individual_characteristics(:,2) ));

%% Los Parameters (basically using full posterior conditional upon shape)

post_los_means = [2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    2, 11.3, 0.9, 9.5, 5.44, 5.21, 6.30, 4.08;
    3.3, 11.1, 1.1, 14.82, 8.91, 6.62, 10.31, 8.47;
    3.3, 11.1, 1.1, 14.82, 8.91, 6.62, 10.31, 8.47;
    3.3, 11.1, 1.1, 14.82, 8.91, 6.62, 10.31, 8.47;
    3.3, 11.1, 1.1, 14.82, 8.91, 6.62, 10.31, 8.47;
    4.8, 10.7, 1.1, 12.86, 7.73, 6.76, 8.95, 8.64;
    4.8, 10.7, 1.1, 12.86, 7.73, 6.76, 8.95, 8.64;
    7.4, 9.7, 1.3, 9.55, 5.74,6.75, 6.64, 8.64;
    7.4, 9.7, 1.3, 9.55, 5.74,6.75, 6.64, 8.64];

post_los_shapes = repmat([2, 2, 1, 2, 2, 2, 2, 2],[num_ages,1]);

post_los_uppers=[2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    2.2, 15.9, 1.2, 22.9, 10.7, 5.7, 12.3,  7.3;
    3.6, 13.1, 1.4, 21.6, 10.1, 8.9, 11.6, 11.4;
    3.6, 13.1, 1.4, 21.6, 10.1, 8.9, 11.6, 11.4;
    3.6, 13.1, 1.4, 21.6, 10.1, 8.9, 11.6, 11.4;
    3.6, 13.1, 1.4, 21.6, 10.1, 8.9, 11.6, 11.4;
    5.3, 12.4, 1.4, 19.2, 9.0, 9.6, 10.3, 12.2;
    5.3, 12.4, 1.4, 19.2, 9.0, 9.6, 10.3, 12.2;
    8.1, 11.2, 1.6, 14.8, 6.9, 10.6, 8.0, 13.5;
    8.1, 11.2, 1.6, 14.8, 6.9, 10.6, 8.0, 13.5];

%% Precalculations for LOS distributions


num_comps = size(post_los_means ,2);
shape_los_params = cell(num_comps,1);
rate_los_params = cell(num_comps,1);

for ii=1:num_comps
    
    %will need to change this estimation of st_dev at some point
    %(originally used quantiles for a normal dist to get st.dev., but now
    %using lognormal LoS distributions to avoid negative LoS
    st_dev = (post_los_uppers(:,ii)-post_los_means(:,ii))./(norminv(0.975,0,1));
    
    M=repmat(post_los_means(:,ii),[1,num_sims]);
    V=repmat(st_dev,[1,num_sims]).^2;
    MU=log(M.^2 ./ sqrt(V+M.^2));
    SIGMA = sqrt(log(V./M.^2 + 1));
    
    %sample mean LoS from the priors
    mean_los_params = lognrnd(MU,SIGMA);
    shape_los_params{ii} = repmat(post_los_shapes(:,ii),[1,num_sims]);
    rate_los_params{ii} = mean_los_params ./ shape_los_params{ii};
    
end

%the length of stay distribution for all simulations and ages
los_rng =@(individual_characteristics,comp) gamrnd(shape_los_params{comp}(individual_characteristics(:,2)+num_ages*(individual_characteristics(:,1)-1)), rate_los_params{comp}(individual_characteristics(:,2)+num_ages*(individual_characteristics(:,1)-1)));



%% Severity Functions
use_odds_ratio= @(baseline_prob,VE_index) min(((1-individual_characteristics(:,VE_index)).*baseline_prob(individual_characteristics(:,2))'./(1-baseline_prob(individual_characteristics(:,2))'))./(1+(1-individual_characteristics(:,VE_index)).*(baseline_prob(individual_characteristics(:,2))'./(1-baseline_prob(individual_characteristics(:,2))'))),1);

%left this variable in (from first nations work). Could potentially be
%used to re-evaluate reactive vaccine work. 
age_shift = 0; 

% %VE parameters here just for reference (note some of these will be related to some level of waning)
% rel_symp_vax = 1-[0, 0.4, 0.71, 0.58, 0.84, 0.58, 0.84];
% rel_hosp_vax = 1-[0,0.81,0.77,0.92,0.93,0.92,0.93];
% rel_vax_ICU = 1-[0,0.81,0.77,0.92,0.93,0.92,0.93];
% rel_vax_deathtemp = 1-[0, 0.88, 0.79, 0.89, 0.9, 0.89, 0.9];
% rel_vax_deathICUtemp = 1-[0, 0.88, 0.79, 0.89, 0.9, 0.89, 0.9];
% rel_vax_deathpostICUtemp = 1-[0, 0.88, 0.79, 0.89, 0.9, 0.89, 0.9];


%p(symps | infection)
symps_baseline = [0.28,0.28,0.2,0.2,0.26,0.26,0.33,0.33,0.4,0.4,0.49,0.49,0.63,0.63,0.69,0.69,0.69];
p_symp = use_odds_ratio(symps_baseline,7);

OR = 2.08;

%p(hosp | infection)
if age_shift==0
    hosp_baseline = 0.75 * [0.039 0.001  0.006  0.009 0.026 0.040 0.042 0.045 0.050 0.074 0.138 0.198 0.247 0.414 0.638 1.000 0.873];
elseif age_shift==10
    hosp_baseline = 0.75 * [0.039 0.001  0.006  0.009 0.042 0.045 0.050 0.074 0.138 0.198 0.247 0.414 0.638 1.000 1.000 1.000 1.000];
elseif age_shift==20
    hosp_baseline = 0.75 * [0.039 0.001  0.006  0.009 0.050 0.074 0.138 0.198 0.247 0.414 0.638 1.000 1.000 1.000 1.000 1.000 1.000];
end

temp = hosp_baseline.*symps_baseline;
p_hosp_temp = rel_sev(1).*min((OR.*temp./(1-temp))./(1+OR.*(temp./(1-temp))),1);
%p_hosp_temp = min((rel_sev(1).*p_hosp_temp./(1-p_hosp_temp))./(1+rel_sev(1).*(p_hosp_temp./(1-p_hosp_temp))),1);
p_hosp_temp = use_odds_ratio(p_hosp_temp,8);
p_hosp = min(p_hosp_temp./p_symp,1);

%% ICU probabilities
OR_ICU_delta=3.35;

% 0.24 (0.14, 0.36)
if age_shift==0
    ICU_baseline =0.24 * [0.243 0.289 0.338 0.389 0.443 0.503 0.570 0.653 0.756 0.866 0.954 1.000 0.972 0.854 0.645 0.402 0.107];
elseif age_shift==10
    ICU_baseline =0.24 * [0.243 0.289 0.338 0.389  0.570 0.653 0.756 0.866 0.954 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0];
elseif age_shift==20
    ICU_baseline =0.24 * [0.243 0.289 0.338 0.389 0.756 0.866 0.954 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0];
end

temp=ICU_baseline .*hosp_baseline.*symps_baseline;
temp2 = rel_sev(2).*min((OR_ICU_delta.*temp./(1-temp))./(1+OR_ICU_delta.*(temp./(1-temp))),1);
%temp2 = min((rel_sev(2).*temp2./(1-temp2))./(1+rel_sev(2).*(temp2./(1-temp2))),1);

temp_p_preICU = use_odds_ratio(temp2,8);
p_preICU = min(temp_p_preICU./(p_hosp.*p_symp),1);



%% Death on Ward probabilities
OR_warddeath_delta=2.33;

% 0.46 (0.36, 0.56)
if age_shift==0
    death_ward_baseline = 0.46 * [0.039, 0.037, 0.035, 0.035, 0.036, 0.039, 0.045, 0.055, 0.074, 0.107, 0.157, 0.238, 0.353, 0.502, 0.675, 0.832, 1];
elseif age_shift==10
    death_ward_baseline = 0.46 * [0.039, 0.037, 0.035, 0.035, 0.045, 0.055, 0.074, 0.107, 0.157, 0.238, 0.353, 0.502, 0.675, 0.832, 1, 1, 1];
elseif age_shift==20
    death_ward_baseline = 0.46 * [0.039, 0.037, 0.035, 0.035, 0.074, 0.107, 0.157, 0.238, 0.353, 0.502, 0.675, 0.832, 1, 1, 1, 1, 1];
end

temp= death_ward_baseline .* (1-ICU_baseline).* hosp_baseline.*symps_baseline;
temp2 = rel_sev(3).*min((OR_warddeath_delta.*temp./(1-temp))./(1+OR_warddeath_delta.*(temp./(1-temp))),1);
%temp2 = min((rel_sev(3).*temp2./(1-temp2))./(1+rel_sev(3).*(temp2./(1-temp2))),1);
temp_ward_death = use_odds_ratio(temp2,9);
p_ward_death = min(temp_ward_death./((1-p_preICU).*p_hosp.*p_symp),1);


%% Death in ICU probabilities
OR_ICUdeath_delta=2.33;

% 0.67 (0.57, 0.77)
if age_shift==0
    ICU_death_baseline = 0.67 * [0.282, 0.286, 0.291, 0.299, 0.310, 0.328, 0.353, 0.390, 0.446, 0.520, 0.604, 0.705, 0.806, 0.899, 0.969, 1.0, 0.918];
elseif age_shift==10
    ICU_death_baseline = 0.67 * [0.282, 0.286, 0.291, 0.299, 0.353, 0.390, 0.446, 0.520, 0.604, 0.705, 0.806, 0.899, 0.969, 1.0, 1.0, 1.0, 1.0];
elseif age_shift==20
    ICU_death_baseline = 0.67 * [0.282, 0.286, 0.291, 0.299, 0.446, 0.520, 0.604, 0.705, 0.806, 0.899, 0.969, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0];
end


temp = ICU_death_baseline .* ICU_baseline.* hosp_baseline.*symps_baseline;
temp2 = rel_sev(3).*min((OR_ICUdeath_delta.*temp./(1-temp))./(1+OR_ICUdeath_delta.*(temp./(1-temp))),1);
%temp2 = min((rel_sev(3).*temp2./(1-temp2))./(1+rel_sev(3).*(temp2./(1-temp2))),1);
temp_p_ICU_death = use_odds_ratio(temp2,9);
p_ICU_death = min(temp_p_ICU_death./(p_preICU.*p_hosp.*p_symp),1);


%% Death postICU probabilities
OR_postICUdeath_delta=2.33;

%0.35 (0.25, 0.46)
if age_shift==0
    postICU_death_baseline = 0.35 * [0.091 0.083 0.077 0.074 0.074 0.076 0.08 0.086 0.093 0.102 0.117 0.148 0.211 0.332 0.526 0.753 1.0];
elseif age_shift==10
    postICU_death_baseline = 0.35 * [0.091 0.083 0.077 0.074 0.08 0.086 0.093 0.102 0.117 0.148 0.211 0.332 0.526 0.753 1.0 1.0 1.0];
elseif age_shift==20
    postICU_death_baseline = 0.35 * [0.091 0.083 0.077 0.074 0.093 0.102 0.117 0.148 0.211 0.332 0.526 0.753 1.0 1.0 1.0 1.0 1.0];
end


temp=postICU_death_baseline .* (1-ICU_death_baseline) .* ICU_baseline.* hosp_baseline.*symps_baseline;
temp2 = rel_sev(3).*min((OR_postICUdeath_delta.*temp./(1-temp))./(1+OR_postICUdeath_delta.*(temp./(1-temp))),1);
%temp2 = min((rel_sev(3).*temp2./(1-temp2))./(1+rel_sev(3).*(temp2./(1-temp2))),1);
temp_p_postICU_death = use_odds_ratio(temp2,9);
p_postICU_death = min(temp_p_postICU_death./((1-p_ICU_death).*p_preICU.*p_hosp.*p_symp),1);

%     hosp_function = @(individual_characteristics) exp((log(0.5)./half_life_hosp).*individual_characteristics(:,4)).*(p_hosp(individual_characteristics(:,2))');
%     ICU_function = @(individual_characteristics) (p_preICU(individual_characteristics(:,2))');
%     death_ward_function = @(individual_characteristics) exp((log(0.5)/half_life_death).*individual_characteristics(:,4)).*(p_ward_death(individual_characteristics(:,2))');
%     death_ICU_function = @(individual_characteristics) exp((log(0.5)/half_life_death).*individual_characteristics(:,4)).*(p_ICU_death(individual_characteristics(:,2))');
%     death_postICU_function = @(individual_characteristics) exp((log(0.5)/half_life_death).*individual_characteristics(:,4)).*(p_postICU_death(individual_characteristics(:,2))');


display('Data and parameter initialisation complete')
toc;


%% Generating Hospitalisations and Modelling ED admissions and denials

%randomly generate hospital demand
hosp_demand_indicies=rand(total_cases,1)<p_hosp;

Admission_Status = nan(total_cases,3); %first is admission time (if admitted), second is an indicator determining if they were lost, the third is a count of reneg attempts

%this can now be a function of # of returns/time of first attempt (this section can potentially be applied to other transitions if we model ICU capacity etc)
p_EDreturn =@(returns) 0.5.*(returns<5);%*ones(num_strata, num_sims); %probability vector associated with returning to ED after no consults available

% model admissions for 1 simulation at a time
for ss = 1:num_sims
    
    % track the people who require hospitalisation
    sim_indices = individual_characteristics(:,1)==ss & hosp_demand_indicies;
    
    % generate first ED arrival
    attempted_admission_time = sim_table.time_symptoms(sim_indices) + delay_distribution_func(individual_characteristics(sim_indices,:));
    
    %preallocate vectors to track the number of denials at ED and the
    %indivduals that aren't hospitalised
    denied_counter = zeros(sum(sim_indices),1);
    loss_counter = zeros(sum(sim_indices),1);
    
    %sort admissions
    [~,admission_ID]=sort(attempted_admission_time);
    sorted_admission_time=attempted_admission_time(admission_ID);
    
    %find next day where ED exceeds capacity
    ceil_admission_time=ceil(sorted_admission_time);
    temp=ceil_admission_time(~isinf(ceil_admission_time));
    h=hist(temp,min(temp):max(temp));
    ED_exceeded=find(h>EDconsult_cap,1);
    
    while ~isempty(ED_exceeded)
        % the day at which ED will next exceed capacity
        next_exceeded = min(ceil_admission_time) -1 + ED_exceeded;
        
        % find the last arrivals that day
        denied_consult=find(ceil_admission_time==next_exceeded,sum(ceil_admission_time==next_exceeded)-EDconsult_cap,'last');
        
        denied_counter(denied_consult) = denied_counter(denied_consult)+1;
        
        %sample returns and losses
        returned_consult=logical(binornd(ones(length(denied_consult),1),p_EDreturn(denied_counter(admission_ID(denied_consult)))));
        
        return_indices = admission_ID(denied_consult(returned_consult));
        loss_indices = admission_ID(denied_consult(~returned_consult));
        
        % track returns and losses
        %denied_counter(return_indices) = denied_counter(return_indices) + 1;
        loss_counter(loss_indices) = 1;
        
        % Update renegs and loss (for returns, asssume a uniform random return on the next
        % day)
        attempted_admission_time(return_indices) = next_exceeded+rand(size(return_indices,1),1);
        attempted_admission_time(loss_indices) = Inf;
        
        % sort
        [~,admission_ID]=sort(attempted_admission_time);
        sorted_admission_time=attempted_admission_time(admission_ID);
        
        %find the next time to hit capacity
        ceil_admission_time=ceil(sorted_admission_time);
        temp=ceil_admission_time(~isinf(ceil_admission_time));
        h=hist(temp,min(temp):max(temp));
        ED_exceeded=find(h>EDconsult_cap,1);
        
        
    end
    Admission_Status(sim_indices,:)=[attempted_admission_time,loss_counter,denied_counter];
end

num_denials=sum(Admission_Status(:,3),'omitnan');
num_lost = sum(Admission_Status(:,2),'omitnan');

display(['Number of denials at ED: ', num2str(num_denials)])
display(['Number that never returned to ED: ', num2str(num_lost)])

%save info on individuals that were admitted
hosp_indices = logical(~isnan(Admission_Status(:,1)) & ~isinf(Admission_Status(:,1)));
hosp_characteristics = individual_characteristics(hosp_indices,:);

total_hosps = sum(hosp_indices);

SIM_HOSP_DATA = nan(total_hosps,9);



%save hospital admission times
SIM_HOSP_DATA(:,1)=Admission_Status(hosp_indices,1);

p_preICUhosp=p_preICU(hosp_indices);
p_ward_deathhosp = p_ward_death(hosp_indices);
p_ICU_deathhosp = p_ICU_death(hosp_indices);
p_postICU_deathhosp = p_postICU_death(hosp_indices);


%% generating transition events
ICU_indicies=rand(total_hosps,1)<p_preICUhosp;

ward_death_indices = zeros(total_hosps,1);
ward_death_indices(~ICU_indicies) = logical(rand(sum(~ICU_indicies),1) < p_ward_deathhosp(~ICU_indicies));

deathICU_indices = zeros(total_hosps,1);
deathICU_indices(ICU_indicies) = rand(sum(ICU_indicies),1) < p_ICU_deathhosp(ICU_indicies);

deathpostICU_indices = zeros(total_hosps,1);
deathpostICU_indices(ICU_indicies & ~deathICU_indices) = logical(rand(sum(ICU_indicies & ~deathICU_indices),1) < p_postICU_deathhosp(ICU_indicies & ~deathICU_indices));


%ordering: Admission, Ward discharge (no ICU), Ward death (no ICU), preICU ward, ICU
%death, ICU to ward death, ICU to ward discharge, postICU death, postICU

%% generating transition times
%Ward (no ICU) discharge time
SIM_HOSP_DATA(~ward_death_indices & ~ICU_indicies,2) = SIM_HOSP_DATA(~ward_death_indices & ~ICU_indicies,1) + los_rng(hosp_characteristics(~ward_death_indices & ~ICU_indicies,:),1);

%Ward (no ICU) death time
SIM_HOSP_DATA(logical(ward_death_indices),3) = SIM_HOSP_DATA(logical(ward_death_indices),1) + los_rng(hosp_characteristics(logical(ward_death_indices),:),2);

%ICU admission
SIM_HOSP_DATA(ICU_indicies,4) = SIM_HOSP_DATA(ICU_indicies,1) + los_rng(hosp_characteristics(ICU_indicies,:),3);

% ICU death
SIM_HOSP_DATA(logical(deathICU_indices),5) = SIM_HOSP_DATA(logical(deathICU_indices),4) + los_rng(hosp_characteristics(logical(deathICU_indices),:),4);

% ICU to ward (eventual death)
SIM_HOSP_DATA(logical(deathpostICU_indices),6) = SIM_HOSP_DATA(logical(deathpostICU_indices),4) + los_rng(hosp_characteristics(logical(deathpostICU_indices),:),5);

% ICU to ward (eventual discharge)
SIM_HOSP_DATA(ICU_indicies & ~deathICU_indices & ~deathpostICU_indices,7) = SIM_HOSP_DATA(ICU_indicies & ~deathICU_indices & ~deathpostICU_indices,4) + los_rng(hosp_characteristics(ICU_indicies & ~deathICU_indices & ~deathpostICU_indices,:),6);


% postICU death
SIM_HOSP_DATA(logical(deathpostICU_indices),8) = SIM_HOSP_DATA(logical(deathpostICU_indices),6) + los_rng(hosp_characteristics(logical(deathpostICU_indices),:),7);

%post ICU discharge
SIM_HOSP_DATA(ICU_indicies & ~deathICU_indices & ~deathpostICU_indices,9) = SIM_HOSP_DATA(ICU_indicies & ~deathICU_indices & ~deathpostICU_indices,7) + los_rng(hosp_characteristics(ICU_indicies & ~deathICU_indices & ~deathpostICU_indices,:),8);

%% saving things
all_trans_probs = [p_hosp,p_preICU,p_ward_death,p_ICU_death,p_postICU_death];
save([scenario_name,'_',num2str(rel_sev),'.mat'],'SIM_HOSP_DATA','hosp_indices','individual_characteristics','all_trans_probs','vax_strata','Admission_Status')


max_T = 900;
day_vec = (1:ceil(max_T))-0.5;

new_symp_series=zeros(aug_num, length(day_vec));
new_asymp_series=zeros(aug_num, length(day_vec));
new_admission_series=zeros(aug_num, length(day_vec));
new_ICU_series=zeros(aug_num, length(day_vec));
ward_OCC_series=zeros(aug_num, length(day_vec));
ICU_OCC_series=zeros(aug_num, length(day_vec));
daily_deaths=zeros(aug_num, length(day_vec));
daily_discharges=zeros(aug_num, length(day_vec));



for jj=1:aug_num
    %number of new symptomatic cases each day
    new_symp_series(jj,:) = hist(sim_table.time_symptoms(sim_table.SimIndex==jj),day_vec);
    
    % number of new asymptomatic cases each day
    new_asymp_series(jj,:) = hist(asymp_table.time_symptoms(asymp_table.SimIndex==jj),day_vec);
    
    %number of new hospitalisations each day
    discretized_sim=hist(SIM_HOSP_DATA(hosp_characteristics(:,1)==jj,:),day_vec);
    
    new_admission_series(jj,:)= discretized_sim(:,1);
    
    new_ICU_series(jj,:) = discretized_sim(:,4);
    
    %new hosp + discharge from ICU - death/discharge from ward - discharge
    %to ICU
    ward_OCC_series(jj,:) = cumsum(discretized_sim(:,1)+discretized_sim(:,6)+discretized_sim(:,7)-discretized_sim(:,2)-discretized_sim(:,3)-discretized_sim(:,4)-discretized_sim(:,8)-discretized_sim(:,9));
    
    %new to ICU - death/discharge from ICU
    ICU_OCC_series(jj,:) = cumsum(discretized_sim(:,4) - discretized_sim(:,5) - discretized_sim(:,6) - discretized_sim(:,7));
    
    daily_deaths(jj,:) = discretized_sim(:,3) + discretized_sim(:,5) + discretized_sim(:,8);
    
    daily_discharges(jj,:) = discretized_sim(:,2) +  discretized_sim(:,9);
end


all_infections=new_symp_series+new_asymp_series;

save([scenario_name,'_',num2str(rel_sev),'_discrete.mat'],'all_infections','new_symp_series','new_asymp_series','discretized_sim','new_admission_series','new_ICU_series','ward_OCC_series','ICU_OCC_series','daily_deaths','daily_discharges','day_vec')



    function currentVE = log10neut_to_VE(log10_neut,log_k,c50)
        currentVE=1./(1+exp(-exp(log_k).*(log10_neut - c50)));
    end
%     function currentVE=estimate_current_efficacy(VE0, decay_rate, time_since_vaccination, lookup)
%
%         init_neut = get_neut_from_efficacy(VE0, lookup);
%         current_neut = get_neut_over_time(init_neut, decay_rate,time_since_vaccination);
%         currentVE = get_efficacy_from_neut(current_neut, lookup);
%     end
%
%     function neut=get_neut_from_efficacy(VE, lookup)
%
%
%
%         loweff_ind=find(lookup(:,2)<=VE,1,'last');
%         higheff_ind=find(lookup(:,2)>=VE,1,'first');
%
%         if isempty(loweff_ind)
%             %if neut is too low (note the file has a minimum VE against death of 0.05)
%             log10neut = min(lookup(:,1));
%             display('min neut hit')
%         elseif isempty(higheff_ind)
%             log10neut = max(lookup(:,1));
%             display('max neut exceeded')
%         else
%             lowneut=lookup(loweff_ind,1);
%             lowVE=lookup(loweff_ind,2);
%
%             if lowVE~=VE
%                 %interpolate if no match
%
%                 highneut=lookup(higheff_ind,1);
%                 highVE=lookup(higheff_ind,2);
%
%                 log10neut = interp1([lowVE,highVE],[lowneut,highneut],VE);
%             else
%                 %exact match
%                 log10neut = lowneut;
%             end
%         end
%
%         neut = 10^log10neut;
%     end
%
%     function eff=get_efficacy_from_neut(neut, lookup)
%
%         log10neut=log10(neut);
%         loweff_ind=find(lookup(:,1)<=log10neut,1,'last');
%         higheff_ind=find(lookup(:,1)>=log10neut,1,'first');
%
%
%         if isempty(loweff_ind)
%             eff = 0;
%             display('min VE hit')
%         elseif isempty(higheff_ind)
%             eff=1;
%             display('max VE hit')
%         else
%             lowneut=lookup(loweff_ind,1);
%             lowVE=lookup(loweff_ind,2);
%             if lowneut~=log10neut
%
%                 highneut=lookup(higheff_ind,1);
%                 highVE=lookup(higheff_ind,2);
%
%                 eff = interp1([lowneut,highneut],[lowVE,highVE],log10neut);
%             else
%                 eff = lowVE;
%
%             end
%         end
%     end
%
%
%     function current_neut = get_neut_over_time(starting_neut, decay_rate, time)
%         if (decay_rate > 0)
%             decay_rate = -decay_rate;
%         end
%         current_neut = starting_neut*exp(decay_rate*time);
%     end
 end
