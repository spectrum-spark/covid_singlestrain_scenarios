import csv
import os
import numpy as np

from Individual import *
# from create_and_generate_initial_conditions import *
# from create_and_generate_initial_conditions_plotting import *
from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'sans-serif'})
import matplotlib.pyplot as plt
plt.switch_backend('agg')

age_bands = ["0-4","5-11","12-15",'16-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
age_band_id = {"0-4":1,"5-11":2,"12-15":3,'16-19':4, '20-24':5, '25-29':6, '30-34':7, '35-39':8, '40-44':9, '45-49':10, '50-54':11, '55-59':12, '60-64':13, '65-69':14, '70-74':15, '75-79':16, '80+':17}

OG_vaccination_time = 7*26*3 # 1.5 years, approximately

OG_earlier_boosting_time_start = 637

six_months = 7*26

days_between_doses_minimum = 7 * 4  # 4 weeks
days_between_booster_dose_minimum = 7 * 12  # 12 weeks


folder = "parameter_files_annual_boosting_2"
folder_path = os.path.join(os.path.dirname(__file__),folder)
if not os.path.exists(folder_path ):
  os.makedirs(folder_path )


input_folder_path =  os.path.join(os.path.dirname(__file__),"parameter_files_annual_boosting_1")
input_paranum = "3"


def output_schedule_extended_6_boosters(list_of_all_people, file):
    # note that "infection" and "infection_day" were to add potential pre-defined dates for infections, not used for the paper
    header = ['age_band', 'num_people', 'max_vax', 'time_1', 'time_2', 'time_3', 'time_4','time_5','time_6', 'infection', 'infection_day']

    dict_collected_details = {}

    for person in list_of_all_people:
        vax_days = person.vaccination_days.copy()
        while len(vax_days) < 6:
            vax_days.append(-1)

        person_details = (
        age_band_id[person.age_band], person.max_vax, vax_days[0], vax_days[1], vax_days[2], vax_days[3],vax_days[4],vax_days[5],
        int(person.infected), person.infected_day)
        if person_details in dict_collected_details:
            dict_collected_details[person_details] = dict_collected_details[person_details] + 1
        else:
            dict_collected_details[person_details] = 1

    with open(file, 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for person_details, num_people in dict_collected_details.items():
            row = [person_details[0], num_people, person_details[1], person_details[2], person_details[3],
                   person_details[4], person_details[5], person_details[6], person_details[7],person_details[8],person_details[9]]
            writer.writerow(row)


def plot_vaccination_distributions_extended_percentage_pretty_6_boosters(list_of_all_people,plotting_name, total_vaccination_rate):


    dose_numbers = {0: {}, 1: {}, 2: {}, 3: {}, 4: {},5:{},6:{}}
    for dose in range(0, 7):
        for age_band in age_bands:
            dose_numbers[dose][age_band] = 0
    simulated_population_by_age_band = [0]*len(age_bands)
    for person in list_of_all_people:
        dose_numbers[person.doses_received][person.age_band] += 1
        simulated_population_by_age_band[age_band_id[person.age_band]-1]+=1

    print(dose_numbers)

    fig, ax2 = plt.subplots(1, 1, figsize=(4, 5))

    y_pos = np.arange(len(age_bands))

    dose_numbers_index = [2,3,4,5,6,0]
    colour_list = ["yellowgreen","forestgreen","darkgreen", "lightblue", "darkblue", "peachpuff"]

    left = [0]*len(age_bands)
    for dose_index,colour in zip(dose_numbers_index,colour_list):
        people_with_doses = [dose_numbers[dose_index][age_band] for age_band in age_bands]
        percentage = [100 * x / y for x, y, in zip(people_with_doses, simulated_population_by_age_band)]
        ax2.barh(y_pos, percentage,left=left, color=colour)

        left = [sum(x) for x in zip(left, percentage)]



    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(age_bands)
    ax2.set_xlabel('Vaccination coverage percentage')
    ax2.set_title('1st year vaccination coverage: ' + str(round(100 * total_vaccination_rate, 0)) + "\%", fontsize=14)

    x_ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels([str(x) + "\%" for x in x_ticks])

    ax2.legend(["Primary course only", "Primary + 1 Booster", "Primary + 2 Boosters", "Primary + 3 Boosters","Primary + 4 Boosters", "Unvaccinated"],
               bbox_to_anchor=(1.04, 0), loc="lower left", borderaxespad=0, frameon=False, handlelength=0.7)

    ax2.xaxis.grid()
    ax2.set_axisbelow(True)
    ax2.set_ylim([-0.4, 16.4])
    ax2.set_xlim([0, 100])

    # plt.tight_layout()
    plt.savefig(plotting_name + "_vaxxed_pop_by_age_band_pretty_extended.png", bbox_inches='tight')
    plt.close()


def plot_vaccination_distributions_time_pretty_6_boosters(list_of_all_people, plotting_name):
    #############################
    total_sim_days = 1200
    number_of_doses_per_day = [0] * total_sim_days
    total_of_dose_N_per_day = [[0] * total_sim_days, [0] * total_sim_days, [0] * total_sim_days, [0] * total_sim_days, [0] * total_sim_days, [0] * total_sim_days]
    number_of_doses_per_day_by_age = dict()
    for age_band in age_bands:
        number_of_doses_per_day_by_age[age_band] = [0] * total_sim_days

    max_day = 0
    for person in list_of_all_people:
        for i in range(len(person.vaccination_days)):
            day = person.vaccination_days[i]
            number_of_doses_per_day[day] += 1
            total_of_dose_N_per_day[i][day] += 1
            number_of_doses_per_day_by_age[person.age_band][day] += 1

            if day > max_day:
                max_day = day

    # plot by day
    days = list(range(1, total_sim_days + 1))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

    doses_N_per_day_index = list(range(0,6))
    colour_list = ['lightskyblue',"deepskyblue","steelblue","darkblue","lightgreen","darkgreen"]
    bottom = [0]*len(total_of_dose_N_per_day[0])

    for dose_N_index, colour in zip(doses_N_per_day_index,colour_list):
        ax1.bar(days, total_of_dose_N_per_day[dose_N_index], bottom=bottom, color=colour, width=1)
        bottom =  [sum(x) for x in zip(bottom,total_of_dose_N_per_day[dose_N_index])]


    ax1.legend(["first doses", "second doses", "first boosters", "second boosters","third boosters","fourth boosters"], bbox_to_anchor=(1.01, 1.0),
               loc='upper left', handlelength=0.7, title="dose number")  # (1.04, 1.0)


    ax1.set_ylabel('doses')

    prior_sum = [0] * total_sim_days

    ax2.set_prop_cycle(plt.cycler('color', plt.cm.inferno(np.linspace(0, 1, len(age_bands)))))

    for age in age_bands:
        ax2.bar(days, number_of_doses_per_day_by_age[age], bottom=prior_sum, width=1)
        prior_sum = [sum(x) for x in zip(prior_sum, number_of_doses_per_day_by_age[age])]

    ax2.legend(age_bands, title="age band", bbox_to_anchor=(1.01, 1.0), loc="upper left", borderaxespad=0, ncol=2,
               handlelength=0.7)
    ax2.set_xlabel('time (days)')
    # ax2.set_title('Doses given out each day: by age group')

    ax2.set_ylabel('doses')

    ax1.set_xlim([0, max(max_day, 546)])
    ax2.set_xlim([0, max(max_day, 546)])

    plt.savefig(plotting_name + "_vax_by_day_dose_group.png", bbox_inches='tight')
    plt.close()


def total_doses_per_time_period(list_of_all_people):
    # upper range 
    total_doses_time_range = {six_months*3+1:0,six_months*4:0 ,six_months*5:0,six_months*6:0,six_months*7:0 }
    for person in list_of_all_people:
        vax_days = person.vaccination_days.copy()
        for vax_day in vax_days:
            for upper_date in total_doses_time_range.keys():
                if vax_day < upper_date:
                    total_doses_time_range[upper_date]+=1
                    break
    
    print(total_doses_time_range)



for younger_or_older in ["younger","older"]:
    input_file_name = "abm_continuous_simulation_parameters_" + younger_or_older+"_" + input_paranum +".csv"

    full_input_file_name = os.path.join(input_folder_path,input_file_name)

    list_of_all_people = []


    with open(full_input_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                print(f'Column names are {", ".join(row)}')
                # age_band,num_people,max_vax,time_1,time_2,time_3,time_4,infection,infection_day
            else:
                age_band, num_people, max_vax, time_1, time_2, time_3, time_4, infection, infection_day = row
                num_people = int(num_people)

                max_vax = int(max_vax)
                time_1 = int(time_1)
                time_2 = int(time_2)
                time_3 = int(time_3)
                time_4 = int(time_4)
                infection = int(infection)
                infection_day = int(infection_day)

                time_5 = -1
                time_6 = -1
                if max_vax ==3: # i.e. these people have received boosters
                    # figure out when they received a booster, to see if they received it during the [first] additional boosting period
                    if time_3 >=OG_earlier_boosting_time_start:
                        max_vax = max_vax+2 # should be 5 now
                        time_4 = time_3 + six_months
                        time_5 = time_4 + six_months
                        next_vax_eligibility_date = time_5+days_between_booster_dose_minimum
                    else:
                        next_vax_eligibility_date = time_3+days_between_booster_dose_minimum
                elif max_vax==4:
                    # these people definitely received a booster during the [first] additional boosting period
                    max_vax = max_vax+2
                    time_5 = time_4 + six_months
                    time_6 = time_5 + six_months
                    next_vax_eligibility_date = time_6 + days_between_booster_dose_minimum
                elif max_vax ==2:
                    next_vax_eligibility_date = time_2 + days_between_booster_dose_minimum
                else:
                    next_vax_eligibility_date = 0

                infected = False # should all be false
                age_band_range = ""

                age_band_id = {"0-4": 1, "5-11": 2, "12-15": 3, '16-19': 4, '20-24': 5, '25-29': 6, '30-34': 7,
                               '35-39': 8, '40-44': 9, '45-49': 10, '50-54': 11, '55-59': 12, '60-64': 13, '65-69': 14,
                               '70-74': 15, '75-79': 16, '80+': 17}
                for key,value in age_band_id.items():
                    if value ==int(age_band):
                        age_band_range = key
                        break

                for number in range(num_people):

                    person = Individual(age_band_range, max_vax, infected, next_vax_eligibility_date)
                    person.doses_received = max_vax
                    person.infected_day = -1
                    person.vaccination_days = [time_1, time_2,time_3,time_4,time_5, time_6][:max_vax]  # days on which this individual gets vaccinated

                    list_of_all_people.append(person)

    full_output_file_name =  os.path.join(folder_path, "abm_continuous_simulation_parameters_" + younger_or_older + ".csv")
    output_schedule_extended_6_boosters(list_of_all_people, full_output_file_name)


    output_file = os.path.join(folder_path, "abm_continuous_simulation_parameters_" + younger_or_older)
    plot_vaccination_distributions_extended_percentage_pretty_6_boosters(list_of_all_people, output_file, 0.8)

    plot_vaccination_distributions_time_pretty_6_boosters(list_of_all_people, output_file)

    #as a third sanity check, calculate the number of doses given out during each boosting interval / the total number of doses given out across the three latter boosting intervals
    total_doses_per_time_period(list_of_all_people)


