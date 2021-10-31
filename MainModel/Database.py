# -*- coding: utf-8 -*-

from MonteCarlo import MonteCarlo
import time

'''
The Database class contains functions to store the results of Monte Carlo simulation
in a datafile and reading these results from the datafile. This class requires the
data and the files to be in a specific format.

- f_name (str): name of the file where date should be stored/obtained from.

'''

class Database:
    
    #%% Initialize
    
    def __init__(self, datafile):
        self.f_name = datafile
    
    
    #%% Write
    
    def write(self, f, data):
        for key in data:
            f.write(f'{key}\n')
            for exp in data[key]:
                for pop in exp:
                    for gen in pop:
                        for allele in gen:
                            f.write(f'{allele},')
                        f.write(';')
                    f.write(' ')
                f.write('\n')
            f.write('\n\n')   
    
    def store(self, data):
        f = open(self.f_name, "w")
        self.write(f, data)
        f.close()
    
    def append(self, data):
        f = open(self.f_name, "a")
        self.write(f, data)
        f.close()
    
    
    #%% Read
    
    def load(self):
        f = open(self.f_name, "r")
        lines = f.readlines()
        
        next_block = True
        dictionary = {}
        for line in lines:
            if line == '\n':
                next_block = True
            else:
                #remove \n from the end of the line.
                line = line.rstrip()
                if next_block:
                    key = float(line) 
                    dictionary[key] = []
                    i = 0
                    next_block = False
                else:
                    #if i==0: print(line)
                    dictionary[key].append([])
                    #split on spaces
                    pops = line.split(' ')
                    #if i==0: print(pops)
                    for j,pop in enumerate(pops):
                        dictionary[key][i].append([])
                        #split on ;
                        gens = pop.split(';')
                        gens = gens[:-1] #remove empty element at the end
                        #if i==0: print(gens)
                        for gen in gens:
                            #split on ,
                            alleles = gen.split(',')
                            alleles = alleles[:-1] #remove empty element at 
                            dictionary[key][i][j].append([float(allele) for allele in alleles])
                            #if i==0: print(gen)
                    i+=1
                    
        f.close()
        return dictionary
    
    
#%% Testing
    
if __name__=='__main__':
    
    '''Create test database, run Monte Carlo simulation, store and read resutls.'''
    
    database = Database('Data/test.txt')
    results = MonteCarlo(c_vals=[0.001, 0.0001], size=5, generations=10, runs=50)
    print("Before:", results)
    database.store(results)
    read_results = database.load()
    print("After:", read_results)
    time.sleep(60)