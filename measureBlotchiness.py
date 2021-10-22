# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 00:06:04 2021

@author: leand
"""

import numpy as np

class BlotchinessMeasurer:
    
    # Input: A lattice that contains the information for each color (numpy)
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
    
    
    
    def measure_distance_neighbors(self, lattice):
        out_lattice = np.zeros(lattice.shape[:2])
        
        # neighbor_l = (lattice[1:, :, :] - lattice[:-1, :, :])**2
        # neighbor_l = np.sqrt(np.sum(neighbor_l), (2))
        
        # neighbor_r = (lattice[:-1, :, :] - lattice[1:, :, :])**2
        # neighbor_r = np.sqrt(np.sum(neighbor_r), (2))
        
        # neighbor_u = (lattice[:, 1:, :] - lattice[:, :-1, :])**2
        # neighbor_u = np.sqrt(np.sum(neighbor_u), (2))
        
        # neighbor_d = (lattice[:, :-1, :] - lattice[:, 1:, :])**2
        # neighbor_d = np.sqrt(np.sum(neighbor_d), (2))
        
        out_lattice[1:, :] += np.sqrt(np.sum((lattice[1:, :, :] - lattice[:-1, :, :])**2, (2)))
        out_lattice[:-1, :] += np.sqrt(np.sum((lattice[:-1, :, :] - lattice[1:, :, :])**2, (2)))
        out_lattice[:, 1:] += np.sqrt(np.sum((lattice[:, 1:, :] - lattice[:, :-1, :])**2, (2)))
        out_lattice[:, :-1] += np.sqrt(np.sum((lattice[:, :-1, :] - lattice[:, 1:, :])**2, (2)))
        
        out_lattice = out_lattice / 4
        
        # out_lattice = (neighbor_l + neighbor_r + neighbor_u + neighbor_d) / 4
        
        mean_out_lattice = np.mean(out_lattice[1:-1, 1:-1], (0, 1))

        
        return mean_out_lattice


    def measure_squared_distance_neighbors(self, lattice):
        out_lattice = np.zeros(lattice.shape[:2])
        
        # neighbor_l = (lattice[1:, :, :] - lattice[:-1, :, :])**2
        # neighbor_l = np.sqrt(np.sum(neighbor_l), (2))
        
        # neighbor_r = (lattice[:-1, :, :] - lattice[1:, :, :])**2
        # neighbor_r = np.sqrt(np.sum(neighbor_r), (2))
        
        # neighbor_u = (lattice[:, 1:, :] - lattice[:, :-1, :])**2
        # neighbor_u = np.sqrt(np.sum(neighbor_u), (2))
        
        # neighbor_d = (lattice[:, :-1, :] - lattice[:, 1:, :])**2
        # neighbor_d = np.sqrt(np.sum(neighbor_d), (2))
        
        out_lattice[1:, :] += (np.sum((lattice[1:, :, :] - lattice[:-1, :, :])**2, (2)))
        out_lattice[:-1, :] += (np.sum((lattice[:-1, :, :] - lattice[1:, :, :])**2, (2)))
        out_lattice[:, 1:] += (np.sum((lattice[:, 1:, :] - lattice[:, :-1, :])**2, (2)))
        out_lattice[:, :-1] += (np.sum((lattice[:, :-1, :] - lattice[:, 1:, :])**2, (2)))
        
        out_lattice = out_lattice / 4
        
        # out_lattice = (neighbor_l + neighbor_r + neighbor_u + neighbor_d) / 4
        
        mean_out_lattice = np.mean(out_lattice[1:-1, 1:-1], (0, 1))

        
        return mean_out_lattice

    
    def measurePop(self, lattice):

        mean_lattice = np.mean(lattice[1:-1, 1:-1], (0, 1))

        
        return mean_lattice
    
    
    
    
if __name__ == '__main__':
    
    A = np.array([[(int(2 * np.random.rand()), int(2 * np.random.rand())) for j in range(100)] for i in range(100)])
    
    # A = np.array([[( np.random.rand(),  np.random.rand()) for j in range(100)] for i in range(100)])
    # A = np.array([[( 1,  0) for j in range(100)] for i in range(100)])
    
    BM = BlotchinessMeasurer()
    blotch = BM.measure(A)