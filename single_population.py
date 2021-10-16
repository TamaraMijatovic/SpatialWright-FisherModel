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
    
    # Class Variables
    
    def __init__(self, N_copies, N_alleles=2):
        self.N_copies = N_copies
        self.N_alleles = N_alleles
        self.population = [0 for i in range(N_alleles)]
        self.population[0] = N_copies
        self.update_relative_population()
        
   
    # Calculate the frequency of the alleles in the population.
    # Changes the instance variable rel_pop.
    def calc_relative_population(self, population):
        return [p/sum(population) for p in population]
        
    def update_relative_population(self):
        self.rel_pop = [p/sum(self.population) for p in self.population]
    
    
    # Given a relative population, draw one random individual from it
    # Return the result as the index of relative allele in the
    # population / rel_pop list
    def draw_random_individual_from_relative_population(self, rel_pop):
        random_number = rnd.random()
        rel_pop_cum = list(np.cumsum(rel_pop))
        for i, rpc in enumerate(rel_pop_cum):
            if random_number < rpc:
                return i
        
    def cumsum(self, A):
        return list(np.cumsum(A))
    
    def draw_random_individual_from_relative_population_cum(self, rel_pop_cum):
        random_number = rnd.random()
        for i, rpc in enumerate(rel_pop_cum):
            if random_number < rpc:
                return i
        
    
    # Create a population based on a given relative population.
    # To ensure that we obtain exactly N_copies individuals:
    # Top off the rounding errors with draw_random_individual...
    def create_population_according_to_relative_population(self, rel_pop):
        
        # Normalize rel_pop
        rel_pop = [r/sum(rel_pop) for r in rel_pop]
        print(rel_pop)
        
        # Generate initial guess of new population
        self.population = [int(self.N_copies * r) for r in rel_pop]
        
        # Check if we changed number of alleles. Print a warning
        if not self.N_alleles == len(self.population):
            print("WARNING: HARD CHANGE IN N_ALLELES")
            self.N_alleles = len(self.population)
        
        # Fill up until N_copies by randomly pulling from relative population
        while sum(self.population) < self.N_copies:
            self.population[self.draw_random_individual_from_relative_population(rel_pop)] += 1
        
    
    # Create a new generation based on a virtual parent generation. New generation will always
    # have N_copies copies
    def create_population_randomize_from_prev_generation(self, prev_relative):
        rel_pop = self.calc_relative_population(prev_relative)
        rel_pop_cum = self.cumsum(rel_pop)
        self.population = [0 for p in self.population]
        for i in range(self.N_copies):
            self.population[self.draw_random_individual_from_relative_population_cum(rel_pop_cum)] += 1
    
    
    
            
        

