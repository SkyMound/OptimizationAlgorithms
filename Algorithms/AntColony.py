# Author : FRESARD Tobias


import numpy as np
import random as rd
import time
import matplotlib.pyplot as plt


class AntColony :
    def __init__(self, exploitation_rate = 4, exploration_rate = 4, evaporation_rate = 0.1, initial_pheromone = 0.5, k = 100) :
        self.exploitation_rate = exploitation_rate
        self.exploration_rate = exploration_rate
        self.evaporation_rate = evaporation_rate
        self.initial_pheromone = initial_pheromone
        self.k = k
    
    def solve(self, problem, iterations = 100, batch_size = 10, timeout=None,display_pheromone=False) :
        start_time = time.time()
        
        costs = np.zeros(iterations)
        distances = problem.get_distances()
        nb_locations = distances.shape[0]
        pheromone_matrice = np.full((nb_locations,nb_locations),self.initial_pheromone)
        
        
        best_solution = None
        best_cost = 10**6
        for i in range(iterations):
            
            ant_solutions = np.zeros((batch_size,nb_locations),dtype=int)
            for ant_index in range(batch_size) :
                if(timeout is not None and time.time()-start_time>timeout) :
                    break
                current_location = ant_index%nb_locations
                visited_locations = [current_location]
                for _ in range(nb_locations-1) :
                    not_visited_locations =np.setdiff1d([ k for k in range(nb_locations)],visited_locations)
                    
                    numerators = np.zeros(len(not_visited_locations))
                    denominator = 0
                    for decision_index, potential_location in enumerate(not_visited_locations) :
                        visibility = (1/distances[current_location][potential_location])**self.exploitation_rate
                        trace = (pheromone_matrice[current_location][potential_location])**self.exploration_rate
                        numerators[decision_index] = visibility*trace
                        denominator += numerators[decision_index]
                    
                    probabilities = np.divide(numerators, denominator)
                   
                    # Make a decision
                    new_location = rd.choices(not_visited_locations,probabilities)[0]
                    visited_locations.append(new_location)  
                              
                ant_solutions[ant_index] = np.array(visited_locations)
            
            if(timeout is not None and time.time()-start_time>timeout) :
                print("Timeout exceeeded")
                break
            
            # Evaporation
            for source in range(nb_locations) :
                for target in range(nb_locations) :
                    pheromone_matrice[source,target] *= (1-self.evaporation_rate)

            # Renforcement
            for ant_index in range(batch_size) :
                current_cost = problem.cost(ant_solutions[ant_index])
                for location_index in range(nb_locations) :
                    source = ant_solutions[ant_index,location_index]
                    target = ant_solutions[ant_index,(location_index+1)%nb_locations]
                    pheromone_matrice[source, target] += self.k/current_cost
                    pheromone_matrice[target, source] += self.k/current_cost
                    
                if current_cost<best_cost :
                    best_cost = current_cost
                    best_solution = ant_solutions[ant_index]
           
            costs[i] = best_cost
        
        # Get best solution according to pheromones
        best_path = [0]
        current_city = 0 

        while len(best_path) < nb_locations :
            next_city = max(
                range(nb_locations),
                key=lambda city: pheromone_matrice[current_city][city] if city not in best_path and city != current_city else -1
            )
            best_path.append(next_city)
            current_city = next_city

        if problem.cost(best_path) < best_cost :
            best_cost = problem.cost(best_path)
            best_solution = np.array(best_path)
        
        if display_pheromone :
            # Plotting the connections between locations
            for i in range(nb_locations):
                for j in range(i + 1, nb_locations):
                    x_values = [problem.city_coords[i][0], problem.city_coords[j][0]]
                    y_values = [problem.city_coords[i][1], problem.city_coords[j][1]]
                    
                    # Set line width based on the pheromone value
                    line_width = pheromone_matrice[i][j]**2*2   # Adjust multiplier as needed
                    
                    plt.plot(x_values, y_values, linewidth=line_width, color='blue')

            # Plotting the locations
            x_coords = [coord[0] for coord in problem.city_coords]
            y_coords = [coord[1] for coord in problem.city_coords]
            plt.scatter(x_coords, y_coords, color='red')
        
        return best_solution, best_cost, costs
    