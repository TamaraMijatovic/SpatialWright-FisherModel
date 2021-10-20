# -*- coding: utf-8 -*-

from Landscape import Landscape
from Visualization import Visualization
import numpy as np
import time

def generate_connection_mat(c, size):
    diag1 = np.array([[c for i in range(size-1)]+[0] for j in range(size)]).flatten()[:-1]
    diag2 = [c for i in range((size-1)*size)]
    connection_mat = np.diag(diag1, 1) + np.diag(diag1, -1) + np.diag(diag2, size) + np.diag(diag2, -size)
    
    #print(connection_mat)
    return connection_mat

if __name__=='__main__':
    #%% Create connection matrix
    
    # Matrix that connects 
    c = 0.001
    size = 20
    connection_mat = generate_connection_mat(c, size)
    
    
    #%% Set up Visualization and Landscape
    
    v = Visualization()
    l = Landscape(connection_mat, 100, 2)
    #l.set_initial_populations([[1,0], [1,1], [1,1], [0,1]])
    l.set_initial_populations([[1,0]]+[[1,1] for i in range(size**2-2) ]+[[0,1]])
    
    
    #%% Visualize
    
    v.visualize_connections(l, [2,2])
    print("Initial gene pools:", l.get_genePools())
    v.visualize_current_genePool(l, [size,size])
    tt = time.time()
    for i in range(1000):
        l.update()
    print(time.time()-tt)
    
    #v.visualize_genePool_generations(l, [size,size])
    #v.visualize_current_genePool(l, [size,size], 'Final landscape')
    
    
'''py-spy top -- python '''