# -*- coding: utf-8 -*-

from Landscape import Landscape, generate_connection_mat, generate_initial_pop
from Visualization import Visualization
from MonteCarlo import MonteCarlo
from Database import Database
import numpy as np
import time

'''
Main program that can either be used to simulate a single run of a landscape useing the 
single run function or to simulate triplos of monte carlo simulations for different
connection coefficients and biases using the simulate function.

'''

#%% Single run

def single_run():
    #Create connection matrix
    c = 0.01
    size = 10
    connection_mat = generate_connection_mat(c, size)

    #Set up Visualization and Landscape
    l = Landscape(connection_mat, 100, 2)
    l.set_initial_populations(generate_initial_pop(size, mode=2))
    v = Visualization(l,[size,size])

    #Visualize
    # visualize connection matrix
    v.visualize_connections()
    # visualize initial gene pools
    print("Initial gene pools:", l.get_genePools())
    v.visualize_current_genePool()
    
    tt = time.time()
    for i in range(500):
        l.update_biased()
    print(time.time()-tt)
    
    # visualize results
    v.visualize_genePool_generations(every=1)
    #v.visualize_current_genePool('Final landscape')


#%% Simulate

def simulate():
    # Gemerate random seeds
    np.random.seed(0)
    random_seeds = np.random.randint(2**16-1, size = (9,3,50)) #total amount of runs
    
    # store random seeds for later reference
    f = open('Data/seeds.txt', "w")
    for seed in random_seeds.flatten():
        f.write(f'{seed},')
    f.close()
    
    # Run 3 Monte carlo simulations for different biases and a range of c-values.
    for i, bias in enumerate([[1,1], [1,1.25], [1,1.5]]):
        for sim in range(3):
            print(f'bias: {bias}, simulation {sim}')
            # Store results in files
            database = Database(f'Data/Dataset{sim}_biased_{bias[0]}_{bias[1]}.txt')
            results = MonteCarlo(c_vals=[0.001, 0.0001, 0.00001], size=20, generations=1000, runs=50, bias=bias, seeds=random_seeds[(i*3)+sim])
            database.store(results)
    
#%% Main

if __name__=='__main__':
    single_run()
    #simulate()
    
'''profiler command: py-spy top -- python <program name>'''