# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 13:05:17 2021

@author: leand
"""

from LimitCaseFileIO import FileIO
import time
import measureBlotchiness as mB
import matplotlib.pyplot as plt
import numpy as np

# STARTING THE PROCESS OF READING OUT A DATA FILE
t0 = time.time()

fileIO = FileIO()
fileIO.set_filename("run1.txt")
fileIO.read_all_and_remember_in_brain()

t1 = time.time()
print(t1-t0)

#%% Measure and plot single Monte Carlo Simulation

# Marking the positions of runs in the file. In steps of 50 because this example had 50 repetitions per value of c
batches = [(0, 50), (50, 100), (100, 150), (150, 200)]
c = [1, 0.1, 0.01, 0.001]

col_mean = ['red', 'blue', 'green', 'yellow']



for batch_nr, (start_batch_0, stop_batch_0) in enumerate(batches):

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
    
    plt.plot(range(0, len(blotchiness_mean)), blotchiness_transpose, color='gray', linewidth = 0.1)
    plt.plot(range(0, len(blotchiness_mean)), \
             blotchiness_mean, \
             color = col_mean[batch_nr], \
             label="c="+str(c[batch_nr]))
    
    
    plt.title("Evolution of distance from neighbors over 1000 generations")
    
    plt.xlabel("generations")
    plt.ylabel('clustering measure, $\mu$')
    
    plt.legend()
    plt.savefig('plot_c'+str(c[batch_nr])+'.png', dpi=300, bbox_inches='tight')
    plt.show()
    
#%% Measure and plot Triplo
# Marking the positions of runs in the file. In steps of 50 because this example had 50 repetitions per value of c
batches = [(0, 50), (50, 100), (100, 150), (150, 200)]
c = [1, 0.1, 0.01, 0.001]

col_mean = ['red', 'blue', 'green', 'yellow']



for batch_nr, (start_batch_0, stop_batch_0) in enumerate(batches):

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
    
    # plt.plot(range(0, len(blotchiness_mean)), blotchiness_transpose, color='gray', linewidth = 0.1)
    plt.plot(range(0, len(blotchiness_mean)), \
             blotchiness_mean, \
             color = col_mean[batch_nr], \
             label="c="+str(c[batch_nr]))
    
        
    plt.title("Evolution of distance from neighbors over 1000 generations, multiple c")
    
    plt.xlabel("generations")
    plt.ylabel('clustering measure, $\mu$')
    plt.legend()
plt.savefig('plot_together.png', dpi=300, bbox_inches='tight')
plt.show()
