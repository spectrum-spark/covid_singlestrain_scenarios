function combined_output_plotter(broad_scenario_name)


load(['outputs_full_',broad_scenario_name,'.mat'])

trunc_T = 800;
day_vec= 1:trunc_T ;

figure(8008)

temp_label = all_infections;
subplot(3,2,1)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{'-b','LineWidth',2})
hold on
title('all_infections')
xlim([300,800])
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{'-b','LineWidth',0.1}) 


temp_label = new_admission_series;
subplot(3,2,2)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{'-b','LineWidth',2})
hold on
title('new hospitalisations')
xlim([300,800])
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{'-b','LineWidth',0.1}) 


temp_label = ward_OCC_series;
subplot(3,2,3)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{'-b','LineWidth',2})
hold on
title('ward occupancy')
xlim([300,800])
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{'-b','LineWidth',0.1}) 

temp_label = ICU_OCC_series;
subplot(3,2,4)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{'-b','LineWidth',2})
hold on
title('ICU occupancy')
xlim([300,800])
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{'-b','LineWidth',0.1}) 

temp_label = daily_deaths;
subplot(3,2,5)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{'-b','LineWidth',2})
hold on
title('daily deaths')
xlim([300,800])
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{'-b','LineWidth',0.1}) 

temp_label=cumsum(daily_deaths,2);
subplot(3,2,6)
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.95)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.05)], 'lineprops',{'-b','LineWidth',2})
hold on
title('cumulative deaths')
xlim([300,800])
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.9)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.1)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.85)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.15)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.80)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.2)], 'lineprops',{'-b','LineWidth',0.1}) 
shadedErrorBar(day_vec, quantile(temp_label,0.5), [quantile(temp_label,0.75)-quantile(temp_label,0.5);quantile(temp_label,0.5)-quantile(temp_label,0.25)], 'lineprops',{'-b','LineWidth',0.1}) 
end