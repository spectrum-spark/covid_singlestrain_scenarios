import csv
import os

header =['age_band','num_people','max_vax','infection']

folder = "winter_wave_scenarios"
filename = "vax_infect_scenario1.csv"
file = os.path.join(os.path.dirname(__file__), folder , filename)

# open the file in the write mode
with open(file, 'w', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
    
    rows = []

    for age_band in range(1,18):
        for infection in [0,1]:
            for max_vax in [0,1,2]:
                num_people = 980 # make this more complicated in the future if necessary
                # or even just hand/hard code the input
                row = [age_band,num_people ,max_vax,infection]
                rows.append(row)

                # write a row to the csv file
    writer.writerows(rows)