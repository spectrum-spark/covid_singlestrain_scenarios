# various code to plot the population age distributions and vaccination-related information

from create_and_generate_initial_conditions import *

from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'sans-serif'})
import matplotlib.pyplot as plt
plt.switch_backend('agg')

def plot_age_distribution(simulated_population_by_age_band,plotting_name, population_type):
    
    if population_type =="younger":
        plotting_colour =  "tab:blue"
        
    elif population_type=="older":
        plotting_colour =  "tab:red"

    fig, ax = plt.subplots(1,1, figsize=(6,6.75))

    y_pos = np.arange(len(age_bands ))

    ax.barh(y_pos,simulated_population_by_age_band,color=plotting_colour)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(age_bands )
    # ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of people')
    ax.set_title(population_type.title()+' Population',fontsize=14)
    ax.set_xlim([0,15500])
    
    # plt.rcParams['mathtext.fontset'] = 'dejavuserif'
    # plt.tight_layout()
    plt.savefig(plotting_name+"_simulated_population_by_age_band.png", bbox_inches='tight')
    plt.close()

def plot_age_distribution_pretty(simulated_population_by_age_band,plotting_name, population_type):
    
    if population_type =="younger":
        plotting_colour_0 = 'navy'
        plotting_colour_1 = 'dodgerblue'
        plotting_colour_2 = 'lightskyblue'
        
        
    elif population_type=="older":
        plotting_colour_0 = 'firebrick'
        plotting_colour_1 = 'red'
        plotting_colour_2 = 'salmon'
        

    fig, ax = plt.subplots(1,1, figsize=(5,5))

    y_pos = np.arange(len(age_bands ))

    ax.barh(y_pos,simulated_population_by_age_band,color=[plotting_colour_0,plotting_colour_1,plotting_colour_2])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(age_bands )
    # ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Population')
    ax.set_title( '“' + population_type.title() +  '” '+' Population',fontsize=14)
    ax.set_xlim([0,15500])
    ax.xaxis.grid()
    ax.set_axisbelow(True)
    ax.set_ylim([-0.4,16.4])
    
    # plt.rcParams['mathtext.fontset'] = 'dejavuserif'
    # plt.tight_layout()
    plt.savefig(plotting_name+"_simulated_population_by_age_band_pretty.png", bbox_inches='tight')
    plt.close()


def plot_vaccination_distributions(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,list_of_all_people,population_type,plotting_name,presim_parameters):
    
    total_population = presim_parameters["total_population"]
    population_type = presim_parameters["population_type"]
    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
    booster_fraction = presim_parameters["booster_fraction"]
    # total_attack_rate  = presim_parameters["total_attack_rate"]
    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction"

    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,6.75))

    y_pos = np.arange(len(age_bands ))

    ax1.barh(y_pos,vax_1_dose_by_age_band,color="lightskyblue")
    ax1.barh(y_pos,vax_2_doses_OG_by_age_band, left=vax_1_dose_by_age_band,color="deepskyblue")
    ax1.barh(y_pos,vax_3_doses_by_age_band, left=[sum(x) for x in zip(vax_1_dose_by_age_band, vax_2_doses_OG_by_age_band)],color="steelblue")
    ax1.barh(y_pos,new_primary_doses_by_age_band, left=[sum(x) for x in zip(vax_1_dose_by_age_band, vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band)],color="lightseagreen")
    
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(age_bands )
    # ax1.invert_yaxis()  # labels read top-to-bottom
    ax1.set_xlabel('Number of people')
    ax1.set_title('Number of vaccinated people in each age group',fontsize=14)


    percentage_vaxed_by_age_group1 = [100*x/y for x,y, in zip(vax_1_dose_by_age_band,simulated_population_by_age_band)]
    ax2.barh(y_pos,percentage_vaxed_by_age_group1,color="lightskyblue")

    percentage_vaxed_by_age_group2 = [100*x/y for x,y, in zip(vax_2_doses_OG_by_age_band,simulated_population_by_age_band)]
    ax2.barh(y_pos,percentage_vaxed_by_age_group2, left=percentage_vaxed_by_age_group1,color="deepskyblue")

    percentage_vaxed_by_age_group3 = [100*x/y for x,y, in zip(vax_3_doses_by_age_band,simulated_population_by_age_band)]
    ax2.barh(y_pos,percentage_vaxed_by_age_group3, left=[sum(x) for x in zip(percentage_vaxed_by_age_group1, percentage_vaxed_by_age_group2)],color="steelblue")

    percentage_vaxed_by_age_group4 = [100*x/y for x,y, in zip(new_primary_doses_by_age_band,simulated_population_by_age_band)]
    ax2.barh(y_pos,percentage_vaxed_by_age_group4 , left=[sum(x) for x in zip(percentage_vaxed_by_age_group1, percentage_vaxed_by_age_group2,percentage_vaxed_by_age_group3)],color="lightseagreen")


    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(age_bands )
    # ax2.invert_yaxis()  # labels read top-to-bottom
    ax2.set_xlabel('Percentage')
    ax2.set_title('Vaccination percentage by age band',fontsize=14)

    ax2.legend(["1 Dose only", "2 doses only (pre-winter)", "3 doses", "2 doses (winter)"],title=info_text)

    # plt.rcParams['mathtext.fontset'] = 'dejavuserif'
    # plt.tight_layout()
    plt.savefig(plotting_name+"_vaxxed_pop_by_age_band.png", bbox_inches='tight')
    plt.close()

    #############################


    total_sim_days = 3*round(30.4*6)+1
    number_of_doses_per_day = [0]*total_sim_days
    total_of_dose_N_per_day = [[0]*total_sim_days,[0]*total_sim_days,[0]*total_sim_days]
    number_of_doses_per_day_by_age = dict()
    for age_band in age_bands:
        number_of_doses_per_day_by_age[age_band] = [0]*total_sim_days

    for person in list_of_all_people:
        for i in range(len(person.vaccination_days)):
            day = person.vaccination_days[i]
            number_of_doses_per_day[day]+=1
            total_of_dose_N_per_day[i][day]+=1
            number_of_doses_per_day_by_age[person.age_band][day]+=1

    # plot by day
    days = list(range(1,total_sim_days+1))
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(12,12))
    
    ax1.plot(days,total_of_dose_N_per_day[0],color='lightskyblue')
    ax1.fill_between(days, [0]*total_sim_days, total_of_dose_N_per_day[0], color='lightskyblue', alpha=0.3)

    ax1.plot(total_of_dose_N_per_day[1],color="deepskyblue")
    ax1.fill_between(days, [0]*total_sim_days, total_of_dose_N_per_day[1], color='deepskyblue', alpha=0.3)

    ax1.plot(total_of_dose_N_per_day[2],color="steelblue")
    ax1.fill_between(days, [0]*total_sim_days, total_of_dose_N_per_day[2], color='steelblue', alpha=0.3)

    
    ax1.plot(days,number_of_doses_per_day,color="black")

    ax1.legend(["dose 1s", "dose 2s", "boosters","total doses"])
    ax1.set_xlabel('day')
    ax1.set_title('Doses given on each day: '+ population_type +" population, "+ str(100*total_vaccination_rate )+"\% vax rate, " + str(100*booster_fraction)+"\% booster fraction",fontsize=14)

    for age in age_bands:
        ax2.plot(number_of_doses_per_day_by_age[age])
        ax2.fill_between(days, [0]*total_sim_days, number_of_doses_per_day_by_age[age], alpha=0.3)

    ax2.legend(age_bands)
    ax2.set_xlabel('day (2021 ~ 2022)')
    ax2.set_title('Doses given to each age group on each day')

    plt.savefig(plotting_name+"_vax_by_day.png", bbox_inches='tight')
    plt.close()

    # plot per day with bar chart

    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(12,7))
    
    ax1.bar(days,total_of_dose_N_per_day[0],color='lightskyblue',width=1)
    ax1.bar(days,total_of_dose_N_per_day[1],bottom=total_of_dose_N_per_day[0],color="deepskyblue",width=1)
    
    ax1.bar(days,total_of_dose_N_per_day[2],bottom=[sum(x) for x in zip(total_of_dose_N_per_day[0],total_of_dose_N_per_day[1])],color="steelblue",width=1)

    ax1.legend(["dose 1s", "dose 2s", "boosters"],bbox_to_anchor=(1.04, 1.0), loc='upper left')
    #ax1.set_xlabel('day')
    ax1.set_title('Doses given on each day: '+ population_type +" population, "+ str(100*total_vaccination_rate )+"\% vax rate, " + str(100*booster_fraction)+"\% booster fraction",fontsize=14)

    prior_sum = [0]*total_sim_days

    # if population_type == "older":
    #     ax2.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, len(age_bands)))))
    # else:
    #     ax2.set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 0.5, len(age_bands)))))
    ax2.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, len(age_bands)))))

    for age in age_bands:
        ax2.bar(days,number_of_doses_per_day_by_age[age],bottom=prior_sum,width=1)
        prior_sum = [sum(x) for x in zip(prior_sum,number_of_doses_per_day_by_age[age])]

    ax2.legend(age_bands,title="age bands",bbox_to_anchor=(1.04,0), loc="lower left", borderaxespad=0)
    ax2.set_xlabel('day')
    ax2.set_title('Doses given to each age group on each day')

    plt.savefig(plotting_name+"_vax_by_day_bar.png", bbox_inches='tight')
    plt.close()



def plot_vaccination_distributions_poster(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,list_of_all_people,population_type,plotting_name,presim_parameters):

    total_population = presim_parameters["total_population"]
    population_type = presim_parameters["population_type"]
    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
    booster_fraction = presim_parameters["booster_fraction"]
    # total_attack_rate  = presim_parameters["total_attack_rate"]
    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction"

    unvaccinated = []
    for i in range(len(age_bands)):
        unvaccinated.append(simulated_population_by_age_band[i]-vax_1_dose_by_age_band[i]-vax_2_doses_OG_by_age_band[i]-vax_3_doses_by_age_band[i]-new_primary_doses_by_age_band[i])

    fig, ax1 = plt.subplots(1,1, figsize=(3.5,4))

    y_pos = np.arange(len(age_bands ))

    ax1.barh(y_pos,unvaccinated,color="plum")
    left_list = unvaccinated

    ax1.barh(y_pos,new_primary_doses_by_age_band, left=left_list,color="limegreen")

    left_list = [sum(x) for x in zip(left_list,new_primary_doses_by_age_band)]

    # ax1.barh(y_pos,vax_1_dose_by_age_band,left=left_list,color="lightskyblue")
    # left_list = [sum(x) for x in zip(left_list,vax_1_dose_by_age_band)]

    ax1.barh(y_pos,vax_2_doses_OG_by_age_band, left=left_list,color='dodgerblue')

    left_list = [sum(x) for x in zip(left_list,vax_2_doses_OG_by_age_band)]

    ax1.barh(y_pos,vax_3_doses_by_age_band, left=left_list,color="navy")

    left_list = [sum(x) for x in zip(left_list,vax_3_doses_by_age_band)]

    
    ax1.set_ylim([-0.5,16.5])
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(age_bands )
    # ax1.invert_yaxis()  # labels read top-to-bottom
    ax1.set_xlabel('population')
    ax1.set_ylabel('age band')
    # ax1.set_title('Number of vaccinated people in each age group',fontsize=14)



    ax1.legend(["unvaccinated", "newly vaccinated (after t=364)", "vaccinated first (starting t=0)", "vaccinated first \& boosted"],bbox_to_anchor=(1.04,0), loc="lower left", borderaxespad=0,frameon=False, handlelength=0.7,ncol=2)#,title=info_text)

    # plt.tight_layout()
    plt.savefig(plotting_name+"_vaxxed_pop_by_age_band_poster.png", bbox_inches='tight')
    # plt.savefig(plotting_name+"_vaxxed_pop_by_age_band_poster.svg", bbox_inches='tight')
    plt.close()

    

def plot_vaccination_distributions_percentage_pretty(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,population_type,plotting_name,presim_parameters):


    total_population = presim_parameters["total_population"]
    population_type = presim_parameters["population_type"]
    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
    booster_fraction = presim_parameters["booster_fraction"]
    # total_attack_rate  = presim_parameters["total_attack_rate"]
    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction"

    fig, ax2 = plt.subplots(1,1, figsize=(4,5))

    y_pos = np.arange(len(age_bands))
    percentage_vaxed_by_age_group1 = [100*x/y for x,y, in zip(vax_1_dose_by_age_band,simulated_population_by_age_band)]

    percentage_vaxed_by_age_group2 = [100*x/y for x,y, in zip(vax_2_doses_OG_by_age_band,simulated_population_by_age_band)]
    ax2.barh(y_pos,percentage_vaxed_by_age_group2, left=percentage_vaxed_by_age_group1,color="yellowgreen")

    percentage_vaxed_by_age_group3 = [100*x/y for x,y, in zip(vax_3_doses_by_age_band,simulated_population_by_age_band)]
    ax2.barh(y_pos,percentage_vaxed_by_age_group3, left=[sum(x) for x in zip(percentage_vaxed_by_age_group1, percentage_vaxed_by_age_group2)],color="darkgreen")

    percentage_vaxed_by_age_group4 = [100*x/y for x,y, in zip(new_primary_doses_by_age_band,simulated_population_by_age_band)]
    ax2.barh(y_pos,percentage_vaxed_by_age_group4 , left=[sum(x) for x in zip(percentage_vaxed_by_age_group1, percentage_vaxed_by_age_group2,percentage_vaxed_by_age_group3)],color="mediumturquoise")

    any_vaxxed = [sum(x) for x in zip(percentage_vaxed_by_age_group1, percentage_vaxed_by_age_group2,percentage_vaxed_by_age_group3,percentage_vaxed_by_age_group4)]
    no_vaxxed = [100-x for x in any_vaxxed]

    ax2.barh(y_pos,no_vaxxed , left=any_vaxxed,color="peachpuff")


    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(age_bands )
    # ax2.invert_yaxis()  # labels read top-to-bottom
    ax2.set_xlabel('Vaccination coverage percentage')
    ax2.set_title('1st year vaccination coverage: '+ str(round(100*total_vaccination_rate,0) )+"\%",fontsize=14)

    x_ticks = [0,10,20,30,40,50,60,70,80,90,100]
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels([str(x)+"\%" for x in x_ticks])

    ax2.legend(["Vaccinated (1st year)", "Vaccinated + Boosted", "Vaccinated (2nd year)","Unvaccinated"],bbox_to_anchor=(1.04,0), loc="lower left", borderaxespad=0,frameon=False, handlelength=0.7)

    ax2.xaxis.grid()
    ax2.set_axisbelow(True)
    ax2.set_ylim([-0.4,16.4])
    ax2.set_xlim([0,100])

    # plt.tight_layout()
    plt.savefig(plotting_name+"_vaxxed_pop_by_age_band_pretty.png", bbox_inches='tight')
    plt.close()


def plot_vaccination_distributions_extended_percentage_pretty(simulated_population_by_age_band,list_of_all_people,population_type,plotting_name,presim_parameters):


    total_population = presim_parameters["total_population"]
    population_type = presim_parameters["population_type"]
    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
    booster_fraction = presim_parameters["booster_fraction"]
    # total_attack_rate  = presim_parameters["total_attack_rate"]
    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction"

    dose_numbers ={0:{},1:{},2:{},3:{},4:{}}
    for dose in range(0,5):
        for age_band in age_bands:
            dose_numbers[dose][age_band] = 0
    
    for person in list_of_all_people:
        dose_numbers[person.doses_received][person.age_band]+=1

    print(dose_numbers)


    fig, ax2 = plt.subplots(1,1, figsize=(4,5))

    y_pos = np.arange(len(age_bands))

    people_who_got_two_doses = [dose_numbers[2][age_band] for age_band in age_bands]
    two_doses = [100*x/y for x,y, in zip(people_who_got_two_doses,simulated_population_by_age_band)]
    ax2.barh(y_pos,two_doses,color="yellowgreen")

    left = two_doses

    people_who_got_three_doses = [dose_numbers[3][age_band] for age_band in age_bands]
    three_doses = [100*x/y for x,y, in zip(people_who_got_three_doses,simulated_population_by_age_band)]
    ax2.barh(y_pos,three_doses , left=left,color="forestgreen")

    left = [sum(x) for x in zip(left, three_doses)]


    people_who_got_four_doses = [dose_numbers[4][age_band] for age_band in age_bands]
    four_doses = [100*x/y for x,y, in zip(people_who_got_four_doses,simulated_population_by_age_band)]
    ax2.barh(y_pos,four_doses , left=left,color="darkgreen")

    left = [sum(x) for x in zip(left, four_doses)]

    people_who_got_no_doses = [dose_numbers[0][age_band] for age_band in age_bands]
    no_doses = [100*x/y for x,y, in zip(people_who_got_no_doses,simulated_population_by_age_band)]

    ax2.barh(y_pos,no_doses, left=left,color="peachpuff")


    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(age_bands )
    # ax2.invert_yaxis()  # labels read top-to-bottom
    ax2.set_xlabel('Vaccination coverage percentage')
    ax2.set_title('1st year vaccination coverage: '+ str(round(100*total_vaccination_rate,0) )+"\%",fontsize=14)

    x_ticks = [0,10,20,30,40,50,60,70,80,90,100]
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels([str(x)+"\%" for x in x_ticks])

    ax2.legend(["Primary course only", "Primary + 1 Booster", "Primary + 2 Boosters","Unvaccinated"],bbox_to_anchor=(1.04,0), loc="lower left", borderaxespad=0,frameon=False, handlelength=0.7)

    ax2.xaxis.grid()
    ax2.set_axisbelow(True)
    ax2.set_ylim([-0.4,16.4])
    ax2.set_xlim([0,100])

    # plt.tight_layout()
    plt.savefig(plotting_name+"_vaxxed_pop_by_age_band_pretty_extended.png", bbox_inches='tight')
    plt.close()


def plot_vaccination_status_distributions_pretty(simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,population_type,plotting_name,presim_parameters):

    total_population = presim_parameters["total_population"]
    population_type = presim_parameters["population_type"]
    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
    booster_fraction = presim_parameters["booster_fraction"]
    # total_attack_rate  = presim_parameters["total_attack_rate"]
    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction"

    unvaccinated = []
    for i in range(len(age_bands)):
        unvaccinated.append(simulated_population_by_age_band[i]-vax_1_dose_by_age_band[i]-vax_2_doses_OG_by_age_band[i]-vax_3_doses_by_age_band[i]-new_primary_doses_by_age_band[i])

    fig, ax1 = plt.subplots(1,1, figsize=(4,5))

    y_pos = np.arange(len(age_bands ))

    left_list = vax_1_dose_by_age_band
    ax1.barh(y_pos,vax_2_doses_OG_by_age_band, left=left_list ,color="yellowgreen")

    left_list = [sum(x) for x in zip(left_list,vax_2_doses_OG_by_age_band)]

    ax1.barh(y_pos,vax_3_doses_by_age_band, left=left_list,color="darkgreen")

    left_list = [sum(x) for x in zip(left_list,vax_3_doses_by_age_band)]

    ax1.barh(y_pos,new_primary_doses_by_age_band, left=left_list,color="mediumturquoise")

    left_list = [sum(x) for x in zip(left_list,new_primary_doses_by_age_band)]


    ax1.barh(y_pos,unvaccinated,left=left_list,color="peachpuff")

    ax1.set_ylim([-0.4,16.4])
    ax1.set_xlim([0,15500])
    ax1.xaxis.grid()
    ax1.set_axisbelow(True)
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(age_bands )
    # ax1.invert_yaxis()  # labels read top-to-bottom
    ax1.set_xlabel('vaccination coverage')
    # ax1.set_ylabel('age band')
    # ax1.set_title('Number of vaccinated people in each age group',fontsize=14)
    ax1.set_title('“' + population_type.title() +  '” '+' Population',fontsize=14)

    ax1.legend(["Vaccinated (1st year)", "Vaccinated + Boosted", "Vaccinated (2nd year)","Unvaccinated"],bbox_to_anchor=(1.04,0), loc="lower left", title='1st year vaccination coverage: '+ str(round(100*total_vaccination_rate,0) )+"\%",borderaxespad=0,frameon=False, handlelength=0.7)

    # plt.tight_layout()
    plt.savefig(plotting_name+"_vaxxed_status_pop_by_age_band_pretty.png", bbox_inches='tight')
    plt.close()


def plot_vaccination_distributions_time_pretty(list_of_all_people,population_type,plotting_name,presim_parameters):
    

    total_population = presim_parameters["total_population"]
    population_type = presim_parameters["population_type"]
    total_vaccination_rate = presim_parameters["total_vaccination_rate"]
    booster_fraction = presim_parameters["booster_fraction"]
    # total_attack_rate  = presim_parameters["total_attack_rate"]
    info_text =  population_type +" population \n"+ str(100*total_vaccination_rate )+"\% vax rate\n" + str(100*booster_fraction)+"\% booster fraction"

    y_pos = np.arange(len(age_bands ))

    #############################
    total_sim_days = 1200
    number_of_doses_per_day = [0]*total_sim_days
    total_of_dose_N_per_day = [[0]*total_sim_days,[0]*total_sim_days,[0]*total_sim_days,[0]*total_sim_days]
    number_of_doses_per_day_by_age = dict()
    for age_band in age_bands:
        number_of_doses_per_day_by_age[age_band] = [0]*total_sim_days

    max_day = 0
    for person in list_of_all_people:
        for i in range(len(person.vaccination_days)):
            day = person.vaccination_days[i]
            number_of_doses_per_day[day]+=1
            total_of_dose_N_per_day[i][day]+=1
            number_of_doses_per_day_by_age[person.age_band][day]+=1

            if day > max_day:
                max_day = day

    # plot by day
    days = list(range(1,total_sim_days+1))
    

    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(9,7),sharex=True)
    
    ax1.bar(days,total_of_dose_N_per_day[0],color='lightskyblue',width=1)
    ax1.bar(days,total_of_dose_N_per_day[1],bottom=total_of_dose_N_per_day[0],color="deepskyblue",width=1)
    
    ax1.bar(days,total_of_dose_N_per_day[2],bottom=[sum(x) for x in zip(total_of_dose_N_per_day[0],total_of_dose_N_per_day[1])],color="steelblue",width=1)

    ax1.bar(days,total_of_dose_N_per_day[3],bottom=[sum(x) for x in zip(total_of_dose_N_per_day[0],total_of_dose_N_per_day[1],total_of_dose_N_per_day[2])],color="darkblue",width=1)

    ax1.legend(["first doses", "second doses", "first boosters", "second boosters"],bbox_to_anchor=(1.01, 1.0), loc='upper left',handlelength=0.7,title="dose number") # (1.04, 1.0)

    # ax1.set_title('Doses given on each day: '+ population_type +" population, "+ str(100*total_vaccination_rate )+"\% vax rate, " + str(100*booster_fraction)+"\% booster fraction",fontsize=14)

    # ax1.set_title('Doses given out each day: by number',fontsize=14)
    ax1.set_ylabel('doses')

    prior_sum = [0]*total_sim_days

    ax2.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, len(age_bands)))))

    for age in age_bands:
        ax2.bar(days,number_of_doses_per_day_by_age[age],bottom=prior_sum,width=1)
        prior_sum = [sum(x) for x in zip(prior_sum,number_of_doses_per_day_by_age[age])]

    ax2.legend(age_bands,title="age band",bbox_to_anchor=(1.01,1.0), loc="upper left", borderaxespad=0,ncol=2,handlelength=0.7)
    ax2.set_xlabel('time (days)')
    # ax2.set_title('Doses given out each day: by age group')

    ax2.set_ylabel('doses')

    ax1.set_xlim([0,max(max_day,546)])
    ax2.set_xlim([0,max(max_day,546)])

    plt.savefig(plotting_name+"_vax_by_day_dose_group.png", bbox_inches='tight')
    plt.close()