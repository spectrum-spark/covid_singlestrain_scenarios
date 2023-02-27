function day_vec=combined_output_plotter2(broad_scenario_name,rel_sev,col_spec)

load([broad_scenario_name,'_',num2str(rel_sev),'_full.mat'])

trunc_T = 800;

all_infections=all_infections_big(:,1:trunc_T);
new_symp_series=new_symp_series_big(:,1:trunc_T);
new_asymp_series=new_asymp_series_big(:,1:trunc_T);
new_admission_series=new_admission_series_big(:,1:trunc_T);
new_ICU_series=new_ICU_series_big(:,1:trunc_T);
ward_OCC_series=ward_OCC_series_big(:,1:trunc_T);
ICU_OCC_series=ICU_OCC_series_big(:,1:trunc_T);
daily_deaths=daily_deaths_big(:,1:trunc_T);
daily_discharges=daily_discharges_big(:,1:trunc_T);


% day_vec= datetime(2021,02,14) + days(1:trunc_T) ;
day_vec= datetime(2021,09,01) + days(1:trunc_T) ;% CHANGED by TK

figure(8008)

temp_label = all_infections;
subplot(3,2,1)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{['-',col_spec],'LineWidth',2})
hold on
title('Infections (daily)')
% xlim(day_vec([300,500]))
xlim(day_vec([200,300])) % changed 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 


temp_label = new_admission_series;
subplot(3,2,2)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{['-',col_spec],'LineWidth',2})
hold on
title('Hospital Admissions (daily)')
% xlim(day_vec([300,500]))
xlim(day_vec([200,300])) % changed 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 



temp_label = ward_OCC_series;
subplot(3,2,3)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{['-',col_spec],'LineWidth',2})
hold on
title('Ward Occupancy')
% xlim(day_vec([300,500]))
xlim(day_vec([200,300])) % changed 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 


temp_label = ICU_OCC_series;
subplot(3,2,4)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{['-',col_spec],'LineWidth',2})
hold on
title('ICU Occupancy')
% xlim(day_vec([300,500]))
xlim(day_vec([200,300])) % changed 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 


temp_label = daily_deaths;
subplot(3,2,5)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{['-',col_spec],'LineWidth',2})
hold on
title('Deaths (daily)')
% xlim(day_vec([300,500]))
xlim(day_vec([200,300])) % changed 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 


temp_label=cumsum(daily_deaths,2);
subplot(3,2,6)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{['-',col_spec],'LineWidth',2})
hold on
title('Cumulative Deaths')
% xlim(day_vec([300,500]))
xlim(day_vec([200,300])) % changed 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{['-',col_spec],'LineWidth',0.1}) 

end