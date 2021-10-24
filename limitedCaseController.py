# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:02:18 2021

@author: leand
"""

import limitingCase as lC
import limitedCaseFileIO as lCFIO

import time

coefficients_c = [1, 0.1, 0.01, 0.001]

N_runs_per_coefficient = 50

file_controller = lCFIO.FileIO()
file_controller.create_fresh_file('run2.txt')




for i, c in enumerate(coefficients_c):
    
    size = 50
    N_steps = 1000
    
    pop_coeffs = [[[0.5, 0.5] for j in range(size)] for i in range(size)]
    spread_coeffs = [[[c, c] for j in range(size)] for i in range(size)]
    
    sim = lC.Simulator(size, N_steps, pop_coeffs, spread_coeffs)
    
    for j, n in enumerate(range(N_runs_per_coefficient)):
        
        t_init = time.time()
        
        print('c:', c, 'n:', n)

        output = sim.simulate()

        file_controller.start_section(output[0].shape, [('run_number', n), ('size', size), ('N_steps', N_steps)])
        
        for o in output:     
            file_controller.append(o)
        
        file_controller.end_section()
        
        t_final = time.time()
        print('duration:', t_final - t_init, 'seconds')
        
        if i == 0 and j == 0:
            print("ESTIMATED DURATION:", round(((t_final - t_init) / 60 / 60) * len(coefficients_c) * N_runs_per_coefficient, 3), 'hours')
            
            


coefficients_c = [1, 0.1, 0.01, 0.001]

N_runs_per_coefficient = 50

file_controller = lCFIO.FileIO()
file_controller.create_fresh_file('run3.txt')




for i, c in enumerate(coefficients_c):
    
    size = 50
    N_steps = 1000
    
    pop_coeffs = [[[0.5, 0.5] for j in range(size)] for i in range(size)]
    spread_coeffs = [[[c, c] for j in range(size)] for i in range(size)]
    
    sim = lC.Simulator(size, N_steps, pop_coeffs, spread_coeffs)
    
    for j, n in enumerate(range(N_runs_per_coefficient)):
        
        t_init = time.time()
        
        print('c:', c, 'n:', n)

        output = sim.simulate()

        file_controller.start_section(output[0].shape, [('run_number', n), ('size', size), ('N_steps', N_steps)])
        
        for o in output:     
            file_controller.append(o)
        
        file_controller.end_section()
        
        t_final = time.time()
        print('duration:', t_final - t_init, 'seconds')
        
        if i == 0 and j == 0:
            print("ESTIMATED DURATION:", round(((t_final - t_init) / 60 / 60) * len(coefficients_c) * N_runs_per_coefficient, 3), 'hours')
            
            

