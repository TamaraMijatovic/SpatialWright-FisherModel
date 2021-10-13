# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 10:41:46 2021

@author: tmija
"""

import Population
import numpy as np
from itertools import product

class Landscape:
    def __init__(self, connection_mat):
        self.N = len(connection_mat)
        assert(connection_mat)
        self.populations = [Population() for n in self.N]
        self.connections = connection_mat
        
    def get_connections(self):
        return self.connections
    
    def get_genePools(self):
        return [p.get_genePool() for p in self.populations] # retrieve gene pool of all populations
    
    def exchange(self):
        alleles = self.get_genePools(self)
        for i,j in product(range(self.N), range(self.N)):
            
            p=self.connections[i][j] # exchange from i to j
            if p != 0:
                exchanged = [allele for allele in alleles[i] if (np.random.rand()<p)] # every allele has a probability of being exchanged
                self.populations[j].add_genes(exchanged) # the number of exchanged alleles is random
                    
    def next_gen(self):
        for n in range(self.N):
            self.populations[n].next_gen() # calculate the next generation
            
    def update(self):
        self.exchange(self)
        self.next_gen(self)

                    
if __name__=='__main__':
    connection_mat=[[1,1][1,1]]
    Landscape(connection_mat)
    Landscape.update()
    
                    
        
        
    