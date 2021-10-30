# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 20:04:11 2021

@author: tmija
"""
from multiprocessing import Pool
import numpy as np
import time

def func(i):
    np.random.seed()
    print(np.random.rand())

if __name__=='__main__':
    # np.random.seed(0)
    # with Pool(12) as p:
    #     results = p.map(func, [i for i in range(12)])
    # time.sleep(10)
    
    np.random.seed(0)
    random_seeds = np.random.randint(2**16-1, size = (9,3,50)) #total amount of runs
    
    # store random seeds for later reference
    f = open('seeds.txt', "w")
    for seed in random_seeds.flatten():
        f.write(f'{seed},')
    f.close()