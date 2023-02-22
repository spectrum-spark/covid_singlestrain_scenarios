# plots the contact matrices for the paper

import os
import numpy as np
import matplotlib.pylab as plt
from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'sans-serif'})
plt.switch_backend('agg')

age_bands_used = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
# 0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80

for population_type in ['younger','older']:
    csvfile =  os.path.join(os.path.dirname(__file__),'contact_matrix_SOCRATES_' + population_type +'.csv')
    with open(csvfile, 'r') as f:
        array = np.loadtxt(f, delimiter=",")

        fig, ax = plt.subplots(1,1, figsize=(6,6))

        img = ax.imshow(array, cmap='YlOrRd', interpolation='nearest', vmin=0, vmax=10) # 
        if population_type=='older':
            ax.set_title('contact matrix for an ' + population_type +' population')
        else:
            ax.set_title('contact matrix for a ' + population_type +' population')
        ax.set_xticks(list(range(0,17)))
        ax.set_yticks(list(range(0,17)))
        ax.set_xticklabels(age_bands_used, rotation = 90)
        ax.set_yticklabels(age_bands_used)
        ax.set_xlabel("age of participant (year)")
        ax.set_ylabel("age of contact")
        # for i in range(17):
        #     for j in range(17):
        #         text = ax.text(j, i, round(array[i, j],3), ha="center", va="center", color="w")
        ax.invert_yaxis()
        fig.colorbar(img,fraction=0.046, pad=0.04)
        plt.savefig( os.path.join(os.path.dirname(__file__), "contact_matrix_" + population_type+".png"), bbox_inches='tight')
        plt.close()