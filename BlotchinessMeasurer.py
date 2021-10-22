# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 00:06:04 2021

@author: leand
"""

import numpy as np

class BlotchinessMeasurer:
    
    # Input: A lattice that contains the information for each color (numpy)
    def measure(self, lattice):
        
        # make sure lattice is large enough
        assert(len(lattice)>2)
        assert(len(lattice[0])>2)
        
        out_lattice = np.zeros(lattice.shape)
        
        out_lattice[1:, :, :] += lattice[:-1, :, :]
        out_lattice[:-1, :, :] += lattice[1:, :, :]
        out_lattice[:, 1:, :] += lattice[:, :-1, :]
        out_lattice[:, :-1, :] += lattice[:, 1:, :]
        
        out_lattice = out_lattice/4 * lattice
        mean_out_lattice = np.mean(out_lattice[1:-1, 1:-1], (0, 1))
            
        return mean_out_lattice
    
    def measure_divided_by_mean(self, lattice):
        
        mean_out_lattice = self.measure(lattice)
        mean_lattice = np.mean(lattice[1:-1, 1:-1], (0, 1))
        mean_lattice[np.where(mean_lattice==0)]=1 # to prevent division by zero
            
        return mean_out_lattice / mean_lattice
    
    
    def measure_generations(self, data, every=1):
        blotchiness = [[] for run in range(len(data))]
        
        for run, generational_memory in enumerate(data):
            # Change order of axes to have first axes denote the generations
            generations = np.transpose(np.array(generational_memory), [1,0,2])
            
            for i,gen in enumerate(generations[np.arange(0,len(generations),every)]):
                gen_lattice = np.reshape(gen, (int(round(np.sqrt(len(gen)))), int(round(np.sqrt(len(gen)))), 2))
                blotchiness[run].append(self.measure(gen_lattice))
        
        blotchiness = np.array(blotchiness)
        mean_blotchiness = np.mean(blotchiness, 0)
        
        return mean_blotchiness#, mean_blotchiness-np.min(blotchiness,0), np.max(blotchiness,0)-mean_blotchiness
    
    
if __name__ == '__main__':
    
    A = np.array([[(1,0) for j in range(100)] for i in range(100)]) # completely one color
    B = np.array([[(1,0) for j in range(50)]+[(0,1) for j in range(50)] for i in range(100)]) # half one color half the other color
    C = np.array([[(0.5,0.5) for j in range(100)] for i in range(100)]) # completely 50,50
    D = np.array([[(0.2,0.8) for j in range(100)] for i in range(100)]) # completely 20,80
    E = np.array([[(((i%2)*(j%2)+(1-(i%2))*(1-(j%2))), ((1-(i%2))*(j%2)+(i%2)*(1-(j%2)))) for j in range(100)] for i in range(100)]) # checkerboeard pattern
    
    
    # A = np.array([[( np.random.rand(),  np.random.rand()) for j in range(100)] for i in range(100)])
    # A = np.array([[(int(2 * np.random.rand()), int(2 * np.random.rand())) for j in range(100)] for i in range(100)])
    
    BM = BlotchinessMeasurer()
    for i in [A,B,C,D,E]:
        blotch1 = BM.measure(i)
        blotch2 = BM.measure_divided_by_mean(i)
        print(blotch1, blotch2)