import csv
import os

# initial-initial parameters
total_population = 100000
population_type = "younger"
total_attack_rate = 0.2
total_vaccination_rate = 0.2


folder = "winter_wave_scenarios"
filename = "vax_infect_scenario1.csv"
file = os.path.join(os.path.dirname(__file__), folder , filename)

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

vax_percentange_by_age_band= [0.0,0.10,0.26,0.26,0.81,0.81 ,0.87,0.87,0.93,0.93,0.87,0.87,0.77,0.77,0.64,0.64,0.37] # world wide

vax_by_age_band_pre_scale = [per*pop for per,pop in zip(vax_percentange_by_age_band,simulated_population_by_age_band)] # aka if the population vaccination had followed the world distribution

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


header =['age_band','num_people','max_vax','infection']



num_people = {0:{},1:{}}
num_people[0][0] = unvaxxed_uninfected_pop_by_age_band
num_people[0][2] = vaxxed_uninfected_pop_by_age_band
num_people[1][0] = unvaxxed_infected_pop_by_age_band
num_people[1][2] = vaxxed_infected_pop_by_age_band

# open the file in the write mode
with open(file, 'w', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
    rows = []

    for age_band in range(1,17+1):

        for infection in [0,1]:
            for max_vax in [0,2]:
                num = num_people[infection][max_vax][age_band-1]
                row = [age_band,num ,max_vax,infection]
                rows.append(row)

                # write a row to the csv file
    writer.writerows(rows)


