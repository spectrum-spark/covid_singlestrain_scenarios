import csv
import os

folder = "winter_wave_scenarios"

# # initial-initial parameters; booster doses to be given to everyone who previously got vaccinated 
# total_population = 100000
# population_type = "younger"
# total_attack_rate = 0.2
# total_vaccination_rate = 0.2
# filename = "initial-and-during_vax_infect_scenario1.csv"


# initial-initial parameters; booster doses to be given to everyone who previously got vaccinated 
total_population = 100000
population_type = "older"
total_attack_rate = 0.2
total_vaccination_rate = 0.2
filename = "initial-and-during_vax_infect_scenario1_older.csv"




file = os.path.join(os.path.dirname(__file__), folder , filename)
plotting_name = os.path.join(os.path.dirname(__file__), folder , "initial-and-during_vax_infect_scenario1_older")

# population demographics 

if population_type =="younger":
    population_by_age_band_approx = [1107,1043,994,924,837,717,637,584,511,428,349,280,217,155,90,47,27] # PNG
    
elif population_type=="older":
    population_by_age_band_approx = [20,20,23,21,21,19,23,21,19,21,19,17,13,10,6,5,3] # French Polynesia

total_pop_temp = sum(population_by_age_band_approx)
percentage_pop_by_age_band = [x/total_pop_temp for x in population_by_age_band_approx]

simulated_population_by_age_band = [x*total_population for x in percentage_pop_by_age_band]

print("simulated_population_by_age_band",simulated_population_by_age_band)

# infection numbers ######################################################################################

total_infected_pop = total_population*total_attack_rate

# ideally, this should be percentage of infections within each group...?
aus_cases_by_age_band_approx = [100,130,150,160,245,260,190,180,150,130,109,101,65,55,35,30,16] # by 1000s, for one gender/half
# https://www.health.gov.au/health-alerts/covid-19/case-numbers-and-statistics
# https://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/3101.0Jun%202019?OpenDocument
aus_pop_by_age_band_approx = [805,830,799,772,903,959,933,884,793,824,750,757,675,595,518,351,424] # by 1000s, for one gender/half of pop

aus_percentage_cases_by_age_band = [x/y for x,y in zip(aus_cases_by_age_band_approx,aus_pop_by_age_band_approx )]

# total_cases = sum(cases_by_age_band_approx)
# percentage_cases_by_age_band = [x/total_cases for x in cases_by_age_band_approx]

infected_cases_by_age_band_prescale = [x*y for x,y in zip(aus_percentage_cases_by_age_band,simulated_population_by_age_band)]
sum_infected_cases_by_age_band_prescale = sum(infected_cases_by_age_band_prescale )
infected_cases_by_age_band = [x*total_infected_pop/sum_infected_cases_by_age_band_prescale for x in infected_cases_by_age_band_prescale]

# print(infected_cases_by_age_band)

print("total infected population", total_infected_pop)
print("total infected cases:",sum(infected_cases_by_age_band)) # should be the same number 

for i in range(17):
    if simulated_population_by_age_band[i]<infected_cases_by_age_band[i]:
        print("more infected people in this age band than actually exists!")

########################################################################################################
# vaccination numbers 

total_vaccinated_pop = total_population*total_vaccination_rate

# https://ourworldindata.org/grapher/covid-fully-vaccinated-by-age?time=latest&country=~HKG
vax_percentange_by_age_band= [0.0,0.10,0.26,0.26,0.81,0.81 ,0.87,0.87,0.93,0.93,0.87,0.87,0.77,0.77,0.64,0.64,0.37] 

vax_by_age_band_pre_scale = [per*pop for per,pop in zip(vax_percentange_by_age_band,simulated_population_by_age_band)] # aka if the population vaccination had followed the above distribution

sum_vax_by_age_band_pre_scale = sum(vax_by_age_band_pre_scale )

vaxxed_pop_by_age_band = [x*total_vaccinated_pop/sum_vax_by_age_band_pre_scale for x in vax_by_age_band_pre_scale]

for i in range(17):
    if simulated_population_by_age_band[i]<vaxxed_pop_by_age_band[i]:
        print("more vaccinated people in this age band than actually exists!")

# total_vax = sum(vax_by_age_band_approx)
# percentage_vax_by_age_band = [x/total_vax for x in vax_by_age_band_approx]
# vaxxed_pop_by_age_band = [x*total_vaccinated_pop for x in percentage_vax_by_age_band]

########################################################################################################
# assuming that only 9% of infected are vaccinated 

unvaxxed_infected_pop_by_age_band = [ round(0.91*x) for x in infected_cases_by_age_band]
vaxxed_infected_pop_by_age_band = [round(0.09*x) for x in infected_cases_by_age_band]

# total vaxxed pop - vaxxed_infected_pop
vaxxed_uninfected_pop_by_age_band = [max([0,round(a_i - b_i)]) for a_i, b_i in zip(vaxxed_pop_by_age_band, vaxxed_infected_pop_by_age_band)]

# total unvaxed pop - unvaxed_infected pop
unvaxxed_uninfected_pop_by_age_band = [max([0,round(total-i-j-k)]) for total, i,j,k in zip(simulated_population_by_age_band,unvaxxed_infected_pop_by_age_band, vaxxed_infected_pop_by_age_band,vaxxed_uninfected_pop_by_age_band)]

print("unvaxxed_infected_pop_by_age_band",unvaxxed_infected_pop_by_age_band)
print("vaxxed_infected_pop_by_age_band",vaxxed_infected_pop_by_age_band)

print("unvaxxed_uninfected_pop_by_age_band",unvaxxed_uninfected_pop_by_age_band) # these two have negative values for some reason
print("vaxxed_uninfected_pop_by_age_band",vaxxed_uninfected_pop_by_age_band)# these two have negative values for some reason

# check that the total population adds up right after making everything integer again! 
print(sum(unvaxxed_infected_pop_by_age_band)+sum(vaxxed_infected_pop_by_age_band)+sum(vaxxed_uninfected_pop_by_age_band)+sum(unvaxxed_uninfected_pop_by_age_band))


header =['age_band','num_people','max_vax','infection','third_dose_round']



num_people = {0:{},1:{}}
num_people[0][0] = unvaxxed_uninfected_pop_by_age_band
num_people[0][2] = vaxxed_uninfected_pop_by_age_band
num_people[1][0] = unvaxxed_infected_pop_by_age_band
num_people[1][2] = vaxxed_infected_pop_by_age_band


# with open(file, 'w', newline='') as f:
#     # create the csv writer
#     writer = csv.writer(f)

#     # write the header
#     writer.writerow(header)
#     rows = []

#     for age_band in range(1,17+1):

#         for infection in [0,1]:
#             for max_vax in [0,2]:
#                 num = num_people[infection][max_vax][age_band-1]
#                 row = [age_band,num ,max_vax,infection,max_vax/2] # max_vax/2 -> for those with primary doses, they will also get a dose in the 3rd round
#                 rows.append(row)

#                 # write a row to the csv file
#     writer.writerows(rows)


######################################

# PLOTTING INITIAL CONDITIONS

import scipy.stats as stats
from matplotlib import rc

rc('text', usetex=True)
rc('font', **{'family': 'serif'})
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np


if population_type =="younger":
    plotting_colour =  "tab:blue"
    
elif population_type=="older":
    plotting_colour =  "tab:red"
    

age_bands = ["0-4","5-11","12-15","16-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80+"]

# todo: plot simulated_population_by_age_band vs age band 
fig, ax = plt.subplots(1,1, figsize=(6,6))

y_pos = np.arange(len(age_bands ))

ax.barh(y_pos,simulated_population_by_age_band,color=plotting_colour)
ax.set_yticks(y_pos)
ax.set_yticklabels(age_bands )
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Number of people')
ax.set_title('Population')



# plt.rcParams['mathtext.fontset'] = 'dejavuserif'
# plt.tight_layout()
plt.savefig(plotting_name+"_simulated_population_by_age_band.png", bbox_inches='tight')
plt.close()


fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,6))

y_pos = np.arange(len(age_bands ))

ax1.barh(y_pos,vaxxed_pop_by_age_band,color=plotting_colour)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(age_bands )
ax1.invert_yaxis()  # labels read top-to-bottom
ax1.set_xlabel('Number of people')
ax1.set_title('Number of vaccinated people in each age group')


percentage_vaxed_by_age_group = [100*x/y for x,y, in zip(vaxxed_pop_by_age_band,simulated_population_by_age_band)]
ax2.barh(y_pos,percentage_vaxed_by_age_group,color=plotting_colour)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(age_bands )
ax2.invert_yaxis()  # labels read top-to-bottom
ax2.set_xlabel('Percentage')
ax2.set_title('Vaccination percentage by age band')

# plt.rcParams['mathtext.fontset'] = 'dejavuserif'
# plt.tight_layout()
plt.savefig(plotting_name+"_vaxxed_pop_by_age_band.png", bbox_inches='tight')
plt.close()

t = np.linspace(0, 90, 90)
age =(-101.0/90.0)*(t-90)

fig, ax = plt.subplots(1,1, figsize=(10,6))

ax.plot(t,age,color=plotting_colour)
ax.set_xlabel('time (days)')
ax.set_ylabel('age')
ax.set_title('Vaccination day by age')
ax.set_xlim([0,90])
ax.set_ylim([0,101])

axes2 = ax.twinx()

age_bands = ["0-4","5-11","12-15","16-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80+"]
age_band_center = [2,8,13.5,17.5,22,27,32,37,42,47,52,57,62,67,72,77,82]
time_per_age_band =[(-90.0/101.0)*a+90 for a in age_band_center] 

rects  = axes2.bar(time_per_age_band,vaxxed_pop_by_age_band,width = 2,color=plotting_colour )
axes2.set_ylabel("number of people")

# Make some labels.
labels =age_bands

for rect, label in zip(rects, labels):
    height = rect.get_height()
    axes2.text(
        rect.get_x() + rect.get_width() / 2, height, label, ha="center", va="bottom"
    )


    # axes2.annotate('{}'.format(height),
    #                 xy=(rect.get_x() + rect.get_width() / 2, height),
    #                 xytext=(0, 3),  # 3 points vertical offset
    #                 textcoords="offset points",
    #                 ha='center', va='bottom')

# plt.rcParams['mathtext.fontset'] = 'dejavuserif'
# plt.tight_layout()
plt.savefig(plotting_name+"_vax_by_age.png", bbox_inches='tight')
plt.close()

fig, ax = plt.subplots(1,1, figsize=(10,6))

time =  np.linspace(0, 212, 212)

mean = (181.0 + 122.0) / 2.0
norm_sd = (181.0 - 122.0) / 4.0
ax.plot(time,stats.norm.pdf(time,mean,norm_sd),color=plotting_colour)

ax.set_xlabel('time (days)')
ax.set_ylabel('probability')
ax.set_title('covid wave pre April 2022')

plt.savefig(plotting_name+"_infection_distribution.png", bbox_inches='tight')
plt.close()







fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,6))

y_pos = np.arange(len(age_bands ))

ax1.barh(y_pos,infected_cases_by_age_band,color=plotting_colour)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(age_bands )
ax1.invert_yaxis()  # labels read top-to-bottom
ax1.set_xlabel('Number of people')
ax1.set_title('Number of infected people in each age group')


percentage_infected_by_age_group = [100*x/y for x,y, in zip(infected_cases_by_age_band,simulated_population_by_age_band)]
ax2.barh(y_pos,percentage_infected_by_age_group,color=plotting_colour)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(age_bands )
ax2.invert_yaxis()  # labels read top-to-bottom
ax2.set_xlabel('Percentage')
ax2.set_title('Infection percentage by age band')

# plt.rcParams['mathtext.fontset'] = 'dejavuserif'
# plt.tight_layout()
plt.savefig(plotting_name+"_infected_pop_by_age_band.png", bbox_inches='tight')
plt.close()