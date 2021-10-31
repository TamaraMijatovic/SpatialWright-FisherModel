# -*- coding: utf-8 -*-

from Landscape import Landscape, generate_connection_mat, generate_initial_pop
import numpy as np
from multiprocessing import Pool
import time

'''
Functions for MonteCarlo simulation where individual runs are done in parallel.

'''

#%% Prallel part

# Function to be executed in parallel
def MonteCarloRun(args):
    # Unpack arguments and set seed
    c, size, connection_mat, gene_copies, alleles, generations, bias, run, seed = args
    np.random.seed(seed)
    
    print(f'c: {c}, run: {run}')
    # Generate Landscape
    l = Landscape(connection_mat, gene_copies, alleles)
    l.set_initial_populations(generate_initial_pop(size, mode=1))
    # Simulate Landscape
    for i in range(generations):
        l.update_biased(bias)

    return l.get_generational_memory()


#%% Simulation

# Execute monte carlo simulation
def MonteCarlo(c_vals, size, gene_copies=100, alleles=2, generations=1000, runs=100, bias=None, seeds=None):
    # If no seed are give, create random seeds
    if seeds is None:
        seeds = np.random.randint(2**16-1, size=(len(c_vals), runs))
    
    # For every value of c execute the required number of runs in parallel
    results_dict = {}
    for i, c in enumerate(c_vals):
        # Generate connection matrix
        connection_mat = generate_connection_mat(c, size)
        
        # prepare arguments for passing on to the parallelized function
        args = [[c, size, connection_mat, gene_copies, alleles, generations, bias, run, seeds[i, run]] for run in range(runs)]
        with Pool(10) as p:
            results = p.map(MonteCarloRun, args)
    
        # store results with corresponding value of c
        results_dict[c] = results
        
    return results_dict
 
    
#%% Testing

if __name__=='__main__':
    
    '''Time monte carlo run and print results.'''
    
    tt = time.time()
    results = MonteCarlo(c_vals=[0.001, 0.0001], size=5, generations=10, runs=2, bias=[1,2], alleles=2)
    print('Execution time:', time.time()-tt)
    print(results)
    time.sleep(60) # to keep terminal open, so that results can be inspected
    