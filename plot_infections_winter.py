from matplotlib import rc
rc('text', usetex=True)
rc('font', **{'family': 'serif'})

import matplotlib.pyplot as plt
plt.switch_backend('agg')

import os
import sys
# import csv
import pandas as pd
import numpy as np


folder = sys.argv[1]
file = sys.argv[2]

# filename = "initial-and-during_vax_infect_scenario1_sim_params_v1_NA.csv"
filename = file + ".csv"
population_type = "younger"

if population_type =="younger":
    plotting_colour =  "lightskyblue"
    
elif population_type=="older":
    plotting_colour =  "lightcoral"

data_file = os.path.join(folder, filename)

pd_obj = pd.read_csv(data_file)
# print(pd_obj)


new_pd = pd_obj.groupby(['day','sim'],as_index=False).n.sum()
df = new_pd.pivot(index='day', columns='sim', values='n')
df.plot()

plt.savefig(os.path.join(folder, filename+"_infections_over_time.png") , bbox_inches='tight')
plt.close()

# plt.show()

# print(df) # has vairous NaN....
print(df.mean(axis='columns'))
df_mean = df.mean(axis='columns')
df_median = df.median(axis='columns')
df_quantile = df.quantile(0.025,axis='columns')
df_quantile_upper = df.quantile(0.975,axis='columns')
# print(df_quantile)
print(df_mean.axes)



fig, ax = plt.subplots(1,1, figsize=(10,6))

ax.plot(df_median,color = "black")
ax.fill_between([212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224,
            225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237,
            238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250,
            251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263,
            264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276,
            277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289,
            290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302],df_quantile,df_quantile_upper,color =plotting_colour)

ax.set_xlabel('time (days)')
ax.set_ylabel('number of infections')
ax.set_title('"winter" covid wave ')

plt.savefig(os.path.join(folder, filename+"_infections_over_time_median.png") , bbox_inches='tight')
plt.close()

# f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row',figsize=(10, 6))
# ax_combined = [ax1,ax2,ax3,ax4]
# f.tight_layout()
# plt.rcParams['mathtext.fontset'] = 'dejavuserif'
# linestyles = [':', '-.', '--', '-']