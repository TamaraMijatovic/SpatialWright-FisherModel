# -*- coding: utf-8 -*-

from Landscape import Landscape
import numpy as np
from multiprocessing import Pool
import time

def generate_connection_mat(c, size):
    diag1 = np.array([[c for i in range(size-1)]+[0] for j in range(size)]).flatten()[:-1]
    diag2 = [c for i in range((size-1)*size)]
    connection_mat = np.diag(diag1, 1) + np.diag(diag1, -1) + np.diag(diag2, size) + np.diag(diag2, -size)
    
    #print(connection_mat)
    return connection_mat

def generate_initial_pop(size, mode=1):
    if size == 1:
        init_pop = [[1,1]]
    else:
        if mode == 1: 
            init_pop = [[1,1] for i in range(size**2)]
        elif mode == 2: 
            init_pop = [[1,0] for i in range(size**2-1)]+[[0,1]]
        elif mode == 3: 
            init_pop = [[1,0]] + [[1,1] for i in range(size**2-1)] + [[0,1]]
        else:
            print("Error: unknown mode.")
            init_pop = [[1,1] for i in range(size**2)]
    
    return init_pop

def MonteCarloRun(args):
    c, size, connection_mat, gene_copies, alleles, generations, bias, run, seed = args
    np.random.seed(seed)
    
    print(f'c: {c}, run: {run}')
    # Generate Landscape
    l = Landscape(connection_mat, gene_copies, alleles)
    l.set_initial_populations(generate_initial_pop(size, mode=1))
    for i in range(generations):
        l.update_biased(bias)

    #print(c, l.get_generational_memory())
    return l.get_generational_memory()

def MonteCarlo(c_vals, size, gene_copies=100, alleles=2, generations=1000, runs=100, bias=None, seeds=None):
    if seeds is None:
        seeds = np.random.randint(2**16-1, size=(len(c_vals), runs))
    
    results_dict = {}
    for i, c in enumerate(c_vals):
        # Generate connection matrix
        connection_mat = generate_connection_mat(c, size)
        
        args = [[c, size, connection_mat, gene_copies, alleles, generations, bias, run, seeds[i, run]] for run in range(runs)]
        with Pool(10) as p:
            results = p.map(MonteCarloRun, args)
    
        results_dict[c] = results
        
    return results_dict
 
    
if __name__=='__main__':
    tt = time.time()
    results = MonteCarlo(c_vals=[0.001, 0.0001], size=5, generations=10, runs=2, bias=[1,2], alleles=10)
    print('Execution time:', time.time()-tt)
    print(results)
    time.sleep(60)
    