# Author : FRESARD Tobias


import numpy as np
import time

class SimulatedAnnealing :
    def __init__(self, temperature = 500, factor = 0.99) :
        self.T = temperature
        self.factor = factor
    
    
    def solve(self,problem, iterations = 100, batch_size = 10, timeout = None) :
        start_time = time.time()
        T = self.T
        costs= np.zeros(iterations)
        
        
        best_solution = current_solution = problem.generate_solution()
        costs[0] = best_cost = current_cost = problem.cost(current_solution)
        
        for i in range(iterations):
            
            if(timeout is not None and time.time()-start_time>timeout) :
                print("Timeout exceeeded")
                break
            
            T=T*self.factor
            
            # Local search (explore neighbor solutions)
            for j in range(batch_size):
                new_solution = problem.get_neighbor(current_solution)
                new_cost = problem.cost(new_solution)
                
                if new_cost < current_cost:
                    current_cost = new_cost
                    current_solution = np.copy(new_solution)
                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_solution = np.copy(new_solution)
                        
                else:
                    x=np.random.uniform()
                    if x<np.exp((current_cost-new_cost)/T):
                        current_cost=new_cost
                        current_solution= np.copy(new_solution)
                        
                costs[i] = current_cost
             
        return  best_solution, best_cost, costs