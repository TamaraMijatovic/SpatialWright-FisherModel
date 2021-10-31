# -*- coding: utf-8 -*-

import random as rnd
import numpy as np

'''
The population class is used to model a single population with N_copies gene copies
each of which can carry one of N_alleles alleles. The population is modelled in
a stochastic way based on the Wright-Fisher model.

- N_copies (int): number of gene copies in the population.
- N_alleles (int): number of alleles in the population.
- normalized_population (array): list of normalized allele frequencies in the population.
- generational_memory (array): list in which all generations are stored for later reference.

'''

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
        
    
    #%% Getters and setters
    
    # Getter for the number of gene copies in te population
    def get_N_copies(self):
        return self.N_copies
    
    # Getter for the number of alleles in the population
    def get_N_alleles(self):
        return self.N_alleles
    
    # Getter for the absolute population.
    # Note that N_copies is not adapted during exchange, therefore the resuls 
    # of this function are only correct after the new generation of N_copies 
    # gene copies has been generated.
    def get_population(self):
        return [round(self.N_copies*p) for p in self.normalized_population]
        # round to get rid of floaing point inaccuracies.
    
    # Getter for the normalized population.
    def get_normalized_population(self):
        return self.normalized_population
    
    # Getter for the generational memory
    def get_generational_memory(self):
        return self.generational_memory
    
    # Setter for the number of gene copeis in the population
    def set_N_copies(self, N_copies):
        self.N_copies = N_copies
        
    # Setter for the number of alleles in the population
    def set_N_alleles(self, N_alleles):
        self.N_alleles = N_alleles
        # reinitialize normalized population, equal freqencies for all alleles)
        self.normalized_population = [1/N_alleles for i in range(N_alleles)]
        # reset generational memory
        self.generational_memory = []
    
    
    #%% Helper methods
    
    # Calculate the normalized frequency of the alleles in the population.
    def normalize_population(self, population):
        return [p/sum(population) for p in population]
    
    # Given a cummulative relative population, draw one random individual from it
    # Return the result as the index of relative allele in the population.
    def draw_random_individual_from_relative_population_cum(self, rel_pop_cum):
        random_number = rnd.random()
        for i, rpc in enumerate(rel_pop_cum):
            if random_number < rpc:
                return i
    # NOTE: this code could be improved by using a similar method as in fetch offspring
    # By making some small changes in the create_population function it would probably 
    # be possible to use the fetch offspring function to generate the remaining necessary
    # gene opies at once, rather than a loop calling this function. That way it would 
    # aslo not be necessary to calculate the cummulative population.
    # I left the code as is, because that is how we ran it. That way the results are 
    # reproducible.
        
    
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
        rel_pop_cum = list(np.cumsum(rel_pop))
        
        # Generate initial guess of new population
        population = [int(self.N_copies * r) for r in rel_pop]
        
        # Fill up until N_copies by randomly pulling from relative population
        while sum(population) < self.N_copies:
            population[self.draw_random_individual_from_relative_population_cum(rel_pop_cum)] += 1
            
        # Normalize the population
        self.normalized_population = self.normalize_population(population)
      
        # Reset the generational memory and store the initial population
        self.generational_memory = []
        self.generational_memory.append(self.normalized_population)
        

    #%% Create the next generation
    
    # Fetch a fixed number of offspring
    def fetch_offspring(self, N_offspring, rel_pop):
        # randomly choose N_offspring gene copies for the current population.
        idxs = np.random.choice(len(rel_pop), size=N_offspring, p=rel_pop)
        offspring = [int(np.sum(idxs == i)) for i in range(self.N_alleles)]
        return offspring
    
    # Create a new generation based on a virtual parent generation. 
    # New generation will always have N_copies copies
    def next_generation(self, prev_pop=None):
        if prev_pop == None:
            # by default use current population
            rel_pop = self.normalized_population
        else:
            # if a previous population is given, empty the current generational memory 
            # and start from the given population
            self.generational_memory = []
            rel_pop = self.normalize_population(prev_pop)
            
        # Obtain the new generation
        population = self.fetch_offspring(self.N_copies, rel_pop)
        
        # Normalize and store the population
        self.normalized_population = self.normalize_population(population)
        self.generational_memory.append(self.normalized_population)
        
        
    #%% Communication with other populations
    
    # Allows for the addition of individuals to the population
    # Note that N_copies is not changes, therefore N_copies can only be assumed
    # to be correct after calculating the new generation.
    def add_genes(self, added_pop):
        population = self.get_population()
        population = [population[i] + added_pop[i] for i in range(self.N_alleles)]
        self.normalized_population = self.normalize_population(population)
        
    
#%% Testing

if __name__ == '__main__':
    
    '''Create a population and simulate 100 generations.'''
    
    P = Population(100,2,[1,3])
    print("Population at start of simulation:", P.get_normalized_population())
    for i in range(100):
        P.next_generation()
    print("Evolution of generations:\n", P.get_generational_memory())
    
            
        

