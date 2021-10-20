# -*- coding: utf-8 -*-

from Landscape import Landscape
from Visualization import Visualization
from MonteCarlo import MonteCarlo, generate_connection_mat, generate_initial_pop
from Database import Database
import time

def single_run():
    #%% Create connection matrix
    
    # Matrix that connects 
    c = 0.001
    size = 20
    connection_mat = generate_connection_mat(c, size)
    
    
    #%% Set up Visualization and Landscape
    
    v = Visualization()
    l = Landscape(connection_mat, 100, 2)
    l.set_initial_populations(generate_initial_pop(size))
    
    
    #%% Visualize
    
    # visualize connection matrix
    v.visualize_connections(l, [2,2])
    # visualize initial gene pools
    print("Initial gene pools:", l.get_genePools())
    v.visualize_current_genePool(l, [size,size], every=100)
    
    
    tt = time.time()
    for i in range(1000):
        l.update()
    print(time.time()-tt)
    
    # visualize results
    v.visualize_genePool_generations(l, [size,size], every=10)
    #v.visualize_current_genePool(l, [size,size], 'Final landscape')
    
def simulate():
    database = Database('test.txt')
    results = MonteCarlo(c_vals=[0.001, 0.0001], size=5, generations=1000, runs=10)
    database.store(results)
    

if __name__=='__main__':
    #single_run()
    simulate()
    
    
'''py-spy top -- python '''