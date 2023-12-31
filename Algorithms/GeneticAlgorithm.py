# Author : FRESARD Tobias


import numpy as np
import time 
import random as rd

class GeneticAlgorithm :
    def __init__(self, crossover_rate = 1, mutation_rate = 1) :
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
          
    
    def solve(self,problem, iterations = 100, batch_size = 10, timeout = None):
        start_time = time.time()
        costs = np.zeros(iterations)
        population = np.array([problem.generate_solution() for _ in range(batch_size)])
        nb_parents = population.shape[0]//2
        nb_children = population.shape[0] - nb_parents 
        for i in range(iterations):
            
            if(timeout is not None and time.time()-start_time>timeout) :
                print("Timeout exceeeded")
                break
            
            costs[i] = problem.cost(self.selection(problem, population, 1)[0])
            parents = self.selection(problem, population, nb_parents)
            children = self.crossover(problem, parents, nb_children)
            mutants = self.mutation(problem, children)
            population[:parents.shape[0], :] = parents
            population[parents.shape[0]:, :] = mutants

        best_solution = self.selection(problem, population, 1)[0]
        best_cost = problem.cost(best_solution)
        return best_solution, best_cost, costs
    
    
    def selection(self, problem, population, nb_selection) :
        
        fitness_scores = [problem.cost(solution) for solution in population]
        
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k],reverse=True)
        
        selected_solutions = np.array([population[idx] for idx in sorted_indices[:nb_selection]])

        return selected_solutions
    
    def population_cost(self, problem, population) :
        return np.mean([problem.cost(solution) for solution in population])
    
    def crossover(self, problem, population, nb_crossover) :
        crossings = []
        i = 0

        while (i < nb_crossover): 
            x = rd.random()
            parent1_index = i%population.shape[0]
            if x > self.crossover_rate:
                crossings.append(np.copy(population[parent1_index]))
            else :
                parent2_index = (i+1)%population.shape[0]
                crossings.append(problem.crossover(population[parent1_index],population[parent2_index]))
            i += 1
            
        return np.array(crossings)
    
    def mutation(self, problem, population) :
        mutants = np.copy(population)
        for i in range(population.shape[0]):
            x = rd.random()
            if x > self.mutation_rate:
                mutants[i] = np.copy(mutants[i])
            else :
                mutants[i] = problem.mutation(mutants[i])
        return mutants