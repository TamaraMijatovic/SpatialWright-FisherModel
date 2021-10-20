# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 10:41:46 2021

@author: tmija
"""

from Population import Population
import numpy as np
from itertools import product

class Landscape:
    def __init__(self, connection_mat, N_copies, N_alleles=2, init_pop=None):
        self.N = len(connection_mat)
        assert(len(connection_mat)==self.N) # Make sure the matrix is square.
        self.populations = [Population(N_copies, N_alleles, init_pop) for n in range(self.N)] # TODO: add arguments
        self.connections = connection_mat
        
        
    #%% getters and setters
    
    def get_connections(self):
        return self.connections
    
    def get_genePools(self):
        return [p.get_population() for p in self.populations] # retrieve gene pool of all populations
    
    def get_normalized_genePools(self):
        return [p.get_normalized_population() for p in self.populations] # retrieve gene pool of all populations
    
    def get_generational_memory(self):
        return [p.get_generational_memory() for p in self.populations]
    
    def set_initial_populations(self, initial_populations):
        assert(len(initial_populations)==self.N)
        for n, pop in enumerate(self.populations):
            pop.create_population(initial_populations[n])
    
    
    #%% exchange and update
    
    def exchange(self):
        alleles = self.get_genePools()
        for i,j in product(range(self.N), range(self.N)):
            p=self.connections[i,j] # exchange from i to j
            if p != 0:
                exchanged = [np.sum(np.random.rand(allele)<p) for allele in alleles[i]] # every allele has a probability of being exchanged
                self.populations[j].add_genes(exchanged) # the number of exchanged alleles is random
                #print(exchanged)
                    
    def next_gen_i(self,i):
        self.populations[i].next_generation()
                
    def next_generation(self):
        for n in range(self.N):
            self.populations[n].next_generation() # calculate the next generation
            
    def update(self):
        self.exchange()
        self.next_generation()


#%% Testing
                    
if __name__=='__main__':
    connection_mat=[[0,0.3],[0.1,0]]
    l = Landscape(connection_mat, 100)
    l.set_initial_populations([[10,1], [3,2]])
    print(l.get_genePools())
    for i in range(100):
        print(i)
        l.update()
    print(l.get_generational_memory())
    
                    
        
        
    