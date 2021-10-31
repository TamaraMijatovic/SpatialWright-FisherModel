# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

'''
The Analysis class loads the data, calculates the blotchiness measure and stores 
the results in a datafile. It also visualizes the results of the monte carlo
simulations as well as the results of the blotchiness measure.

- file (str): name of the file containing the blotchiness resutls.
- Blotchiness_results (dict): blotchiness results obtained from file.
- bias (dict): dictionary indicating the bias belonging to each dataset.
    
This program can be used to compare the blotchiness results for different conditions.

'''

class BlotchinessComparison:
    
    #%% Initialize
    
    def __init__(self, biases, file_name = 'Blotchiness_results.txt'):
        self.file = f"Data\{file_name}"
        self.Blotchiness_results = self.read_blotchiness_results()
        self.bias = biases
        
        
    #%% Obtain data
        
    # obtain data from file
    def read_blotchiness_results(self):
        results = {}
        
        f = open(self.file, "r")
        lines = f.readlines()
        for line in lines:
            line = line.rstrip() #remove trailing \n
            line = line.split(' ') # split on spaces
            dataset = line[0]
            key = bias[dataset]
            c = float(line[1])
            data = np.array([line[i].split(',')[:-1] for i in range(2,len(line))]).astype(float)

            if key in results:
                if c in results[key]:
                    results[key][c].append(data)
                else:
                    results[key][c] = [data]
            else:
                results[key] = {c : [data]}

        return results
    
    # Transform the dictionary so that the other quantity is on the first axis
    def transform_blotchiness_results(self):
        transformed_results = {}
        
        for key in self.Blotchiness_results:
            for c in self.Blotchiness_results[key]:
                
                if c in transformed_results:
                    transformed_results[c][key] = self.Blotchiness_results[key][c]
                else:
                    transformed_results[c] = {key : self.Blotchiness_results[key][c]}
        
        return transformed_results
           
    
    #%% Comparison plots
    
    # Make plots that allow for comparison of the blotchiness measure for different conditions
    def compare(self, results, labels=['bias','c'], mode=1):
        linestyles = ['-', '--', ':', '-.']
        markers = ['', '*', 'o']

        if mode == 1:
            # plot conditions in seperate figures
            plt.figure(f"{labels[0]}", figsize=(15,4))
            for k, key in enumerate(results):
                plt.subplot(1,len(list(results.keys())),k+1)
                plt.grid()
                plt.title(f"{labels[0]} = {key}")
                for i, c in enumerate(results[key]):
                    min_blotch = np.min(results[key][c], 0)
                    max_blotch = np.max(results[key][c], 0)
                    mean_blotch = np.mean(results[key][c], 0)
                    for j in range(len(mean_blotch)):
                        generations = len(mean_blotch[j])
                        plt.fill_between(np.arange(generations), min_blotch[j], max_blotch[j], color=cm.tab20(2*(i%10)+1))
                        plt.plot(mean_blotch[j], c=cm.tab20(2*(i%10)), linestyle=linestyles[j%len(linestyles)], Label=f'{labels[1]}={c}, allele {j}')
                plt.xlabel('generation')
                plt.ylabel('clustering measure, $\mu$')
                plt.legend()
                plt.xlim([0,generations])
                plt.ylim([0,1])
        else:
            # plot all conditions in the same figure
            plt.figure(f"{labels[0]}",figsize=(8,6))
            #plt.grid()
            for k, key in enumerate(results):
                for i, c in enumerate(results[key]):
                    min_blotch = np.min(results[key][c], 0)
                    max_blotch = np.max(results[key][c], 0)
                    mean_blotch = np.mean(results[key][c], 0)
                    for j in range(len(mean_blotch)):
                        generations = len(mean_blotch[j])
                        plt.fill_between(np.arange(generations), min_blotch[j], max_blotch[j], color=cm.tab20(2*(k%10)+1))
                        plt.plot(mean_blotch[j], c=cm.tab20(2*(k%10)), linestyle=linestyles[i%len(linestyles)], marker=markers[j%len(markers)], Label=f'{labels[0]} = {key}, {labels[1]}={c}, allele {j}')
                plt.xlabel('generation')
                plt.ylabel('clustering measure, $\mu$')
                plt.legend()
                plt.xlim([0,generations])
                plt.ylim([0,1])
    
    # Make comparison for differnt values of c
    def compare_connection(self, mode=1):
        self.compare(self.Blotchiness_results, labels=['bias','c'], mode=mode)
        
    # Make comparison for different biases
    def compare_bias(self, mode=1):
        results = self.transform_blotchiness_results()
        self.compare(results, labels=['c','bias'], mode=mode)
            
        
#%% Main
        
if __name__=='__main__':    
    
    bias = {'Data/Dataset0_biased_1_1.txt': (1,1), \
            'Data/Dataset0_biased_1_1.25.txt': (1,1.25), \
            'Data/Dataset0_biased_1_1.5.txt': (1,1.5), \
            'Data/Dataset1_biased_1_1.txt': (1,1), \
            'Data/Dataset1_biased_1_1.25.txt': (1,1.25), \
            'Data/Dataset1_biased_1_1.5.txt': (1,1.5), \
            'Data/Dataset2_biased_1_1.txt': (1,1), \
            'Data/Dataset2_biased_1_1.25.txt': (1,1.25), \
            'Data/Dataset2_biased_1_1.5.txt': (1,1.5)}
        
    compare = BlotchinessComparison(bias, 'Blotchiness_results_measure4.txt')
    compare.compare_connection(2)
    compare.compare_bias(2)