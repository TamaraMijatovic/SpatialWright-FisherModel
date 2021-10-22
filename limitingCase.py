# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 10:46:25 2021

@author: leand
"""

# Two alleles
# Only deal in absolutes

# Loop:
    # Produce generations until only one allele remains per population
    # Spread from neighbors to other populations


import numpy as np
import random as rnd
import matplotlib.pyplot as plt

from measureBlotchiness import BlotchinessMeasurer

class Population:
    
    def __init__(self, init_rel_pop):
        self.rel_pop = init_rel_pop
        self.normalize_rel_pop()
        # print(self.rel_pop)
        self.generational_memory = []
        # self.generational_memory.append(self.rel_pop)
      
    def normalize_rel_pop(self):
        self.rel_pop = np.array([r/sum(self.rel_pop) for r in self.rel_pop])
    
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
    
    def add_to_rel_pop(self, change_in_rel_pop):
        self.rel_pop = self.rel_pop + change_in_rel_pop
        
    def get_offspring(self, offspring_weights):
        return offspring_weights * self.rel_pop
    
    def get_generational_memory(self):
        return self.generational_memory
    
    def get_generation(self):
        return self.rel_pop
    

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
        
        
    

    
if __name__ == '__main__':
    
    
    size = 50
    
    pop_coeffs = [[[0.5, 0.5] for j in range(size)] for i in range(size)]
    spread_coeffs = [[[0.001, 0.001] for j in range(size)] for i in range(size)]
    
    # pop_coeffs = [[[0.5, 0.5, 0.5] for j in range(size)] for i in range(size)]
    # spread_coeffs = [[[0.001, 0.001, 0.001] for j in range(size)] for i in range(size)]
    
    populations = [[Population(pop_coeffs[i][j]) for j in range(size)] for i in range(size)]
    
    for i, p in enumerate(populations):
            for j, pp in enumerate(p):
                pp.gen_until_only_one_remains()
    
    next_generation(size, populations, spread_coeffs)
    
    N_steps = 1000
    rel_pop = np.zeros((size, size, 2))
    
    BM = BlotchinessMeasurer()
    
    
    blotchiness = []
    mean = []
    
    for i in range(N_steps):
        print("step", i, "/", N_steps)
        next_generation(size, populations, spread_coeffs)
        rel_pop = np.array([[populations[i][j].get_generation() for j in range(size)] for i in range(size)])
        
        blotchiness.append(BM.measure_squared_distance_neighbors(rel_pop))
        mean.append(BM.measurePop(rel_pop))
        
        if(i%100 == 0):
            plt.imshow(rel_pop[:,:,0])
            plt.show()
            
            
            