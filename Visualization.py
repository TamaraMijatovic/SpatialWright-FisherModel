# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 19:31:59 2021

@author: tmija
"""

import Landscape
import matplotlib.pyplot as plt
import numpy as np

class Visualization:
    def __init__(self):
        pass
    
    def visualize(self, Lanscape, grid):
        landscape = np.mean(Landscape.get_genePools(), axis=1)
        
        plt.figure("Landscape")
        plt.imshow(np.reshape(landscape, grid))
        

if __name__=='__main__':
    v = Visualization()
    v.visualize('a', [2,2])
    