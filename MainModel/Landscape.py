# -*- coding: utf-8 -*-

from Population import Population
import numpy as np

'''
The Landscape class combines N population objects in a grid to model a landscape
of populations. This class is used to simulate exchange of genes between populations.

- N (int): number of populations.
- populations (array): list containing the population objects.
- connections (numpy array): matrix containing connection coefficients that give the probability
  of gene transfer from one population to another.

'''

class Landscape:
    
    #%% Initialize
    
    def __init__(self, connection_mat, N_copies, N_alleles=2, init_pop=None):
        self.N = len(connection_mat)
        assert(len(connection_mat)==self.N) # Make sure the matrix is square.
        self.populations = [Population(N_copies, N_alleles, init_pop) for n in range(self.N)]
        self.connections = connection_mat
        
        
    #%% Getters and setters
    
    # Getter for the connection matrix
    def get_connections(self):
        return self.connections
    
    # Getter for the absolute gene pools of all populations
    def get_genePools(self):
        return [p.get_population() for p in self.populations] # retrieve gene pool of all populations
    
    # Getter for the normalized gene pools of all populations
    def get_normalized_genePools(self):
        return [p.get_normalized_population() for p in self.populations] # retrieve gene pool of all populations
    
    # Getter for the generational memory of all populations
    def get_generational_memory(self):
        return [p.get_generational_memory() for p in self.populations]
    
    # Setter for the initial gene pool of all populations
    def set_initial_populations(self, initial_populations):
        assert(len(initial_populations)==self.N)
        for n, pop in enumerate(self.populations):
            pop.create_population(initial_populations[n])
    
    
    #%% Exchange and update
            
    # Exchange genes between populations according to the connection matrix and
    # a given bias.
    def exchange_biased(self, bias=None):
        alleles = self.get_genePools()
        
        # if no bias is given, exchange will be unbiased.
        if bias == None:
            bias = [1 for i in range(len(alleles[0]))]
        
        # for each population collect all genes that are added to that population and then add.
        for j in range(self.N):
            exchanged = np.zeros(len(alleles[j]))
            for i in range(self.N):
                p=self.connections[i][j] # exchange from i to j
                if p != 0:
                    exchanged += [np.sum(np.random.rand(allele)<bias[k]*p) for k,allele in enumerate(alleles[i])] # every allele has a probability of being exchanged
            self.populations[j].add_genes(exchanged) # the number of exchanged alleles is random
            # Note: Add all alleles at the same time, since the add_genes function normalizes the
            # resulting population. If genes would be added one at a time, the genes that would
            # be added later would count more.
                
    # Calculate next generation for all populations
    def next_generation(self):
        for n in range(self.N):
            self.populations[n].next_generation() # calculate the next generation
        
    # Update the population: exchange genes and calculate the next generations
    def update_biased(self, bias=None):
        self.exchange_biased(bias)
        self.next_generation()


#%% Functions for generating connection matrix and initial conditions

# Generate a connection matrix that connects all populations to only their direct 
# neighbours (left, right, above, below) by connection coefficient c.
def generate_connection_mat(c, size):
    diag1 = np.array([[c for i in range(size-1)]+[0] for j in range(size)]).flatten()[:-1]
    diag2 = [c for i in range((size-1)*size)]
    connection_mat = np.diag(diag1, 1) + np.diag(diag1, -1) + np.diag(diag2, size) + np.diag(diag2, -size)

    return connection_mat

# Generate initial population for a system with two alleles
def generate_initial_pop(size, mode=1):
    if size == 1:
        # equal frequencies for both alleles
        init_pop = [[1,1]]
    else:
        if mode == 1: 
            # equal frequencies for both alleles
            init_pop = [[1,1] for i in range(size**2)]
        elif mode == 2: 
            # all allele 1 except the last square
            init_pop = [[1,0] for i in range(size**2-1)]+[[0,1]]
        elif mode == 3: 
            # first square only allele 2, last square only allele 2, 
            # other squares equal frequencies for both alleles
            init_pop = [[1,0]] + [[1,1] for i in range(size**2-1)] + [[0,1]]
        else:
            # if mode is not know, give all populations equal frequenies for both alleles
            print("Error: unknown mode.")
            init_pop = [[1,1] for i in range(size**2)]
    
    return init_pop


#%% Testing
                    
if __name__=='__main__':
    
    '''Create a landscape based on a simple connection matrix, set its initial populations and
       simulate 100 generations.'''
    
    connection_mat=[[0,0.3],[0.1,0]]
    l = Landscape(connection_mat, 100)
    l.set_initial_populations([[10,1], [3,2]])
    print(l.get_genePools())
    for i in range(100):
        print(i)
        #l.update()
        l.update_biased()
    print(l.get_generational_memory())
    
                    
        
        
    