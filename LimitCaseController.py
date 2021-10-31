# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:02:18 2021

@author: leand
"""

import LimitCase as lC
import LimitCaseFileIO as lCFIO

import time


# EXECUTES ONE RUN
def do_run(file_controller, size, N_steps, pop_coeffs, spread_coeffs, sim, n):
    output = sim.simulate()
    file_controller.start_section(output[0].shape, [('run_number', n), ('size', size), ('N_steps', N_steps)])
    for o in output:     
        file_controller.append(o)
    file_controller.end_section()


#%% I DO NOT RECOMMEND RUNNING THIS PROGRAMME. VERY RESOURCE INTENSIVE

def main():
    

    # Set custom filename. WARNING: FILE CAN BE VERY LARGE
    filename = 'run.txt'
    
    
    #%% LOADOUT 0: SERIOUS RUNS
    # # List of coefficients to simulate
    # coefficients_c = [1, 0.1, 0.01, 0.001]
    
    # # Parameters for each coefficient
    # SIZE = [50, 50, 50, 50]
    # N_STEPS = [1000, 1000, 1000, 1000]
    
    # # Number of runs per coefficient
    # N_runs_per_coefficient = 50
    
    #%% LOADOUT 1: TESTING PURPOSES
    coefficients_c = [1, 0.1, 0.01, 0.001]
    SIZE = [20, 20, 20, 20]
    N_STEPS = [100, 100, 100, 100]
    N_runs_per_coefficient = 2
    
    print("REMEMBER TO ADJUST THE DOMAINS FOR EACH C IN THE ANALYSIS SCRIPTS")
    
    #%% Execution
    
    file_controller = lCFIO.FileIO()
    file_controller.create_fresh_file(filename)
    
    
    
    for i, c in enumerate(coefficients_c):
        
        size = SIZE[i]
        N_steps = N_STEPS[i]
        
        pop_coeffs = [[[0.5, 0.5] for j in range(size)] for i in range(size)]
        spread_coeffs = [[[c, c] for j in range(size)] for i in range(size)]
        
        sim = lC.Simulator(size, N_steps, pop_coeffs, spread_coeffs)
        
        for j, n in enumerate(range(N_runs_per_coefficient)):
            t_init = time.time()
            print('c:', c, 'n:', n)
    
            do_run(file_controller, size, N_steps, pop_coeffs, spread_coeffs, sim, n)
            
            t_final = time.time()
            print('duration:', t_final - t_init, 'seconds')
            if i == 0 and j == 0:
                print("ESTIMATED DURATION:", round(((t_final - t_init) / 60 / 60) * len(coefficients_c) * N_runs_per_coefficient, 3), 'hours')
            
  
            
  
if __name__ == '__main__':
    main()

#%% JUST COPY BLOCKS OF CODE IF YOU WANT TO START DIFFERENT RUNS


# coefficients_c = [0.1, 0.01]

# N_runs_per_coefficient = 100

# file_controller = lCFIO.FileIO()
# file_controller.create_fresh_file('run4_long_time.txt')




# for i, c in enumerate(coefficients_c):
    
#     size = 20
#     N_steps = 5000
    
#     pop_coeffs = [[[0.5, 0.5] for j in range(size)] for i in range(size)]
#     spread_coeffs = [[[c, c] for j in range(size)] for i in range(size)]
    
#     sim = lC.Simulator(size, N_steps, pop_coeffs, spread_coeffs)
    
#     for j, n in enumerate(range(N_runs_per_coefficient)):
        
#         t_init = time.time()
        
#         print('c:', c, 'n:', n)

#         output = sim.simulate()

#         file_controller.start_section(output[0].shape, [('run_number', n), ('size', size), ('N_steps', N_steps)])
        
#         for o in output:     
#             file_controller.append(o)
        
#         file_controller.end_section()
        
#         t_final = time.time()
#         print('duration:', t_final - t_init, 'seconds')
        
#         if i == 0 and j == 0:
#             print("ESTIMATED DURATION:", round(((t_final - t_init) / 60 / 60) * len(coefficients_c) * N_runs_per_coefficient, 3), 'hours')
            
            

