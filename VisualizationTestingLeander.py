# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 19:31:59 2021

@author: tmija
"""

from Landscape import Landscape
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import time

class Visualization:
    def __init__(self):
        pass
    
    def visualize_connections(self, Landscape, grid):
        connections = Landscape.get_connections()
        plt.figure("Connections")
        plt.imshow(connections)
        plt.colorbar()
        
    def visualize_generation(self, gen, grid):
        plt.imshow(np.reshape(gen[:,0], grid))
        
    def visualize_current_genePool(self, Landscape, grid, title='Landscape'):
        landscape = np.array(Landscape.get_normalized_genePools()) # get the first allele frequency from the gene pool      
        plt.figure(title)
        self.visualize_generation(landscape, grid)
        cb = plt.colorbar()
        plt.clim(0,1)
        
    def visualize_genePool_generations(self, Landscape, grid, title='Landscape evolution'):
        generations = np.transpose(np.array(Landscape.get_generational_memory()), [1,0,2])[::100]
        # transpose to make the 0th axis correspond to the generations rather than the populations.
        
        print(generations.shape)
        
        plt.ion()
        fig = plt.figure(title)
        
        for gen in generations:
            self.visualize_generation(gen, grid)
            cb = plt.colorbar()
            plt.clim(0,1)
            
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.01)
            
            cb.remove()
            
        cb = plt.colorbar()
        plt.clim(0,1)
        
        # https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/

if __name__=='__main__':
    
    c = 0.005
    size = 10
    a = np.zeros((size**2, size**2)) # Create matrix with only 0
    diag1 = np.array([[c for i in range(size-1)]+[0] for j in range(size)]).flatten()[:-1]
    diag2 = [c for i in range((size-1)*size)]
    connection_mat = np.diag(diag1, 1) + np.diag(diag1, -1) + np.diag(diag2, size) + np.diag(diag2, -size)
    
    v = Visualization()
    l = Landscape(connection_mat, 100, 2)
    v.visualize_connections(l, [2,2])
    
    #l.set_initial_populations([[1,0], [1,1], [1,1], [0,1]])
    # l.set_initial_populations([[0,1]]+[[1,0] for i in range(size**2-2) ]+[[0,1]])
    
    # pop_init = [[1,0] for i in range(int(0.5 * size**2))] + [[0,1] for i in range(int(0.5 * size**2), size**2)]
    pop_init = [[0.5, 0.5] for i in range(size**2)]
    
    print(int(0.5 * size**2))
    print(len(pop_init))
    
    l.set_initial_populations(pop_init)
    
    print("Initial gene pools:", l.get_genePools())
    v.visualize_current_genePool(l, [size,size])
    
    i_max = 10000
    
    
    tt = time.time()
    for i in range(i_max):
        # tt = time.time()
        l.update()
        print(i, '/', i_max)
        
    print(time.time() - tt)
    v.visualize_genePool_generations(l, [size,size])
    #v.visualize_current_genePool(l, [size,size], 'Final landscape')
    