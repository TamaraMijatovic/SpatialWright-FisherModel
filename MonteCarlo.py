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

def generate_initial_pop(size):
    if size == 1:
        init_pop = [[1,1]]
    else:
        init_pop = [[1,0]]+[[1,1] for i in range(size**2-2) ]+[[0,1]]
    
    return init_pop

def MonteCarloRun(args):
    c, size, individuals, alleles, generations, runs = args
    # Generate connection matrix
    connection_mat = generate_connection_mat(c, size)
    
    results = []
    for run in range(runs):      
        # Generate Landscape
        l = Landscape(connection_mat, individuals, alleles)
        l.set_initial_populations(generate_initial_pop(size))
        for i in range(generations):
            l.update()
        # Store data
        results.append(l.get_generational_memory())
        #print(c, l.get_generational_memory())
        
    return results

def MonteCarlo(c_vals, size, individuals=100, alleles=2, generations=1000, runs=100):
    args = [[c, size, individuals, alleles, generations, runs] for c in c_vals]
    
    with Pool(2) as p:
        results = p.map(MonteCarloRun, args)
        
    results_dict = {}
    for i,result in enumerate(results):
        results_dict[c_vals[i]] = result
        
    return results_dict
 
    
if __name__=='__main__':
    tt = time.time()
    results = MonteCarlo(c_vals=[0.001, 0.0001], size=5, generations=1000, runs=10)
    print('Execution time:', time.time()-tt)
    #print(results)
    time.sleep(60)
    