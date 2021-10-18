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

class Population:
    
    def __init__(self, init_rel_pop):
        self.rel_pop = init_rel_pop
        self.normalize_rel_pop()
        print(self.rel_pop)
        self.generational_memory = []
        self.generational_memory.append(self.rel_pop)
      
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
    
    for p in populations:
        for pp in p:
            print(pp.get_generation())
    
    total_offspring = np.zeros((size, size, 2))
    total_offspring[:, :-1] += offspring[:, 1:]
    total_offspring[:, 1:] += offspring[:, :-1]
    total_offspring[:-1, :] += offspring[1:, :]
    total_offspring[1:, :] += offspring[:-1, :]
    
    for i, p in enumerate(populations):
        for j, pp in enumerate(p):
            pp.add_to_rel_pop(total_offspring[i,j])
            pp.normalize_rel_pop()
            pp.gen_until_only_one_remains()
    
    

size = 10

pop_coeffs = [[[0.5, 0.5] for j in range(size)] for i in range(size)]
spread_coeffs = [[[0.1, 0.1] for j in range(size)] for i in range(size)]

populations = [[Population(pop_coeffs[i][j]) for j in range(size)] for i in range(size)]

for i, p in enumerate(populations):
        for j, pp in enumerate(p):
            pp.gen_until_only_one_remains()

next_generation(size, populations, spread_coeffs)


N_steps = 100
rel_pop = np.zeros((size, size, 2))

for i in range(N_steps):
    print('start')
    next_generation(size, populations, spread_coeffs)
    rel_pop = np.array([[populations[i][j].get_generation() for j in range(size)] for i in range(size)])
    # plt.imshow(rel_pop)