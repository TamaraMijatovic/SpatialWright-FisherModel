# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 11:48:15 2021

@author: tmija
"""

from Database import Database
from BlotchinessMeasurer import BlotchinessMeasurer
import numpy as np
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, dataset):
        self.dataset_name = dataset
        self.database = Database(self.dataset_name)
        self.results = self.database.load()
        self.BM = BlotchinessMeasurer()
        self.blotchiness = []
        
    def analyze(self):
        for c in self.results:
            self.blotchiness.append(self.BM.measure_generations(self.results[c]))
        
    def visualize_blotchiness(self, title = "Blotchiness_over_generations"):
        plt.figure(title)
        linestyles = ['-', ':', '--', '-.']
        plt.grid()
        #print(self.blotchiness)
        for i,c in enumerate(self.results):
            for j,allele in enumerate(self.blotchiness[i].T):
                plt.plot(allele, c=f'C{i}', linestyle=linestyles[j%len(linestyles)], Label=f'c={c}, allele {j}')
        plt.xlabel('generation')
        plt.ylabel('blotchiness')
        plt.legend()
        plt.xlim([0,len(self.blotchiness[i])-1])
        plt.ylim([0,1])
        
        plt.savefig(f'Plots/{title}.png')
        plt.close()
        
    def store_blotchiness(self, file='Blotchiness_results.txt', clear=False):
        if clear:
            f = open(f"Data\{file}", "w")
        else:
            f = open(f"Data\{file}", "a")
        
        for i,c in enumerate(self.results):
            f.write(f'{self.dataset_name} {c} ')
            for allele in self.blotchiness[i].T:
                for generation in allele:
                    f.write(f'{generation},')
                f.write(' ')
            f.write('\n')
            
        f.close()
        
    def visualize_last_genePool(self, grid, title='Final_landscape'):
        for i,c in enumerate(self.results):
            
            results_c = np.array(self.results[c])
            size = np.sqrt(len(results_c)+1)
            #print(size)
            
            fig = plt.figure(f"{title}, c={c}", figsize=(12,10))
            axs = []
            for j,exp in enumerate(results_c):
                axs.append(fig.add_subplot(int(np.floor(size)),int(np.ceil(size)),j+1))
                plot = axs[j].imshow(np.reshape(exp[:,-1,0], grid), vmin=0, vmax=1) # plot first allele frequency of the last generation
                #ax[j].clim(0,1)
                axs[j].set_xticks([])
                axs[j].set_yticks([])
            plt.colorbar(plot, ax=axs, location='right', shrink=0.5)
            
            plt.savefig(f'Plots/{title}_c{c}.png')
            #plt.close()    


if __name__=='__main__':
    # data_test = Analysis('Data/test.txt')
    # data_test.analyze()
    # data_test.store_blotchiness()
    # data_test.visualize_blotchiness("test")
    # data_test.visualize_last_genePool([5,5], "test_final")
    
    datasets = ['Data/Dataset1_unbiased.txt', \
                'Data/Dataset2_biased_1_1.25.txt', \
                'Data/Dataset3_biased_1_1.5.txt', \
                'Data/Dataset4_unbiased.txt', \
                'Data/Dataset5_biased_1_1.25.txt', \
                'Data/Dataset6_biased_1_1.5.txt']
        
    for i, dataset in enumerate(datasets):
        data = Analysis(dataset)
        print("Data loaded!")
        
        data.analyze()
        data.store_blotchiness()
        print("Data analyzed!")
        
        data.visualize_blotchiness(f"Dataset{i}_analysis")
        data.visualize_last_genePool([20,20], f"Dataset{i}_final")
    