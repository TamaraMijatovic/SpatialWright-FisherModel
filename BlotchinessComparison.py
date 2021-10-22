# -*- coding: utf-8 -*-

class BlotchinessComparison:
    def __init__(self, file_name = 'Blotchiness_results.txt'):
        self.file = f"Data\{file_name}"
        self.Blotchiness_results = self.read_blotchiness_results()
        
    def read_blotchiness_results(self):
        results = {}
        
        f = open(self.file, "r")
        lines = f.readlines()
        for line in lines:
            line = line.rstrip() #remove trailing \n
            line = line.split(' ') # split on spaces
            dataset = line[0]
            c = float(line[1])
            data = [line[i].split(',')[:-1] for i in range(2,len(line))]
            
        
if __name__=='__main__':
    compare = BlotchinessComparison()