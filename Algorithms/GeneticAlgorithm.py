# Author : FRESARD Tobias


import TSP
import numpy as np
import time 

class GeneticAlgorithm :
    def __init__(self, crossover_rate = 0.6, mutation_rate = 0.6) :
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
            
            costs[i] = self.population_cost(problem, population)
            parents = self.selection(problem, population, nb_parents)
            children = problem.crossover(parents, nb_children, self.crossover_rate)
            mutants = problem.mutation(children, self.mutation_rate)
            population[:parents.shape[0], :] = parents
            population[parents.shape[0]:, :] = mutants

        best_solution = self.selection(problem, population, 1)[0]
        best_cost = problem.cost(best_solution)
        return best_solution, best_cost, costs
    
    
    def selection(self, problem, population, nb_selection) :
        
        fitness_scores = [problem.cost(solution) for solution in population]
        
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k])
        
        selected_solutions = np.array([population[idx] for idx in sorted_indices[:nb_selection]])

        return selected_solutions
    
    def population_cost(self, problem, population) :
        return np.mean([problem.cost(solution) for solution in population])