# Author : FRESARD Tobias


import numpy as np
import random as rd

class Problem :
    # Store usefull information of the problem
    def __init__(self):
        pass
    
    # Generate random solution
    def generate_solution(self) :
        pass 
    
    # Apply heursitics to solution
    def optimize_solution(self, solution) :
        pass
    
    # return the fix of an invalid solution
    def rectify(self, solution):
        pass
    
    # return the cost of the solution
    def cost(self, solution) :
        pass
    
    # return a neighbor solution
    def get_neighbor(self, solution) :
        pass
    
    # Return all the crossings
    def crossover(self, population, nb_crossover, crossover_rate) :
        pass
    
    # Return all the mutants
    def mutation(self, population, mutation_rate) :
        pass
        
    def get_distances(self) :
        pass