% figure(8008)
% subplot(3,2,2)
% plot(0,0,'g.')
% hold on
% plot(0,0,'r.')
% plot(0,0,'b.')
% plot(0,0,'m.')
% combined_output_plotter('scenario1_2000Omicron','g')
% combined_output_plotter('scenario2_2000Omicron','r')
% combined_output_plotter('scenario13_2000Omicron','b')
% combined_output_plotter('scenario14_2000Omicron','m')
% legend('60% 6month','80% 6month','60% 3month','80% 3 month','Location','NorthWest')
% 


fig = figure(1)
set(fig, 'defaultLegendAutoUpdate',' off');
subplot(3,2,2)
plot(0,0,'k.','MarkerSize',20)
hold on
plot(0,0,'r.','MarkerSize',20)
plot(0,0,'m.','MarkerSize',20)
plot(0,0,'b.','MarkerSize',20)

subplot(3,2,2)
legend('3 months','4 months', '5 months', '6 months','Location','NorthEast','FontSize',12, 'AutoUpdate','off')
%plot(0,0,'g.','MarkerSize',20)
%plot(0,0,'c.','MarkerSize',20)
%combined_output_plotter2('scenario2_2000Omicron',[0.5,0.5,0.5],'k')
%combined_output_plotter2('scenario2_2000Omicron_Low',[0.5,0.5,0.5],'r')
%combined_output_plotter2('scenario2_2000Omicron_Med',[0.5,0.5,0.5],'m')
%combined_output_plotter2('scenario14_2000Omicron_Low',[0.5,0.5,0.5],'g')
%combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario25_2000Omicron_Baseline',[1,1,1],'k')
%combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario25_2000Omicron_Low',[1,1,1],'r')
%combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario25_2000Omicron_Med',[1,1,1],'m')
%combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario26_2000Omicron_Baseline',[1,1,1],'b')
%combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario26_2000Omicron_Low',[1,1,1],'g')
%combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario26_2000Omicron_Med',[1,1,1],'c')
%combined_output_plotter2('scenario25_2000Omicron_Baseline',[1,1,1],'c')

combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario2_2000Omicron_Baseline',[1 1 1],'k');
combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario25_2000Omicron_Med',[1,1,1],'r');
combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario26_2000Omicron_Med',[1,1,1],'m');
day_vec=combined_output_plotter2('/home/michaell/cm37_scratch/health/NSW_outputs/scenario2_2000Omicron_Med',1,'b');

subplot(3,2,2)
plot(day_vec([300,500]),[3900,3900],'k--','LineWidth',1.5)
subplot(3,2,3)
plot(day_vec([300,500]),[8800,8800],'k--','LineWidth',1.5)
subplot(3,2,4)
plot(day_vec([300,500]),[750,750],'k--','LineWidth',1.5)

datetick('x', '')

%legend(gca, 'off')

%Figure size:
set(gcf, 'PaperUnits','inches','PaperPosition', [0 0 12.2 12.96])
print(gcf, '-dpng', 'med_phsms_severity.png', '-r150')
