# -*- coding: utf-8 -*-

from Landscape import Landscape
from Visualization import Visualization
import numpy as np

#%% Create connection matrix

# Matrix that connects 
c = 0.05
size = 5
a = np.zeros((size**2, size**2)) # Create matrix with only 0
diag1 = np.array([[c for i in range(size-1)]+[0] for j in range(size)]).flatten()[:-1]
diag2 = [c for i in range((size-1)*size)]
connection_mat = np.diag(diag1, 1) + np.diag(diag1, -1) + np.diag(diag2, size) + np.diag(diag2, -size)


#%% Set up Visualization and Landscape

v = Visualization()
l = Landscape(connection_mat, 10, 2)
#l.set_initial_populations([[1,0], [1,1], [1,1], [0,1]])
l.set_initial_populations([[1,0]]+[[1,0] for i in range(size**2-2) ]+[[0,1]])


#%% Visualize

v.visualize_connections(l, [2,2])
print("Initial gene pools:", l.get_genePools())
v.visualize_current_genePool(l, [size,size])
for i in range(100):
    l.update()
v.visualize_genePool_generations(l, [size,size])
#v.visualize_current_genePool(l, [size,size], 'Final landscape')