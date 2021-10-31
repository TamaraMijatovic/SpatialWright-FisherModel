# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 00:06:04 2021

@author: leand
"""

import numpy as np

class BlotchinessMeasurer:
    
    
    #%% OUTDATED
    # Input: A lattice that contains the information for each color (numpy)
    # Output: Array containing the distance from neighbors for each allele
    def measure(self, lattice):
        
        out_lattice = np.zeros(lattice.shape)
        x,y = lattice.shape[:2]
        
        out_lattice[1:, :, :] += lattice[:-1, :, :]
        out_lattice[:-1, :, :] += lattice[1:, :, :]
        out_lattice[:, 1:, :] += lattice[:, :-1, :]
        out_lattice[:, :-1, :] += lattice[:, 1:, :]
        
        out_lattice = out_lattice * lattice
        
        mean_out_lattice = np.mean(out_lattice[1:-1, 1:-1], (0, 1))
        mean_lattice = np.mean(lattice[1:-1, 1:-1], (0, 1))
        
        for i,m in enumerate(mean_lattice):
            if m == 0:
                mean_lattice[i] = 1
            
        
        return mean_out_lattice / mean_lattice / 4
    
    
    
    #%% SQRT OF WHAT IS ACTUALLY HAPPENING
    # INPUT: 2D array containing relative allele frequencies of populations (1D)
    # OUTPUT: One number describing the average distance from neighbors
    def measure_distance_neighbors(self, lattice):
        out_lattice = np.zeros(lattice.shape[:2])
        
        out_lattice[1:, :] += np.sqrt(np.mean((lattice[1:, :, :] - lattice[:-1, :, :])**2, (2)))
        out_lattice[:-1, :] += np.sqrt(np.mean((lattice[:-1, :, :] - lattice[1:, :, :])**2, (2)))
        out_lattice[:, 1:] += np.sqrt(np.mean((lattice[:, 1:, :] - lattice[:, :-1, :])**2, (2)))
        out_lattice[:, :-1] += np.sqrt(np.mean((lattice[:, :-1, :] - lattice[:, 1:, :])**2, (2)))
        
        out_lattice = out_lattice / 4
        mean_out_lattice = np.mean(out_lattice[1:-1, 1:-1], (0, 1))

        
        return mean_out_lattice

    #%% ACTUAL METRIC
    # INPUT: 2D array containing relative allele frequencies of populations (1D)
    # OUTPUT: One number describing the average squared distance from neighbors
    def measure_squared_distance_neighbors(self, lattice):
        out_lattice = np.zeros(lattice.shape[:2])
        
        out_lattice[1:, :] += (np.mean((lattice[1:, :, :] - lattice[:-1, :, :])**2, (2)))
        out_lattice[:-1, :] += (np.mean((lattice[:-1, :, :] - lattice[1:, :, :])**2, (2)))
        out_lattice[:, 1:] += (np.mean((lattice[:, 1:, :] - lattice[:, :-1, :])**2, (2)))
        out_lattice[:, :-1] += (np.mean((lattice[:, :-1, :] - lattice[:, 1:, :])**2, (2)))
        
        out_lattice = out_lattice / 4

        mean_out_lattice = np.mean(out_lattice[1:-1, 1:-1], (0, 1))

        
        return mean_out_lattice


    # RETURNS THE AVERAGE ALLELE FREQUENCIES
    def measurePop(self, lattice):
        mean_lattice = np.mean(lattice[1:-1, 1:-1], (0, 1))    
        return mean_lattice
    
    
    
    
if __name__ == '__main__':
    
    A = np.array([[(int(2 * np.random.rand()), int(2 * np.random.rand())) for j in range(100)] for i in range(100)])
    
    # A = np.array([[( np.random.rand(),  np.random.rand()) for j in range(100)] for i in range(100)])
    # A = np.array([[( 1,  0) for j in range(100)] for i in range(100)])
    
    BM = BlotchinessMeasurer()
    blotch = BM.measure(A)