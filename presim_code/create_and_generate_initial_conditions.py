# functions to calculate the population, vaccination allocation across the population, and vaccination schedule

import json
import os
import math
import random
import csv
import numpy as np
from iteround import saferound
from Individual import *

# for the abm

age_bands = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_band_id = {"0-4":1,"5-11":2,"12-15":3,'16-19':4, '20-24':5, '25-29':6, '30-34':7, '35-39':8, '40-44':9, '45-49':10, '50-54':11, '55-59':12, '60-64':13, '65-69':14, '70-74':15, '75-79':16, '80+':17}

# calculates the number of people per age band given the population distributions and the total population size
def population_by_age_distribution(total_population,population_type,year=2021):
    folder_path = os.path.join(os.path.dirname(__file__),"population")

    file_save_name = "abm_population_" + str(population_type) +"_year_" +str(year)+".json"

    fullfilename = os.path.join(folder_path,file_save_name)
    with open(fullfilename, "r") as file:
        data = json.load(file)
    
    population_by_age_band_approx = [data[age_band] for age_band in age_bands]

    total_pop_temp = sum(population_by_age_band_approx)

    percentage_pop_by_age_band = [x/total_pop_temp for x in population_by_age_band_approx]

    simulated_population_by_age_band = saferound([x*total_population for x in percentage_pop_by_age_band], places=0)

    simulated_population_by_age_band = [int(x) for x in simulated_population_by_age_band]
    
    # simulated_population_by_age_band = [round(x*total_population) for x in percentage_pop_by_age_band]

    print("simulated_population_by_age_band:",simulated_population_by_age_band)
    print("total simulated population:",sum(simulated_population_by_age_band))

    if sum(simulated_population_by_age_band)!= total_population:
            print("incorrect number of total people")
            exit(1)

    return simulated_population_by_age_band

# assigns who will get the vaccination doses during the first year (pre-booster)
def primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,oldest_group_coverage):
    total_vaccinated_pop = total_population*total_vaccination_rate
    primary_doses_available = total_population*total_vaccination_rate

    vax_1_dose_by_age_band = [0]*len(age_bands)  # assuming that no one only gets one dose 

    # find first occurence of "60"
    old_index = 0
    for age_band in age_bands:
        if "60" in age_band:
            old_index = age_bands.index(age_band)
            break


    doses_oldest_group = oldest_group_coverage*sum(simulated_population_by_age_band[old_index:])
    remaining_doses_for_others = primary_doses_available-doses_oldest_group
    
    if(remaining_doses_for_others <0):
        print("more dose covereage for the oldest population than actually possible")
        exit(1)
    
    population_old = sum(simulated_population_by_age_band[old_index:])
    population_middle = sum(simulated_population_by_age_band[1:old_index]) # not including the youngest group and not including the oldest group

    full_vax_by_age_band = []
    for i in range(len(simulated_population_by_age_band)):
        if i ==0: # youngest group
            full_vax_by_age_band.append(0.0)
        elif i >= old_index: #oldest group
            full_vax_by_age_band.append(doses_oldest_group*simulated_population_by_age_band[i]/population_old)
        else:
            full_vax_by_age_band.append(remaining_doses_for_others*simulated_population_by_age_band[i]/population_middle)
    
    full_vax_by_age_band = saferound(full_vax_by_age_band,places=0)
    full_vax_by_age_band = [int(x) for x in full_vax_by_age_band]

    for i in range(len(simulated_population_by_age_band)):
        if simulated_population_by_age_band[i]<full_vax_by_age_band[i]:
            difference = full_vax_by_age_band[i]-simulated_population_by_age_band[i]
            full_vax_by_age_band[i] =  full_vax_by_age_band[i] - difference
            full_vax_by_age_band[i+1] +=difference


    print("full_vax_by_age_band:",full_vax_by_age_band)
    print("total number of fully vaccinated people:",sum(full_vax_by_age_band))

    # check that these numbers don't go over the simulated population number
    for i in range(len(simulated_population_by_age_band)):
        if simulated_population_by_age_band[i]<full_vax_by_age_band[i]: 
            print(simulated_population_by_age_band[i])
            print(full_vax_by_age_band[i])
            print("more vaccinated people in this age band than actually exists!:",i)
            exit(1)

    if sum(full_vax_by_age_band)!= total_vaccinated_pop:
        print("incorrect number of total vaccinated people")
        exit(1)

    return vax_1_dose_by_age_band, full_vax_by_age_band

# assigns who give get the doses during the first half of the second year, i.e. booster doses plus new primary doses
# booster_fraction = 0.5 or 0.8 
def booster_and_new_primary_vaccination_allocation(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band, full_vax_by_age_band,booster_fraction):

    total_doses_available = total_population*total_vaccination_rate

    booster_doses = total_doses_available*booster_fraction

    primary_course_doses = (total_doses_available-booster_doses)/2

    # uniform distribution: booster doses 

    if sum(full_vax_by_age_band) !=0:
        vax_3_doses_by_age_band = [round(booster_doses*x/sum(full_vax_by_age_band)) for x in full_vax_by_age_band]
    else:
        vax_3_doses_by_age_band = [0 for x in full_vax_by_age_band]
    vax_2_doses_OG_by_age_band = [a-b for a,b, in zip(full_vax_by_age_band,vax_3_doses_by_age_band)]
    
    
    # uniform distribution: new primary course doses
    unvaxxed_by_age_band = [a-b for a,b, in zip(simulated_population_by_age_band, full_vax_by_age_band)]
    unvaxxed_not_including_youngest = sum(unvaxxed_by_age_band)-unvaxxed_by_age_band [0]

    new_primary_doses_by_age_band = [round(primary_course_doses*unvaxxed_by_age_band[i]/unvaxxed_not_including_youngest) for i in range(len(unvaxxed_by_age_band))]
    new_primary_doses_by_age_band[0] = 0

    for i in range(len(simulated_population_by_age_band)):
        if simulated_population_by_age_band[i]<vax_1_dose_by_age_band[i]+vax_2_doses_OG_by_age_band[i]+vax_3_doses_by_age_band[i]+ new_primary_doses_by_age_band[i]:
            difference = vax_1_dose_by_age_band[i]+vax_2_doses_OG_by_age_band[i]+vax_3_doses_by_age_band[i]+ new_primary_doses_by_age_band[i]-simulated_population_by_age_band[i]
            new_primary_doses_by_age_band[i] = new_primary_doses_by_age_band[i] - difference
            try:
                new_primary_doses_by_age_band[i+1] +=difference
            except:
                print("unused doses:",difference)

    print("vax_1_dose_by_age_band",vax_1_dose_by_age_band)
    print("vax_2_doses_OG_by_age_band",vax_2_doses_OG_by_age_band)
    print("vax_3_doses_by_age_band",vax_3_doses_by_age_band)
    print("new_primary_doses_by_age_band",new_primary_doses_by_age_band)

    vaccinated_all = []
    for i in range(len(simulated_population_by_age_band)):
        vaccinated_all.append(vax_1_dose_by_age_band[i]+vax_2_doses_OG_by_age_band[i]+vax_3_doses_by_age_band[i]+ new_primary_doses_by_age_band[i] )

    print("vaccinated_all",vaccinated_all)
    
    for i in range(len(simulated_population_by_age_band)):
        if simulated_population_by_age_band[i]<vaccinated_all[i]:
            print("more vaccinated people in this age band than actually exists!:",i)
            exit(1)
    
    print("total number of fully vaccinated people after the ultimate end of the simulation (includes people with and without boosters):",sum(vax_2_doses_OG_by_age_band)+sum(vax_3_doses_by_age_band)+sum(new_primary_doses_by_age_band))

    return vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band


# assigns dates of vaccination to the cohort to be vaccinated
def vaccination_schedule(total_population,total_vaccination_rate,simulated_population_by_age_band,vax_1_dose_by_age_band,vax_2_doses_OG_by_age_band,vax_3_doses_by_age_band, new_primary_doses_by_age_band,booster_fraction,original_vax_priority,additional_vax_priority):

    # 6 months per dose stage
    days_per_stage = 7*26 # 26 weeks
    days_between_doses_minimum = 7*4 # 4 weeks
    days_between_booster_dose_minimum = 7*12 # 12 weeks

    first_year_days = 2*days_per_stage

    second_year_half_days = days_per_stage

    ################################################ 

    # total doses to be administered during the first year:
    total_first_doses_to_administer = sum(vax_1_dose_by_age_band) +sum(vax_2_doses_OG_by_age_band)+sum(vax_3_doses_by_age_band)
    total_second_doses_to_administer =sum(vax_2_doses_OG_by_age_band)+sum(vax_3_doses_by_age_band)

    total_first_year_doses = total_first_doses_to_administer + total_second_doses_to_administer 

    doses_per_day_first_year = math.ceil(total_first_year_doses/first_year_days)

    # total doses to be adminstered in the second year (first half):
    # there can be less new primary doses than expected if there is already a high vaccination rate
    total_doses_available = total_population*total_vaccination_rate
    # booster_doses = total_doses_available*booster_fraction
    # primary_course_doses = (total_doses_available-booster_doses)/2

    # total_second_year_half_doses = sum(vax_3_doses_by_age_band) + 2*sum(new_primary_doses_by_age_band)
    total_second_year_half_doses = total_doses_available

    doses_per_day_second_year_half = math.ceil(total_second_year_half_doses/second_year_half_days)


    ###############################################
    # list of all people

    # for each group of { x vaccinations }, create the relevant number of individuals and populate
    # total vaccinations to receive

    # first: the people who will be getting at least one dose during the first year (aka before the second year of the simulation)
    list_of_all_people = []
    for a in range(len(vax_1_dose_by_age_band)):
        age_band = age_bands[a]
        for i in range(vax_1_dose_by_age_band[a]):
            max_vax=1
            infected = False
            next_vax_eligibility_date= 0 
            list_of_all_people.append(Individual(age_band, max_vax,infected,next_vax_eligibility_date))

    for a in range(len(vax_2_doses_OG_by_age_band)):
        age_band = age_bands[a]
        for i in range(vax_2_doses_OG_by_age_band[a]):
            max_vax=2
            infected = False
            next_vax_eligibility_date= 0 
            list_of_all_people.append(Individual(age_band, max_vax,infected,next_vax_eligibility_date))
    
    for a in range(len(vax_3_doses_by_age_band)):
        age_band = age_bands[a]
        for i in range(vax_3_doses_by_age_band[a]):
            max_vax=3
            infected = False
            next_vax_eligibility_date= 0 
            list_of_all_people.append(Individual(age_band, max_vax,infected,next_vax_eligibility_date))
    
    # then the people who will only get a primary dose *later* during the second year of the simulation
    for a in range(len(new_primary_doses_by_age_band)):
        age_band = age_bands[a]
        for i in range(new_primary_doses_by_age_band[a]):
            max_vax=2
            infected = False
            next_vax_eligibility_date = first_year_days
            list_of_all_people.append(Individual(age_band, max_vax,infected,next_vax_eligibility_date))
    
    # lastly, create the people who don't get any dose:
    unvaccinated_pop_by_age_band = []
    for i in range(len(simulated_population_by_age_band)):
        unvaccinated_pop_by_age_band.append(simulated_population_by_age_band[i]-vax_1_dose_by_age_band[i]-vax_2_doses_OG_by_age_band[i]-vax_3_doses_by_age_band[i]-new_primary_doses_by_age_band[i])
    
    for a in range(len(unvaccinated_pop_by_age_band)):
        age_band = age_bands[a]
        for i in range(unvaccinated_pop_by_age_band[a]):
            max_vax=0
            infected = False
            next_vax_eligibility_date = 100000
            list_of_all_people.append(Individual(age_band, max_vax,infected,next_vax_eligibility_date))


    ################################################
    # in the "priority dictionary", we have priority levels 0, 1,2...., defining the most important group/dose-number to give out
    # they also have a max_daily_allocation fraction, aka how many of the day's doses could be assigned to that priority group.

    max_doses_per_level = {}
    for priority_level in original_vax_priority.keys():
        max_doses_per_level[priority_level] = math.ceil(doses_per_day_first_year*original_vax_priority[priority_level]['max_daily_allocation'])

    second_year_half_max_doses_per_level = {}
    for priority_level in additional_vax_priority.keys():
        second_year_half_max_doses_per_level[priority_level] = math.ceil(doses_per_day_second_year_half*additional_vax_priority[priority_level]['max_daily_allocation'])
    ################################################

    # preparing groups for vaccination~
    first_year_ranked_groups = dict()
    for priority_level in original_vax_priority.keys():
        first_year_ranked_groups[priority_level] = [] # to be a list of Individual-indices

    second_year_half_ranked_groups = dict()
    for priority_level in additional_vax_priority.keys():
        second_year_half_ranked_groups[priority_level] = [] # to be a list of Individual-indices

    # inserting people into the ranked groups lists 
    for i in range(len(list_of_all_people)):
        person = list_of_all_people[i]
        if person.max_vax >0:
            if person.next_vax_eligibility_date ==0:
                # find the priority group they should be in
                dose_num = 1
                
                for priority_level in original_vax_priority.keys():
                    if dose_num in original_vax_priority[priority_level]['dose_numbers'] and person.age_band in original_vax_priority[priority_level]['ages']:
                        first_year_ranked_groups[priority_level].append(i)
                        break
            elif person.next_vax_eligibility_date>1:
                # these should be the people getting their first dose in the second year of the simulation
                dose_num = 1

                for priority_level in additional_vax_priority.keys():
                    if dose_num in additional_vax_priority[priority_level]['dose_numbers'] and person.age_band in additional_vax_priority[priority_level]['ages']:
                        second_year_half_ranked_groups[priority_level].append(i)
                        break
    
    # shuffling_days = [days_between_doses_minimum,2*days_between_doses_minimum]

    ################################################

    # FIRST UP: FIRST YEAR OF THE VACCINATION PROGRAM

    for day in range(first_year_days):

        # add in a few random shuffles at certain dates
        if day%days_between_doses_minimum ==0:
            for priority_level in first_year_ranked_groups:
                random.shuffle(first_year_ranked_groups[priority_level])

        doses_per_level_given = {} # to ensure that we don't go over max_doses_per_level per day
        for priority_level in original_vax_priority.keys():
            doses_per_level_given[priority_level] = 0 

        for dose in range(doses_per_day_first_year):
            for priority_level in original_vax_priority.keys():
                if doses_per_level_given[priority_level]==max_doses_per_level[priority_level]:
                    continue
                if len(first_year_ranked_groups[priority_level])==0:
                    continue
                # else

                # finding an eligible person
                eligible = False
                total_people_in_this_group = len(first_year_ranked_groups[priority_level])
                people_checked = 0
                list_of_ineligible_people_to_append = []
                while not eligible:
                    person_index = first_year_ranked_groups[priority_level].pop()
                    person = list_of_all_people[person_index]
                    people_checked+=1
                    if person.max_vax == person.doses_received:
                        print(person.vaccination_days)
                        print(person.max_vax)
                        print(person.doses_received)

                        print("this person shouldn't be on the first_year_rank_groups lists anymore!")
                        exit(1)
                    if person.next_vax_eligibility_date > day:
                        # not yet eligible, add back to list 
                        list_of_ineligible_people_to_append.append(person_index)
                        
                        
                    else:
                        eligible = True # break

                    if people_checked == total_people_in_this_group:
                        break # break out of this while loop
                first_year_ranked_groups[priority_level].extend(list_of_ineligible_people_to_append)

                if people_checked == total_people_in_this_group and not eligible:
                        continue # there is no one in this group that can be vaccinated, move onto the next priority group 
                
                # else: we now have a person to vaccinate! 
                person.doses_received+=1
                person.vaccination_days.append(day)
                doses_per_level_given[priority_level] += 1

                if person.max_vax > person.doses_received:
                    
                    if person.doses_received+1 ==2: # i.e. they need to get in line for a second dose during the first year, then:

                        person.next_vax_eligibility_date = day+days_between_doses_minimum
                        dose_num = 2

                        inserted = False 
                        for level in original_vax_priority.keys():
                            if dose_num in original_vax_priority[level]['dose_numbers'] and person.age_band in original_vax_priority[level]['ages']:
                                first_year_ranked_groups[level].append(person_index)
                                inserted = True
                                break
                        if not inserted:
                            print("unable to insert into first_year_ranked_groups")
                            exit(1)
                    elif person.doses_received+1 ==3: # i.e. they need to get in line for a booster dose in the second year, then:

                        person.next_vax_eligibility_date = day+days_between_booster_dose_minimum
                        dose_num = 3

                        inserted = False    
                        for level in additional_vax_priority.keys():
                            if dose_num in additional_vax_priority[level]['dose_numbers'] and person.age_band in additional_vax_priority[level]['ages']:
                                second_year_half_ranked_groups[level].append(person_index)
                                inserted = True
                                break
                        if not inserted:
                            print("unable to insert into second_year_half_ranked_groups")
                            exit(1)
                        

                # check that the object person has indeed changed:
                # print(list_of_all_people[person_index].vaccination_days)

                break # break because we found a person to vaccinate using this [dose] so we don't need to go through the rest of the priority level groups 


    # check that everyone who should be vaccinated in the first year has been vaccinated:
    for priority_level in first_year_ranked_groups:
        if len(first_year_ranked_groups[priority_level])>0:
            print("not everyone was vaccinated in the first year!")
            print(first_year_ranked_groups[priority_level])
            exit(1)

    ################################################
    
    # NOW FOR THE SECOND YEAR (first half)
    # # (i.e. boosters and new primary doses) 
    
    print(second_year_half_max_doses_per_level)

    for day in range(first_year_days,first_year_days+second_year_half_days):
        # print('day',day)

        # add in a few random shuffles at certain dates
        if day%days_between_doses_minimum ==0:
            for priority_level in second_year_half_ranked_groups:
                random.shuffle(second_year_half_ranked_groups[priority_level])


        doses_per_level_given = {} # to ensure that we don't go over max_doses_per_level per day
        for priority_level in additional_vax_priority.keys():
            doses_per_level_given[priority_level] = 0
        
        for dose in range(doses_per_day_second_year_half):
            for priority_level in additional_vax_priority.keys():
                if doses_per_level_given[priority_level]==second_year_half_max_doses_per_level[priority_level]:
                    continue
                if len(second_year_half_ranked_groups[priority_level])==0:
                    continue
                
                # else

                # finding an eligible person
                eligible = False
                total_people_in_this_group = len(second_year_half_ranked_groups[priority_level])
                people_checked = 0
                list_of_ineligible_people_to_append = []
                while not eligible:
                    person_index = second_year_half_ranked_groups[priority_level].pop()
                    person = list_of_all_people[person_index]
                    people_checked+=1
                    if person.max_vax == person.doses_received:
                        print("this person shouldn't be on the first_year_rank_groups lists anymore!")
                        exit(1)
                    if person.next_vax_eligibility_date > day:
                        # not yet eligible, add back to list 
                        # if person.max_vax ==3:
                        #     print(person.next_vax_eligibility_date)
                        list_of_ineligible_people_to_append.append(person_index)
                    else:
                        eligible = True # break

                    if people_checked == total_people_in_this_group:
                        break # break out of this while loop

                second_year_half_ranked_groups[priority_level].extend(list_of_ineligible_people_to_append)
                
                if people_checked == total_people_in_this_group and not eligible:
                    continue # there is no one in this group that can be vaccinated, move onto the next priority group 
                
                # else: we now have a person to vaccinate! 
                person.doses_received+=1
                person.vaccination_days.append(day)
                doses_per_level_given[priority_level] += 1

                if person.max_vax > person.doses_received: # i.e. they can still get some more doses
                    
                    if person.doses_received+1 ==2: # i.e. they need to get in line for a second primary dose during the second year, then:

                        person.next_vax_eligibility_date = day+days_between_doses_minimum
                        dose_num = 2
                        inserted=False
                        for level in additional_vax_priority.keys():
                            if dose_num in additional_vax_priority[level]['dose_numbers'] and person.age_band in additional_vax_priority[level]['ages']:
                                second_year_half_ranked_groups[level].append(person_index)
                                inserted=True
                                break
                        if not inserted:
                            print("unable to insert into second_year_half_ranked_groups")
                            exit(1)
                    elif person.doses_received+1 ==3: # i.e. they need to get in line for a booster dose in the second year, then:

                        person.next_vax_eligibility_date = day+days_between_booster_dose_minimum
                        dose_num = 3
                        inserted=False
                        for level in additional_vax_priority.keys():
                            if dose_num in additional_vax_priority[level]['dose_numbers'] and person.age_band in additional_vax_priority[level]['ages']:
                                second_year_half_ranked_groups[level].append(person_index)
                                inserted=True
                                break
                        if not inserted:
                            print("unable to insert into second_year_half_ranked_groups")
                            exit(1)

                # check that the object person has indeed changed:
                # print(list_of_all_people[person_index].vaccination_days)

                break # break because we found a person to vaccinate using this [dose] so we don't need to go through the rest of the priority level groups 
        
        # print(doses_per_level_given)
    
    # check that everyone who should be vaccinated in the second year (first half) has been vaccinated:
    for priority_level in second_year_half_ranked_groups:
        if len(second_year_half_ranked_groups[priority_level])>0:
            print("not everyone was vaccinated in the second year (first half)!")
            print("priority level",priority_level)
            print(len(second_year_half_ranked_groups[priority_level]))
            exit(1)

    return list_of_all_people

# outputs the details of each person with their vaccination schedule (which can be no vaccination)
def output_schedule(list_of_all_people,file):

    # note that "infection" and "infection_day" were to add potential pre-defined dates for infections, not used for the paper
    header =['age_band','num_people','max_vax','time_1','time_2','time_3','infection','infection_day']
    
    with open(file, 'w', newline='') as f:
    # create the csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for person in list_of_all_people:
            num = 1
            vax_days = person.vaccination_days.copy()
            while len(vax_days)<3:
                vax_days.append(-1)
        
            row = [age_band_id[person.age_band],num ,person.max_vax,vax_days[0],vax_days[1],vax_days[2], int(person.infected),person.infected_day] 
            writer.writerow(row)
            # write a row to the csv file

def vaccination_schedule_boosters(list_of_all_people,booster_uptake_probability,boosters_vax_priority,vaccination_start, vaccination_duration):

    if vaccination_start ==-1:
        print("no fourth boosters are given")
        # no fourth boosters are given
        return list_of_all_people

    days_between_doses_minimum = 7*4 # 4 weeks

    people_receiving_boosters = dict()
    for priority_level in boosters_vax_priority.keys():
        people_receiving_boosters[priority_level] = [] # to be a list of Individual-indices

    total_people_receiving_boosters = 0
    
    two_dose_already_group = {}
    three_dose_already_group = {}
    for age_band in age_bands:
        two_dose_already_group[age_band] = []
        three_dose_already_group[age_band] = []

    for i in range(len(list_of_all_people)):
        person = list_of_all_people[i]
        if person.doses_received==2:
            two_dose_already_group[person.age_band].append(i)
        elif person.doses_received ==3:
            three_dose_already_group[person.age_band].append(i)

    for age_band in age_bands:
        random.shuffle(two_dose_already_group[age_band])
        random.shuffle(three_dose_already_group[age_band])

    to_boost =  [] 
    for age_band in age_bands:
        to_boost.extend(two_dose_already_group[age_band][0:int(booster_uptake_probability*len(two_dose_already_group[age_band]))])
        to_boost.extend(three_dose_already_group[age_band][0:int(booster_uptake_probability*len(three_dose_already_group[age_band]))])


    for i in to_boost:
        person = list_of_all_people[i]

        person.max_vax = person.max_vax +1
        person.next_vax_eligibility_date =  person.vaccination_days[-1] + days_between_doses_minimum

        # find the priority group they should be in
        dose_num = person.doses_received + 1
    
        for priority_level in boosters_vax_priority.keys():
            if dose_num in boosters_vax_priority[priority_level]['dose_numbers'] and person.age_band in boosters_vax_priority[priority_level]['ages']:
                people_receiving_boosters[priority_level].append(i)
                total_people_receiving_boosters +=1
                break

    doses_per_day = math.ceil(total_people_receiving_boosters/ vaccination_duration)
    print("doses_per_day: ", doses_per_day)

    extended_max_doses_per_level = {}
    for priority_level in boosters_vax_priority.keys():
        extended_max_doses_per_level[priority_level] = math.ceil(doses_per_day*boosters_vax_priority[priority_level]['max_daily_allocation'])

    # add in a few random shuffles
    for priority_level in people_receiving_boosters:
        random.shuffle(people_receiving_boosters[priority_level])

    number_of_people_vaccinated = 0
    for day in range(vaccination_start,vaccination_start+vaccination_duration):

        doses_per_level_given = {} # to ensure that we don't go over max_doses_per_level per day
        for priority_level in boosters_vax_priority.keys():
            doses_per_level_given[priority_level] = 0 

        

        for dose in range(doses_per_day):
            for priority_level in boosters_vax_priority.keys():
                if doses_per_level_given[priority_level]==extended_max_doses_per_level[priority_level]:
                    continue
                if len(people_receiving_boosters[priority_level])==0:
                    continue
                # else

                # finding an eligible person
                eligible = False
                total_people_in_this_group = len(people_receiving_boosters[priority_level])
                people_checked = 0
                list_of_ineligible_people_to_append = []
                while not eligible:
                    person_index = people_receiving_boosters[priority_level].pop()
                    person = list_of_all_people[person_index]
                    people_checked+=1
                    if person.max_vax == person.doses_received:
                        print("this person shouldn't be on the people_receiving_boosters lists anymore!")
                        exit(1)
                    if person.next_vax_eligibility_date > day: # too early for the next dose
                        list_of_ineligible_people_to_append.append(person_index)
                    else:
                        eligible = True # break

                    if people_checked == total_people_in_this_group:
                        break # break out of this while loop

                people_receiving_boosters[priority_level].extend(list_of_ineligible_people_to_append)
                
                if people_checked == total_people_in_this_group and not eligible:
                    continue # there is no one in this group that can be vaccinated, move onto the next priority group 

                # else: we now have a person to vaccinate! 
                number_of_people_vaccinated+=1
                person.doses_received+=1
                person.vaccination_days.append(day)
                doses_per_level_given[priority_level] += 1
    print("number_of_people_vaccinated: ",number_of_people_vaccinated)
    # check that everyone who should be vaccinated in the second year (first half) has been vaccinated:
    for priority_level in people_receiving_boosters:
        if len(people_receiving_boosters[priority_level])>0:
            print("not everyone was vaccinated during the extended period!")
            print("priority level",priority_level)
            print(len(people_receiving_boosters[priority_level]))
            exit(1)


    return list_of_all_people


def vaccination_schedule_annual_boosters(list_of_all_people,second_additional_doses_available,boosters_vax_priority,vaccination_start, vaccination_duration):

    if vaccination_start ==-1:
        print("no fourth boosters are given")
        # no fourth boosters are given
        return list_of_all_people

    days_between_doses_minimum = 7*4 # 4 weeks # don't need this, since the time frames are long enough 


    people_who_could_be_receiving_boosters = dict()
    for priority_level in boosters_vax_priority.keys():
        people_who_could_be_receiving_boosters[priority_level] = [] # to be a list of Individual-indices



    # inserting people into the ranked groups lists 
    for i in range(len(list_of_all_people)):
        person = list_of_all_people[i]
        if person.doses_received >1: # this means they've been vaccinated; so they're egilible for boosting 
            for priority_level in boosters_vax_priority.keys():
                if person.doses_received+1 in boosters_vax_priority[priority_level]['dose_numbers'] and person.age_band in boosters_vax_priority[priority_level]['ages']:
                    people_who_could_be_receiving_boosters[priority_level].append(i)
                    break
           

    for priority_level in boosters_vax_priority.keys():
        random.shuffle(people_who_could_be_receiving_boosters[priority_level])

    boosting_program_days = list(range(vaccination_start,vaccination_start+vaccination_duration))
    doses_per_day = math.ceil(second_additional_doses_available/vaccination_duration)
    number_of_people_vaccinated = 0 
    print("doses_per_day: ", doses_per_day)

    extended_max_doses_per_level = {}
    for priority_level in boosters_vax_priority.keys():
        extended_max_doses_per_level[priority_level] = math.ceil(doses_per_day*boosters_vax_priority[priority_level]['max_daily_allocation'])

    for day in boosting_program_days:
        doses_per_level_given = {} # to ensure that we don't go over max_doses_per_level per day
        for priority_level in boosters_vax_priority.keys():
            doses_per_level_given[priority_level] = 0 
    
        for dose in range(doses_per_day):
            if number_of_people_vaccinated>=second_additional_doses_available:
                break
            for priority_level in boosters_vax_priority.keys():
                if doses_per_level_given[priority_level]>=extended_max_doses_per_level[priority_level]:
                    continue
                if len(people_who_could_be_receiving_boosters[priority_level])==0:
                    continue
                # else

                # all people in the list are eligible, no checking needed 
                person_index = people_who_could_be_receiving_boosters[priority_level].pop()
                person = list_of_all_people[person_index]


                person.max_vax = person.max_vax +1
                person.next_vax_eligibility_date =  person.vaccination_days[-1] + days_between_doses_minimum
                number_of_people_vaccinated+=1
                person.doses_received+=1
                person.vaccination_days.append(day)
                doses_per_level_given[priority_level] += 1

                break 

    print("number_of_people_vaccinated during annual boosting: ",number_of_people_vaccinated)

    return list_of_all_people
    
def vaccination_schedule_additional_primary(list_of_all_people,second_additional_doses_available,boosters_vax_priority,vaccination_start, vaccination_duration): # TODO IN PROGRESS

    if vaccination_start ==-1:
        print("no fourth boosters are given")
        # no fourth boosters are given
        return list_of_all_people

    days_between_doses_minimum = 7*4 

    total_people_who_can_be_fully_vaccinated = math.floor(second_additional_doses_available/2)


    people_who_could_be_receiving_primary_doses = dict()
    for priority_level in boosters_vax_priority.keys():
        people_who_could_be_receiving_primary_doses[priority_level] = [] # to be a list of Individual-indices



    # inserting people into the ranked groups lists 
    for i in range(len(list_of_all_people)):
        person = list_of_all_people[i]
        if person.doses_received ==0: # this means they've never vaccinated; so they're egilible for vaccination
            for priority_level in boosters_vax_priority.keys():
                if person.doses_received+1 in boosters_vax_priority[priority_level]['dose_numbers'] and person.age_band in boosters_vax_priority[priority_level]['ages']:
                    people_who_could_be_receiving_primary_doses[priority_level].append(i)
                    break
           

    for priority_level in boosters_vax_priority.keys():
        random.shuffle(people_who_could_be_receiving_primary_doses[priority_level])

    assignments_remaining = total_people_who_can_be_fully_vaccinated
    people_who_will_be_receiving_primary_doses = dict()
    for priority_level in boosters_vax_priority.keys():
        if len(people_who_could_be_receiving_primary_doses[priority_level])<= assignments_remaining:

            people_who_will_be_receiving_primary_doses[priority_level] = people_who_could_be_receiving_primary_doses[priority_level]
            assignments_remaining = assignments_remaining-len(people_who_could_be_receiving_primary_doses[priority_level])
        elif assignments_remaining>0:
            people_who_will_be_receiving_primary_doses[priority_level] = people_who_could_be_receiving_primary_doses[priority_level][:assignments_remaining]
            assignments_remaining=0
        else:
            people_who_will_be_receiving_primary_doses[priority_level] = []
    print("assignments_remaining:",assignments_remaining)


    boosting_program_days = list(range(vaccination_start,vaccination_start+vaccination_duration))
    doses_per_day = math.ceil(second_additional_doses_available/vaccination_duration)
    number_of_people_vaccinated = 0 
    doses_delivered = 0
    print("doses_per_day: ", doses_per_day)

    extended_max_doses_per_level = {}
    for priority_level in boosters_vax_priority.keys():
        extended_max_doses_per_level[priority_level] = math.ceil(doses_per_day*boosters_vax_priority[priority_level]['max_daily_allocation'])

    halfway_day = (boosting_program_days[0]+boosting_program_days[-1])/2

    for day in boosting_program_days:
        doses_per_level_given = {} # to ensure that we don't go over max_doses_per_level per day
        for priority_level in boosters_vax_priority.keys():
            doses_per_level_given[priority_level] = 0 
    
        for dose in range(doses_per_day):
            if number_of_people_vaccinated>=second_additional_doses_available:
                break
            for priority_level in boosters_vax_priority.keys():
                if doses_per_level_given[priority_level]>=extended_max_doses_per_level[priority_level]:
                    continue
                if len(people_who_will_be_receiving_primary_doses[priority_level])==0:
                    continue
                # else

                # finding an eligible person
                eligible = False
                total_people_in_this_group = len(people_who_will_be_receiving_primary_doses[priority_level])
                people_checked = 0
                list_of_ineligible_people_to_append = []
                while not eligible:
                    person_index = people_who_will_be_receiving_primary_doses[priority_level].pop()
                    person = list_of_all_people[person_index]
                    people_checked+=1
                    if person.doses_received==0:
                        eligible=True
                    elif person.doses_received==1 and person.next_vax_eligibility_date <= day and day >=halfway_day :
                        eligible= True
                    else:
                        list_of_ineligible_people_to_append.append(person_index)

                    if people_checked == total_people_in_this_group:
                        break # break out of this while loop

                people_who_will_be_receiving_primary_doses[priority_level].extend(list_of_ineligible_people_to_append)

                if people_checked == total_people_in_this_group and not eligible:
                    continue # there is no one in this group that can be vaccinated, move onto the next priority group 
                
                # else: we now have a person to vaccinate!
                person.doses_received+=1
                person.vaccination_days.append(day)
                doses_per_level_given[priority_level] += 1
                doses_delivered +=1

                if person.doses_received ==1: # aka they need to get a second dose too
                    person.max_vax = 2
                    person.next_vax_eligibility_date =  day + days_between_doses_minimum

                    dose_num = 2

                    inserted = False 
                    for level in boosters_vax_priority.keys():
                        if dose_num in boosters_vax_priority[level]['dose_numbers'] and person.age_band in boosters_vax_priority[level]['ages']:
                            people_who_will_be_receiving_primary_doses[level].append(person_index)
                            inserted = True
                            break
                    if not inserted:
                        print("unable to insert into people_who_will_be_receiving_primary_doses")
                        exit(1)
                elif person.doses_received==2:
                    number_of_people_vaccinated+=1
                break 
    
    print("doses_delivered :",doses_delivered )
    print("number_of_people_vaccinated during annual boosting: ",number_of_people_vaccinated)

    return list_of_all_people

    


def output_schedule_extended(list_of_all_people,file):
    # note that "infection" and "infection_day" were to add potential pre-defined dates for infections, not used for the paper
    header =['age_band','num_people','max_vax','time_1','time_2','time_3', 'time_4','infection','infection_day']

    dict_collected_details = {}

    for person in list_of_all_people:
        vax_days = person.vaccination_days.copy()
        while len(vax_days)<4:
            vax_days.append(-1)
        person_details = (age_band_id[person.age_band],person.max_vax,vax_days[0],vax_days[1],vax_days[2], vax_days[3],int(person.infected),person.infected_day) 
        if person_details in dict_collected_details :
            dict_collected_details[person_details] = dict_collected_details[person_details] +1
        else:
            dict_collected_details[person_details] = 1

    
    with open(file, 'w', newline='') as f:
    # create the csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for person_details, num_people in dict_collected_details.items():
            row =  [person_details[0],num_people ,person_details[1],person_details[2],person_details[3],person_details[4],person_details[5],person_details[6],person_details[7]] 
            writer.writerow(row)

        # for person in list_of_all_people:
        #     num = 1
        #     vax_days = person.vaccination_days.copy()
        #     while len(vax_days)<4:
        #         vax_days.append(-1)
        
        #     row = [age_band_id[person.age_band],num ,person.max_vax,vax_days[0],vax_days[1],vax_days[2], vax_days[3],int(person.infected),person.infected_day] 
        #     writer.writerow(row)
        #     # write a row to the csv file
