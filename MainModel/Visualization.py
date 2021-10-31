# -*- coding: utf-8 -*-

from Landscape import Landscape, generate_connection_mat, generate_initial_pop
import matplotlib.pyplot as plt
import numpy as np
import time

'''
The Visualization class visualizes a given Landscape. Visualization works by 
plotting the frequency of the first allele and therefore can only be used in 
the case of 2 alleles. For more alleles additional functions would have to be
added with a different visualization technique.

- Landscape (obj): the landscape to be visualized.
- grid (array): the grid on which to visualize the landscape, indicates the position of
  the populations in space.

'''

class Visualization:
    
    #%% Initialize
    
    def __init__(self, Landscape=None, grid=None):
        self.Landscape = Landscape
        self.grid = grid
        
        
    #%% Getters and setters
    
    # Setter for the grid
    def set_grid(self, grid):
        self.grid = grid
        
    # Setter for the Landscape
    def set_landscape(self, Landscape):
        self.Landscape = Landscape
    
    
    #%% Static visualization
    
    # Plot the connection matrix
    def visualize_connections(self):
        connections = self.Landscape.get_connections()
        plt.figure("Connections")
        plt.imshow(connections)
        plt.colorbar()
        
    # Plot the current allele frequencies for all populations
    def visualize_current_genePool(self, title='Landscape'):
        landscape = np.array(self.Landscape.get_normalized_genePools()) # get the gene pool
        plt.figure(title)
        plt.imshow(np.reshape(landscape[:,0], self.grid)) # plot frequency of first allele
        plt.colorbar()
        plt.clim(0,1)
        
        
    #%% Dynamic visualization
    
    # Plot allele freqeuncies of one generation for all populations
    def visualize_generation(self, gen, i):
        if i==0:
            self.obj = plt.imshow(np.reshape(gen[:,0], self.grid))
            plt.colorbar()
            plt.clim(0,1)
        else:
            self.obj.set_data(np.reshape(gen[:,0], self.grid))
    
    # Plot the evolution of the populations over generations by updating the plot
    # for every generation
    def visualize_genePool_generations(self, generations=None, every=1, title='Landscape evolution'):
        if generations == None:
            generations = np.array(self.Landscape.get_generational_memory())
            
        generations = np.transpose(generations, [1,0,2])
        # transpose to make the 0th axis correspond to the generations rather than the populations.
        
        plt.ion()
        fig = plt.figure(title)
        
        for i,gen in enumerate(generations[np.arange(0,len(generations),every)]):
            self.visualize_generation(gen, i)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.01)
            #if i==0:
            #    time.sleep(30)
        
        # https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/


#%% Testing

if __name__=='__main__':
    
    '''Create a landscape, set up visualization, plot the connection matrix, 
       the inital gene pool, the evolution over 200 generations and the final 
       gene pool.'''
    
    c = 10
    size = 20
    connection_mat = generate_connection_mat(c,size)
    
    l = Landscape(connection_mat, N_copies=1, N_alleles=2)
    #l.set_initial_populations([[1,0], [1,1], [1,1], [0,1]])
    #l.set_initial_populations([[0,1]]+[[1,0] for i in range(size**2-2)]+[[0,1]])
    l.set_initial_populations([[1,1] for i in range(size**2)])
    
    v = Visualization(l, [size,size])
    v.visualize_connections()
    print("Initial gene pools:", l.get_genePools())
    v.visualize_current_genePool()
    for i in range(200):
        l.update_biased()
    v.visualize_genePool_generations(every=1)
    v.visualize_current_genePool('Final landscape')
    