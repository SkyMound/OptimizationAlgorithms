# Author : FRESARD Tobias


import numpy as np
import random as rd
import matplotlib.pyplot as plt

class TSP :
    def __init__(self, nb_city, max_x, max_y):
        self.nb_city = nb_city
        self.max_x = max_x
        self.max_y = max_y
        self.max_distance = np.linalg.norm(np.array([max_x,max_y])-np.array([0,0]))

        self.city_coords = np.zeros((nb_city,2))
        self.distances = np.zeros((nb_city, nb_city))
        for city_index in range(nb_city) :
            self.city_coords[city_index][0] = rd.randint(0,max_x)
            self.city_coords[city_index][1] = rd.randint(0,max_y)
        
        for source in range(nb_city):
            for target in range(nb_city):
                self.distances[source][target] = self.distances[source][target] = np.linalg.norm(self.city_coords[target]-self.city_coords[source])
    
    
    def plot(self, solution=None, add_to_subplot=False, fig=None, ax=None, path_color='blue'):
        if not add_to_subplot:
            fig, ax = plt.subplots(figsize=(4, 4))

        # Plot the city
        ax.scatter(self.city_coords[:, 0], self.city_coords[:, 1], color=path_color, label='Cities')

        # Plot the solution if specified
        if solution is not None and len(solution) > 0:
            for i in range(self.nb_city):
                ax.plot([self.city_coords[solution[i]][0], self.city_coords[solution[(i + 1)%self.nb_city]][0]],
                        [self.city_coords[solution[i]][1], self.city_coords[solution[(i + 1)%self.nb_city]][1]],
                        color=path_color, linewidth=2)

        if not add_to_subplot:
            return fig, ax
    
    
    def generate_solution(self) :
        return rd.sample(range(self.nb_city),self.nb_city)
    
    def optimize_solution(self, solution) :
        # Apply heursitics to solution
        pass
    
    def rectify(self, solution):
        unique_cities_index = np.unique(solution,return_index=True)[1]
        unique_cities = [solution[index] for index in sorted(unique_cities_index)]
        cities_to_add = np.setdiff1d(np.arange(self.nb_city), unique_cities)
        valid_solution = np.concatenate((unique_cities,cities_to_add))
        return valid_solution
    
    def cost(self, solution) :
        eval=0
        for i in range (len(solution)):
            source,target = solution[i], solution[(i+1)%self.nb_city]
            eval += self.distances[source][target]
        return eval
    
    def get_neighbor(self, solution) :
        index=rd.sample(range(self.nb_city),2)
        neighbor=np.copy(solution)
        (neighbor[index[0]],neighbor[index[1]])=(neighbor[index[1]],neighbor[index[0]])
        return neighbor
    
    def crossover(self, population, nb_crossover, crossover_rate) :
        crossings = np.empty((nb_crossover,self.nb_city),dtype=int)
        crossing_point = int(self.nb_city/2)
        i = 0

        while (i < nb_crossover): 
            x = rd.random()
            if x > crossover_rate:
                continue
            parent_index_1 = i%population.shape[0]
            parent_index_2 = (i+1)%population.shape[0]
            
            crossing = np.zeros(self.nb_city,dtype=int)
            crossing[:crossing_point] = population[parent_index_1, :crossing_point]
            crossing[crossing_point:] = population[parent_index_2, crossing_point:]
            crossing = self.rectify(crossing)
            crossings[i] = crossing
            
            i += 1

        return crossings
    
    def mutation(self, population, mutation_rate) :
        nb_solutions = population.shape[0]
        mutants = np.copy(population)
        for i in range(nb_solutions):
            x = rd.random()
            if x > mutation_rate:
                continue
            
            idx1, idx2 = np.random.choice(self.nb_city, 2, replace=False)
            mutants[i][idx1], mutants[i][idx2] = mutants[i][idx2], mutants[i][idx1]
            mutants[i] = self.rectify(mutants[i])
        return mutants
        
    def get_visibilities(self) :
        return np.copy(self.distances)