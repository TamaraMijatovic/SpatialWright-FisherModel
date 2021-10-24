# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:04:57 2021

@author: leand
"""

import os
import numpy as np

class FileIO:
    
    def create_fresh_file(self, filename):
        self.set_filename(filename)
        with open(self.filename, 'w') as f:
            f.write('')
        
    
    def set_filename(self, filename):
        current_dir = os.getcwd()
        self.filename = current_dir + "/" + filename
    
    
    def start_section(self, shape, parameters):
        with open(self.filename, 'a') as f:
            f.write(str(shape))
            
            for p in parameters:
                name, value = p
                f.write(';' + str((name, value)))
            f.write('\n')
    
    
    def end_section(self):
        with open(self.filename, 'a') as f:
            f.write('@\n')
    
    def append(self, array):
        with open(self.filename, 'a') as f:
            array_flattened_stringed = [str(b) for b in array.flatten()]
            f.write(' '.join(array_flattened_stringed)+ '\n')

        



    def read_all_and_remember_in_brain(self):
        
        print("reading...")
        
        container = [[]]
        
        with open(self.filename) as f:
            lines = f.readlines()
            
            for l in lines:
                if not l == '@\n':
                    container[-1].append(l)
                else:
                    container.append([])
                    
            del(container[-1])
        
        
        print("done")
        
        output = []
        
        sh = len(container)
        
        print("unpacking container...")
        for i, c  in enumerate(container):
            
            print("reading set", i, '/', sh)
            
            shape_and_params = c[0].split(';')
            
            shape_text = shape_and_params[0]
            params_text = shape_and_params[1:]
            
            shape_text = shape_text.replace('(','')
            shape_text = shape_text.replace(')','')
            
            shape_text = shape_text.split(', ')
            
            shape = [int(s) for s in shape_text]
            
            data_text = c[1:]
            data_flat = np.array([[float(l_split) for l_split in l.split(' ')] for l in data_text])
            
            data = data_flat.reshape(tuple([data_flat.shape[0]]) + tuple(shape))
            
            output.append([tuple(shape), params_text, data])
        
        print("done")
        
        print("saving to brain...")
        
        self.brain = output
        
        print("done")


    def get_whole_brain(self):
        print("fetching brain...")
        return self.brain
        print("done")
        

    def get_segment_brain(self, i, j):
        return self.brain[i:j]

    def get_slice_brain(self, i):
        return self.brain[i]

    def read_all(self):
        
        print("reading...")
        
        container = [[]]
        
        with open(self.filename) as f:
            lines = f.readlines()
            
            for l in lines:
                if not l == '@\n':
                    container[-1].append(l)
                else:
                    container.append([])
                    
            del(container[-1])
        
        
        print("done")
        
        output = []
        
        sh = len(container)
        
        print("unpacking container...")
        for i, c  in enumerate(container):
            
            print("reading set", i, '/', sh)
            
            shape_and_params = c[0].split(';')
            
            shape_text = shape_and_params[0]
            params_text = shape_and_params[1:]
            
            shape_text = shape_text.replace('(','')
            shape_text = shape_text.replace(')','')
            
            shape_text = shape_text.split(', ')
            
            shape = [int(s) for s in shape_text]
            
            data_text = c[1:]
            data_flat = np.array([[float(l_split) for l_split in l.split(' ')] for l in data_text])
            
            data = data_flat.reshape(tuple([data_flat.shape[0]]) + tuple(shape))
            
            output.append([tuple(shape), params_text, data])
        
        print("done")
        
        return output
        
    
            
    
    
    
if __name__ == '__main__':
    
    
    A = np.arange(24)
    B = A.reshape((4,3,2))
    
    
    C = np.arange(100, 124)
    D = C.reshape((4,3,2))
    
    fileIO = FileIO()
    fileIO.create_fresh_file('test.txt')
    fileIO.start_section(B.shape, (['c', 0.1],['t_max', 1000]))
    fileIO.append(B)
    fileIO.append(B + 1)
    fileIO.end_section()
    
    fileIO.start_section(D.shape, (['c', 0.01],['t_max', 100]))
    fileIO.append(C)
    fileIO.append(C-1)
    fileIO.end_section()
    
    output = fileIO.read_all()
    