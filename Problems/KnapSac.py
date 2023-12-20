# Author : FRESARD Tobias


import numpy as np
import random as rd

class KnapSac :
    # Store usefull information of the problem
    def __init__(self, nb_objects, capacity_max, weight_min = 2, weight_max = 15, value_min = 50, value_max = 350):
        self.nb_objects = nb_objects
        self.capacity_max = capacity_max
        self.id_objects = np.arange(0, nb_objects)
        self.weights = np.random.randint(weight_min, weight_max, size=nb_objects) # Poids des objets générés aléatoirement entre 1kg et 15kg
        self.values = np.random.randint(value_min, value_max, size=nb_objects) # Valeurs des objets générées aléatoirement entre 50€ et 350€

    
    # Generate random valid solution
    def generate_solution(self) :
        return np.random.randint(2, size=self.nb_objects, dtype=int)
    
    def get_nb_qubit(self) :
        return self.nb_objects
    
    # Apply heursitics to solution
    def optimize_solution(self, solution) :
        pass
    
    # return the fix of an invalid solution
    def rectify(self, solution) :
        new_solution = np.copy(solution)
        while not self.is_valid(new_solution):
            indices = np.where(new_solution == 1)[0]
            np.random.shuffle(indices)
            new_solution[indices[0]] = 0
        return new_solution
    
    def is_valid(self, solution) :
        return np.sum(solution * self.weights) <= self.capacity_max
    
    # return the cost of the solution
    def cost(self, solution) :
        deltaWeight = self.capacity_max - np.sum(solution * self.weights)
        if deltaWeight >= 0:
            return np.sum(solution * self.values)
        else :
            return deltaWeight
    
    