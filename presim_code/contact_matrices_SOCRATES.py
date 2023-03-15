# produces the averaged contact matrices used

import os
import csv
import numpy as np

older_files = ["20220503013225_social_contact_matrix_Belgium2006.csv","20220503013251_social_contact_matrix_Belgium2010.csv","20220503013310_social_contact_matrix_Finland2008.csv","20220503013334_social_contact_matrix_France2015.csv","20220503013352_social_contact_matrix_Germany2008.csv","20220503013405_social_contact_matrix_HongKong2017.csv","20220503013434_social_contact_matrix_Italy2008.csv","20220503013448_social_contact_matrix_Luxembourg2008.csv","20220503013535_social_contact_matrix_Poland2008.csv"]
younger_files = ["20220503013752_social_contact_matrix_Vietnam2007.csv","20220503013818_social_contact_matrix_Zimbabwe2013.csv"]

files = {'older':older_files,'younger':younger_files}
countries_contact_matrices = {'younger':{},'older':{}}
for population_type in ['younger','older']:
    for country_file in files[population_type]:
        print(country_file)
        filename =  os.path.join(os.path.dirname(__file__),'contact_matrices',country_file)
        contact_matrix = []
        with open(filename) as csvfile:
            reader = csv.reader(csvfile,quoting=csv.QUOTE_NONNUMERIC)
            next(reader)
            for data in reader:
                contact_matrix.append(data)
        countries_contact_matrices[population_type][country_file] = contact_matrix
        

average_contact_matrix = dict()
for population_type in ['younger','older']:
    arr = [countries_contact_matrices[population_type][country] for country in countries_contact_matrices[population_type]]
    # print(np.mean( np.array(arr), axis=0))
    average_contact_matrix[population_type] = np.mean( np.array(arr), axis=0)

# print(average_contact_matrix)

for population_type in ['younger','older']:
    csvfile =  os.path.join(os.path.dirname(__file__),'contact_matrix_SOCRATES_' + population_type +'.csv')
    with open(csvfile, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerows(average_contact_matrix[population_type])

