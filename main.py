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
    
    l = Landscape(connection_mat, 100, 2)
    l.set_initial_populations(generate_initial_pop(size, mode=1))
    v = Visualization(l,[size,size])
    
    
    #%% Visualize
    
    # visualize connection matrix
    v.visualize_connections()
    # visualize initial gene pools
    print("Initial gene pools:", l.get_genePools())
    v.visualize_current_genePool()
    
    tt = time.time()
    for i in range(100):
        l.update_biased([1,2])
    print(time.time()-tt)
    
    # visualize results
    v.visualize_genePool_generations(every=1)
    #v.visualize_current_genePool('Final landscape')
    
def simulate():
    database = Database('Data/Dataset9_biased_1_1.5.txt')
    results = MonteCarlo(c_vals=[0.001, 0.0001, 0.00001], size=20, generations=1000, runs=50, bias=[1,1.5])
    database.store(results)
    

if __name__=='__main__':
    #single_run()
    simulate()
    
    
'''py-spy top -- python '''