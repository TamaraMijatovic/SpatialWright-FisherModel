# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:04:57 2021

@author: leand
"""

import os

class fileIO:
    
    def create_fresh_file(self, filename):
        self.set_filename(filename)
        with open(filename, 'w') as f:
            f.write("")
        
    
    def set_filename(self, filename):
        current_dir = os.getcwd()
        self.filename = current_dir + "/" + filename
        
    def append_3D(self, array):
        return
    
    def append_2D(self, array):
        return
        
    def read_3D(self):
        return
        
    def read_2D(self):
        return