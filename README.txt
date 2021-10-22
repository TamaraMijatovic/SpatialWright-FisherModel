Monte Carlo simulations of the Wright-Fisher model including spacial infomration.

Class Population: models a single population of N individuals. 
Class Landscape: models a grid of populations and facilitates exchange of genes between the populations. 
Class Visualize: class that allows for visualization of the population grid of a landscape object. 
Class MonteCarlo: parallelized monte carlo simulation of landscapes for different gene exchange conditions. 
Class Database: reading and writing results if the MonteCarlo simulation to a file. 
main.py: main program for running a single Landscape simulation or running a monte Carlo simulation. 
Class BlotchinessMeasurer: Determine blotchiness of a grid of populations obtained from simulations. 
Class Analysis: analysis and visualization of the blotchiness of Monte Carlo simulation results read from file. 
Class CompareBlotchiness: compare and visualize blotchiness results from different Monte Carlo simulations read from file. 
