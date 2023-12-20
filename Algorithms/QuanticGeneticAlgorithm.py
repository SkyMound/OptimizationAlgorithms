# Author : FRESARD Tobias


import numpy as np
import time 
import random as rd
import math

class QuanticGeneticAlgorithm :
    def __init__(self ) :
        pass
          
    
    def solve(self,problem, iterations = 100, batch_size = 10, timeout = None):
        start_time = time.time()
        costs = np.zeros(iterations)

        Q = np.ones((batch_size,problem.get_nb_qubit(),2))/np.sqrt(2)
        P = np.array([ np.array([0 if rd.random() < qj[0]**2 else 1 for qj in q]) for q in Q])
        
        best_solution   = self.selection(problem, P, 1)[0]
        best_cost       = problem.cost(best_solution)
        
        for i in range(iterations):
            
            
            
            if(timeout is not None and time.time()-start_time>timeout) :
                print("Timeout exceeeded")
                break
            # Apply rotation gate (Kuk-Hyun Han et Jong-Hwan Kim, 2000)
            for q_solution, solution, solution_index in zip(Q,P,range(batch_size)) :
                current_cost = problem.cost(solution)
                for qubit, bit, bbit, qubit_index in zip(q_solution, solution, best_solution, range(problem.get_nb_qubit())) :
                    
                    bit_flag = bit == 1
                    bbit_flag = bbit == 1 
                    cost_flag = current_cost >= best_cost
                    
                    if ((not(bit_flag) and not(bbit_flag))
                    or (not(bit_flag) and bbit_flag and not(cost_flag))) :
                        continue
                    
                    if not(bit_flag) and bbit_flag and cost_flag :
                        gamma = 0.05*math.pi*self.compute_sign(qubit,-1,1,'r',0)
                    
                    if bit_flag and not(bbit_flag) and not(cost_flag) :
                        gamma = 0.01*math.pi*self.compute_sign(qubit,-1,1,'r',0)
                        
                    if bit_flag  and cost_flag :
                        gamma = 0.025*math.pi*self.compute_sign(qubit,1,-1,0,'r')
                        
                    if bit_flag and bbit_flag and not(cost_flag) :
                        gamma = 0.05*math.pi*self.compute_sign(qubit,1,-1,0,'r')
                    
                    U = np.array([[math.cos(gamma),-math.sin(gamma)],
                                  [math.sin(gamma),math.cos(gamma)]])
                    
                    Q[solution_index,qubit_index] = np.dot(U,qubit)
                                   
            P = np.array([ np.array([0 if rd.random() < qj[0]**2 else 1 for qj in q]) for q in Q])
            
            new_solution   = self.selection(problem, P, 1)[0]
            new_cost       = problem.cost(new_solution)
            print(new_cost)
            costs[i] = new_cost
            if(new_cost > best_cost) :
                best_solution = new_solution
                best_cost = new_cost
        print(Q)
        return best_solution, best_cost, costs
    
    
    def selection(self, problem, population, nb_selection) :
        
        fitness_scores = [problem.cost(solution) for solution in population]
        
        sorted_indices = sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k],reverse=True)
        
        selected_solutions = np.array([population[idx] for idx in sorted_indices[:nb_selection]])

        return selected_solutions
    
    def population_cost(self, problem, population) :
        return np.mean([problem.cost(solution) for solution in population])
    
    def compute_sign(self, q, v1, v2, v3, v4) :
        if q[0]*q[1] < 0:
            return v1
        elif q[0]*q[1] > 0:
            return v2
        elif q[0] == 0 :
            return v3 if v3 != 'r' else rd.randint(0,1)
        elif q[1] == 0 :
            return v4 if v4 != 'r' else rd.randint(0,1)