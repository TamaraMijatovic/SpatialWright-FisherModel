# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 10:46:25 2021

@author: leand
"""

import numpy as np
import random as rnd
import matplotlib.pyplot as plt

from measureBlotchiness import BlotchinessMeasurer


#%% POPULATION CLASS
# Class controlling limit case simulations
class Population:
    
    # Need an initial relative allele frequency to start
    def __init__(self, init_rel_pop):
        self.rel_pop = init_rel_pop
        self.normalize_rel_pop()
        self.generational_memory = []
        
    # Makes sure that allele frequencies sum to 1
    def normalize_rel_pop(self):
        self.rel_pop = np.array([r/sum(self.rel_pop) for r in self.rel_pop])
    
    # Eliminates all but one allele based on their initial frequency
    # This happens according to Wright-Fisher
    def gen_until_only_one_remains(self):
        
        self.normalize_rel_pop()
        
        rel_pop_cum = np.cumsum(self.rel_pop)
        random_number = rnd.random()
        
        for i, r in enumerate(rel_pop_cum):
            if random_number < r:
                self.rel_pop = 0 * self.rel_pop
                self.rel_pop[i] = 1
                break
                
        self.generational_memory.append(self.rel_pop)
    
    # For receiving fresh genes from neighbors
    def add_to_rel_pop(self, change_in_rel_pop):
        self.rel_pop = self.rel_pop + change_in_rel_pop
        
    # For passing on fresh genes to neighbors
    def get_offspring(self, offspring_weights):
        return offspring_weights * self.rel_pop
    
    # Returns all states taken on by the population over its lifespan
    def get_generational_memory(self):
        return self.generational_memory
    
    # Returns the current relative allele frequencies of the population
    def get_generation(self):
        return self.rel_pop
    

#%% CONTROL FUNCTIONS
# Controls the addition of 
def next_generation(size, populations, spread_coeffs):
    offspring = np.array([[populations[i][j].get_offspring(spread_coeffs[i][j]) for j in range(size)] for i in range(size)])
    
    total_offspring = np.zeros((size, size, offspring.shape[-1]))
    total_offspring[:, :-1] += offspring[:, 1:]
    total_offspring[:, 1:] += offspring[:, :-1]
    total_offspring[:-1, :] += offspring[1:, :]
    total_offspring[1:, :] += offspring[:-1, :]
    
    for i, p in enumerate(populations):
        for j, pp in enumerate(p):
            pp.add_to_rel_pop(total_offspring[i,j])
            pp.normalize_rel_pop()
            pp.gen_until_only_one_remains()
    

#%% SIMULATOR CLASS, used by other scripts to automize simulations    
class Simulator:
    
    def __init__(self, size, N_steps, pop_coeffs, spread_coeffs):
        
        self.size = size
        self.N_steps = N_steps
        
        self.pop_coeffs = pop_coeffs
        self.spread_coeffs = spread_coeffs
        
    
    def simulate(self):
        populations = [[Population(self.pop_coeffs[i][j]) for j in range(self.size)] for i in range(self.size)]
        
        for i, p in enumerate(populations):
            for j, pp in enumerate(p):
                pp.gen_until_only_one_remains()
                
        for i in range(self.N_steps):
            next_generation(self.size, populations, self.spread_coeffs)
            
            
        gen_memory = np.array([[pp.get_generational_memory() for pp in p] for p in populations])
        gen_memory = gen_memory.transpose((2, 0, 1, 3))
        return gen_memory
        
        
    
#%% Used to plot results and save them to files
def plot_and_save(rel_pop_slice, filename, title):
    plt.imshow(rel_pop_slice)
    plt.axis('off')
    plt.title(title)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    
    

#%% Brain behind the main() method
def run_generations(N_generations, size, pop_coeffs, spread_coeffs):
    
    # generating fresh populations based on the population coefficients
    populations = [[Population(pop_coeffs[i][j]) for j in range(size)] for i in range(size)]
    
    
    # Making sure that every population has only one allele remaining    
    next_generation(size, populations, spread_coeffs)
    
    # Creating a tool for measuring blotchiness
    BM = BlotchinessMeasurer()
    
    
    # Creating arrays for blotchiness and mean
    blotchiness = []
    mean = []
    
    # Basis for calculating moving average
    rel_pop_prev = np.array([[populations[i][j].get_generation() for j in range(size)] for i in range(size)])
    
    N_steps = N_generations
    
    for i in range(N_steps):
        print("step", i, "/", N_steps)
        next_generation(size, populations, spread_coeffs)
        rel_pop = np.array([[populations[i][j].get_generation() for j in range(size)] for i in range(size)])
        
        rel_pop_average = 0.5 * (rel_pop + rel_pop_prev)
        rel_pop_prev = rel_pop.copy()
        
        
        blotchiness.append(BM.measure_squared_distance_neighbors(rel_pop))
        mean.append(BM.measurePop(rel_pop))
        
        # Plotting and saving every 100 generations
        if(i%100 == 0):
            filename = 'plot_examplepop_'+ str(i)+ '.png'
            title = "t="+str(i)
            plot_and_save(rel_pop[:,:,0], filename, title)
            
            filename = 'plot_examplepop_average_'+ str(i)+ '.png'
            title = "t="+str(i)
            plot_and_save(rel_pop_average[:,:,0], filename, title)
            

    filename = 'checkerboard_oneframe_' + str(spread_coeffs[0][0][0]) + '.png'
    title = 'c=' + str(spread_coeffs[0][0][0])
    plot_and_save(rel_pop[:,:,0], filename, title)
    
    
    filename = 'checkerboard_oneframe_average_' + str(spread_coeffs[0][0][0]) + '.png'
    title = 'c=' + str(spread_coeffs[0][0][0])
    plot_and_save(rel_pop_average[:,:,0], filename, title)
    
    
    plt.title('blotchiness and mean')
    plt.plot(range(0, N_steps), blotchiness, label='blotchiness')
    plt.plot(range(0, N_steps), mean, label = 'mean')
    plt.legend()
    plt.show()

    
#%% Get's called upon running this script
def main():
    N_generations = 1000
    
    size = 50
    
    
    #%% PRELOAD 0
    
    # pop_coeffs describes the probability for each Population to start with the relevant alleles
    # spread_coeffs describes the probability for each Population to pass on the relevant alleles to its neighbors
    
    
    pop_coeffs = [[[0.5, 0.5] for j in range(size)] for i in range(size)]
    spread_coeffs = [[[100, 100] for j in range(size)] for i in range(size)]
    
    #%% PRELOAD 1
    
    # Add your own custom initial conditions
    
    #%% Execute Simulation
    
    spread_coeffs = [[[100, 100] for j in range(size)] for i in range(size)]
    
    run_generations(N_generations+1, size, pop_coeffs, spread_coeffs)


if __name__ == '__main__':
    main()
    