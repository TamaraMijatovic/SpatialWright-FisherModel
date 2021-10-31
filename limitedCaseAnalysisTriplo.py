# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 15:05:16 2021

@author: leand
"""

from limitedCaseFileIO import FileIO
import time
import measureBlotchiness as mB
import matplotlib.pyplot as plt
import numpy as np


#%% ANALYSIS FOR A SINGLE TRIPLO

t0 = time.time()

FILEIO = [FileIO() for i in range(0,3)]
filenames = ["run1.txt", "run2.txt", "run3.txt"]

for f_i,fileIO in enumerate(FILEIO):
    
    fileIO.set_filename(filenames[f_i])
    fileIO.read_all_and_remember_in_brain()

t1 = time.time()
print(t1-t0)

#%% helpers

B_mean = []
B_mean_mean = []

#%% Measure

start_batch_0 = 150

stop_batch_0 = start_batch_0 + 50


BLOTCHINESS = []
BLOTCHINESS_TRANSPOSE = []
BLOTCHINESS_MEAN = []

for f_i, fileIO in enumerate(FILEIO):
    
    measurer = mB.BlotchinessMeasurer()
    
    blotchiness = [[] for b in range(start_batch_0, stop_batch_0)]
    
    for i, n in enumerate(range(start_batch_0, stop_batch_0)):
        
        print("getting slice", n, "operation", i, "/", stop_batch_0 - start_batch_0)
        
        part = fileIO.get_slice_brain(n)
        info = part[:2]
        data = part[2]
        
        for t, b_t in enumerate(data):
            blotchiness[i].append(measurer.measure_squared_distance_neighbors(b_t))
    
    
    blotchiness_transpose = np.transpose(blotchiness)
    blotchiness_mean = np.mean(blotchiness, (0))
    
    BLOTCHINESS.append(blotchiness)
    BLOTCHINESS_TRANSPOSE.append(blotchiness_transpose)
    BLOTCHINESS_MEAN.append(blotchiness_mean)

BLOTCHINESS_MEAN_MEAN = np.mean(BLOTCHINESS_MEAN, (0))

B_mean.append(np.transpose(BLOTCHINESS_MEAN))
B_mean_mean.append(BLOTCHINESS_MEAN_MEAN)

#%% Plotting



plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), np.transpose(BLOTCHINESS_MEAN), color='gray', linewidth = 1.5)
plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), BLOTCHINESS_MEAN_MEAN, color='red', label='c = 0.001')

plt.title("Triplo: Evolution of distance from neighbors over 1000 generations")
    
plt.xlabel("generations")
plt.ylabel('clustering measure, $\mu$')

plt.legend()


plt.savefig('plot_c1.png', dpi=300, bbox_inches='tight')
plt.show()

# for f_i, fileIO in enumerate(FILEIO):
#     # plt.plot(range(0, len(blotchiness_mean)), blotchiness_transpose, color='gray', linewidth = 0.1)
#     plt.plot(range(0, len(blotchiness_mean)), \
#              blotchiness_mean, \
#              color = col_mean[batch_nr], \
#              label="c="+str(c[batch_nr]))
    
        
#     plt.title("Evolution of distance from neighbors over 1000 generations, multiple c")
    
#     plt.xlabel("generations")
#     plt.ylabel('clustering measure, $\mu$')
#     plt.legend()
# plt.show()

#%% Plotting all together


plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean[0], color = 'gray', linewidth = 1.5)
plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean_mean[0], color = 'red', linewidth = 1.5, label = 'c = 1')

plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean[1], color = 'gray', linewidth = 1.5)
plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean_mean[1], color = 'blue', linewidth = 1.5, label = 'c = 0.1')

plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean[2], color = 'gray', linewidth = 1.5)
plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean_mean[2], color = 'green', linewidth = 1.5, label = 'c = 0.01')

plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean[3], color = 'gray', linewidth = 1.5)
plt.plot(range(0, len(BLOTCHINESS_MEAN_MEAN)), B_mean_mean[3], color = 'yellow', linewidth = 1.5, label = 'c = 0.001')



plt.title("Triplo: Evolution of distance from neighbors over 1000 generations")
    
plt.xlabel("generations")
plt.ylabel('clustering measure, $\mu$')

plt.legend()


plt.savefig('plot_c_all_together.png', dpi=300, bbox_inches='tight')
plt.show()





