# -*- coding: utf-8 -*-

from MonteCarlo import MonteCarlo
import time

class Database:
    def __init__(self, datafile):
        self.f_name = datafile
    
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
    
    
if __name__=='__main__':
    database = Database('Data/test.txt')
    results = MonteCarlo(c_vals=[0.01, 0.0001], size=2, generations=10, runs=2)
    print("Before:", results)
    database.store(results)
    read_results = database.load()
    print("After:", read_results)
    time.sleep(60)