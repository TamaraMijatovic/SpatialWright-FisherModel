# -*- coding: utf-8 -*-

from Database import Database
from BlotchinessMeasurer import BlotchinessMeasurer
from Visualization import Visualization
import numpy as np
import matplotlib.pyplot as plt

'''
The Analysis class loads the data, calculates the blotchiness measure and stores 
the results in a datafile. It also visualizes the results of the monte carlo
simulations as well as the results of the blotchiness measure.

- dataset_name (str): name of the dataset.
- database (obj): database object ofr the dataset.
- results (dict): results obtained form the database.
- BM (obj): BlotchinessMeasurer object for measureing blotchiness of results.
- blotchiness (array): blotchiness results of analysis.

This program can be used to analyze all data, or only one dataset.

'''

class Analysis:
    
    #%% Initialize
    
    def __init__(self, dataset):
        self.dataset_name = dataset
        self.database = Database(self.dataset_name)
        self.results = self.database.load()
        self.BM = BlotchinessMeasurer()
        self.blotchiness = []
        
        
    #%% Analysis
    
    # Calculate blotchiness measure of the results
    def analyze(self, mode):
        self.blotchiness = []
        for c in self.results:
            self.blotchiness.append(self.BM.measure_generations(self.results[c], measure=mode))
           
            
    #%% Storing data in file
           
    # Store results for blotchiness measure in file
    def store_blotchiness(self, file='Blotchiness_results.txt', clear=False):
        if clear:
            # clear file before writing
            f = open(f"Data\{file}", "w")
        else:
            # append to file
            f = open(f"Data\{file}", "a")
        
        for i,c in enumerate(self.results):
            f.write(f'{self.dataset_name} {c} ')
            
            if len(self.blotchiness[i].shape)==1:
                # one measure for all alleles
                for generation in self.blotchiness[i].T:
                    f.write(f'{generation},')
                f.write(' ')
                
            else:
                # different measures for the different alleles
                for allele in self.blotchiness[i].T:
                    for generation in allele:
                        f.write(f'{generation},')
                    f.write(' ')
                    
            f.write('\n')

        f.close()
        
        
    #%% Visualization
        
    # Visualize blotchiness of all simulations
    def visualize_blotchiness(self, title = "Blotchiness_over_generations"):
        linestyles = ['-', ':', '--', '-.']
        plt.figure(title)
        plt.grid()

        for i,c in enumerate(self.results):
            if len(self.blotchiness[i].shape)==1:
                plt.plot(self.blotchiness[i], c=f'C{i}', Label=f'c={c}')
            else:
                for j,allele in enumerate(self.blotchiness[i].T):
                    plt.plot(allele, c=f'C{i}', linestyle=linestyles[j%len(linestyles)], Label=f'c={c}, allele {j}')
       
        plt.xlabel('generation')
        plt.ylabel('blotchiness')
        plt.legend()
        plt.xlim([0,len(self.blotchiness[i])-1])
        plt.ylim([0,1])
        
        plt.savefig(f'Plots/{title}.png')
        plt.close()
        
        
    # Visualize state of the population grid at the end of the population
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
            
    # Visualize
    def visualize_one_run(self, grid, title='Example_run'):
        vis = Visualization(grid=grid)
        for c in self.results:
            vis.visualize_genePool_generations(generations=self.results[c][0], title=f'{title}_c{c}')
   
    
#%% Analyze all data

def analyze_all_data():
    for i, bias in enumerate([[1,1], [1,1.25], [1,1.5]]):
        for sim in range(3):
            dataset = f'Data/Dataset{sim}_biased_{bias[0]}_{bias[1]}.txt'
            
            data = Analysis(dataset)
            print(f"Data loaded! {i*3+sim}")
            
            measure = 4
            data.analyze(measure)
            data.store_blotchiness(f'Blotchiness_results_measure{measure}.txt')
            data.visualize_blotchiness(f"Dataset{sim}_biased_{bias[0]}_{bias[1]}_blotchiness_{measure}")
            print(f"Data analyzed! {i*3+sim}")
    
            # data_test.visualize_last_genePool([5,5], "test_final")
            data.visualize_last_genePool([20,20], f"Dataset{sim}_biased_{bias[0]}_{bias[1]}_final")
        
        
#%% Analyze one dataset
        
def analyze_one_run():
    # data = Analysis('Data/test.txt')
    # print("Data loaded!")
    # data.visualize_one_run([5,5])

    data = Analysis('Data/Dataset0_biased_1_1.txt')
    print("Data loaded!")
    data.visualize_one_run([20,20])


#%% Main

if __name__=='__main__':
    analyze_all_data()
    #analyze_one_run()
    
    
    
    
    
    
    