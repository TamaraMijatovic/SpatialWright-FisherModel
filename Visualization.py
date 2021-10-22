# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 19:31:59 2021

@author: tmija
"""

from Landscape import Landscape
import matplotlib.pyplot as plt
import numpy as np
import time

class Visualization:
    def __init__(self, Landscape, grid):
        self.Landscape = Landscape
        self.grid = grid
    
    def visualize_connections(self):
        connections = self.Landscape.get_connections()
        plt.figure("Connections")
        plt.imshow(connections)
        plt.colorbar()
        
    def visualize_current_genePool(self, title='Landscape'):
        landscape = np.array(self.Landscape.get_normalized_genePools()) # get the gene pool
        plt.figure(title)
        plt.imshow(np.reshape(landscape[:,0], self.grid)) # plot frequency of first allele
        plt.colorbar()
        plt.clim(0,1)
        
    def visualize_generation(self, gen, i):
        if i==0:
            self.obj = plt.imshow(np.reshape(gen[:,0], self.grid))
            plt.colorbar()
            plt.clim(0,1)
        else:
            self.obj.set_data(np.reshape(gen[:,0], self.grid))
        
    def visualize_genePool_generations(self, every=1, title='Landscape evolution'):
        generations = np.transpose(np.array(self.Landscape.get_generational_memory()), [1,0,2])
        # transpose to make the 0th axis correspond to the generations rather than the populations.
        
        plt.ion()
        fig = plt.figure(title)
        
        for i,gen in enumerate(generations[np.arange(0,len(generations),every)]):
            self.visualize_generation(gen, i)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.01)
        
        # https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/

if __name__=='__main__':
    
    c = 0.05
    size = 10
    a = np.zeros((size**2, size**2)) # Create matrix with only 0
    diag1 = np.array([[c for i in range(size-1)]+[0] for j in range(size)]).flatten()[:-1]
    diag2 = [c for i in range((size-1)*size)]
    connection_mat = np.diag(diag1, 1) + np.diag(diag1, -1) + np.diag(diag2, size) + np.diag(diag2, -size)
    
    l = Landscape(connection_mat, 10, 2)
     #l.set_initial_populations([[1,0], [1,1], [1,1], [0,1]])
    l.set_initial_populations([[1,0]]+[[1,0] for i in range(size**2-2) ]+[[0,1]])
    
    v = Visualization(l, [size,size])
    v.visualize_connections()
    print("Initial gene pools:", l.get_genePools())
    v.visualize_current_genePool()
    for i in range(200):
        l.update_biased([1,2])
    v.visualize_genePool_generations(every=1)
    #v.visualize_current_genePool(l, [size,size], 'Final landscape')
    