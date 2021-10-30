# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 20:08:07 2021

@author: leand
"""

# This is my first attempt at working with github. We will see how this goes!

# I will initially save the populations as small arrays containing
# The relevant numbers of individuals

import random as rnd
import numpy as np

class Population:
    
    #%% Initialize
    
    def __init__(self, N_copies, N_alleles=2, rel_pop=None):
        # Initializing parameters
        self.N_copies = N_copies
        self.N_alleles = N_alleles
        self.normalized_population = [0 for i in range(N_alleles)]
        self.generational_memory = []
        
        # Creating first generation
        if rel_pop == None:
            # As default set all allele frequencies equal
            rel_pop = [1 for allele in range(N_alleles)]
        
        self.create_population(rel_pop)    
        
    
    #%% getters and setters
    
    def get_N_copies(self):
        return self.N_copies
    
    def get_N_alleles(self):
        return self.N_alleles
    
    def get_population(self):
        if np.sum(self.normalized_population) <1:
            print('returning empty population 1')
        pop=[round(self.N_copies*p) for p in self.normalized_population]
        if np.sum(pop) <1:
            print('returning empty population 2', self.N_copies, [p for p in self.normalized_population])
        return pop
        # round to get rid of floaing point inaccuracies.
    
    def get_normalized_population(self):
        return self.normalized_population
    
    def get_generational_memory(self):
        return self.generational_memory
    
    def set_N_copies(self, N_copies):
        self.N_copies = N_copies
        
    def set_N_alleles(self, N_alleles):
        self.N_alleles = N_alleles
        self.normalized_population = [1/N_alleles for i in range(N_alleles)]
        self.generational_memory = []
        # TODO: make sure population is initialized correctly
    
    
    #%% a couple of helper methods
    
    # Calculate the frequency of the alleles in the population.
    # Changes the instance variable rel_pop.
    def normalize_population(self, population):
        return [p/sum(population) for p in population]
        
    # helper function because I don't always want to have to call np
    def cumsum(self, A):
        return list(np.cumsum(A))
    
    # Given a cummulative relative population, draw one random individual from it
    # Return the result as the index of relative allele in the population.
    def draw_random_individual_from_relative_population_cum(self, rel_pop_cum):
        random_number = rnd.random()
        for i, rpc in enumerate(rel_pop_cum):
            if random_number < rpc:
                return i
        
    
    #%% Create a new population
    
    # Create a population based on a given relative population.
    # To ensure that we obtain exactly N_copies individuals:
    # Top off the rounding errors with draw_random_individual...
    def create_population(self, rel_pop):
        # Check if we changed number of alleles. Print a warning
        if not self.N_alleles == len(rel_pop):
            print("WARNING: HARD CHANGE IN N_ALLELES")
            self.N_alleles = len(rel_pop)
        
        # Normalize rel_pop
        rel_pop = self.normalize_population(rel_pop)
        rel_pop_cum = self.cumsum(rel_pop)
        
        # Generate initial guess of new population
        population = [int(self.N_copies * r) for r in rel_pop]
        
        # Fill up until N_copies by randomly pulling from relative population
        while sum(population) < self.N_copies:
            population[self.draw_random_individual_from_relative_population_cum(rel_pop_cum)] += 1
            
        self.normalized_population = self.normalize_population(population)
      
        self.generational_memory = []
        self.generational_memory.append(self.normalized_population)
        

    #%% Create the next generation
    
    # fetch fixed number of offspring
    def fetch_offspring(self, N_offspring, rel_pop):

        idxs = np.random.choice(len(rel_pop), size=N_offspring, p=rel_pop)
        offspring = [int(np.sum(idxs == i)) for i in range(self.N_alleles)]

        return offspring
    
    # spread to neighbors but relative to number of copies
    def fetch_offspring_relative(self, p_N_copies, rel_pop):
        return self.fetch_offspring(round(p_N_copies * self.N_copies), rel_pop)
    
    # Create a new generation based on a virtual parent generation. New generation will always
    # have N_copies copies
    def next_generation(self, prev_pop=None):
        if prev_pop == None:
            # by default use current population
            rel_pop = self.normalized_population
        else:
            # if a previous population is given, empty the current generational memory 
            # and start from the given population
            self.generational_memory = []
            rel_pop = self.normalize_population(prev_pop)
            
        population = self.fetch_offspring(self.N_copies, rel_pop)
        
        self.normalized_population = self.normalize_population(population)
        self.generational_memory.append(self.normalized_population)
        
        
    #%% Communication with other populations
    
    # Allows for the addition of individuals to the population
    def add_genes(self, added_pop):
        population = self.get_population()
        population = [population[i] + added_pop[i] for i in range(self.N_alleles)]
        self.normalized_population = self.normalize_population(population)
        if np.sum(self.normalized_population)<1:
            print("adding:", population, added_pop, self.normalized_population)
        
    
#%% Testing

if __name__ == '__main__':
    print("hi!")
    
    P = Population(100,2,[1,3])
    #P.create_population([10, 10, 10])
    print("Population at start of simulation:", P.get_normalized_population())
    for i in range(100):
        P.next_generation()
    print("Evolution of generations:\n", P.get_generational_memory())
    
            
        

