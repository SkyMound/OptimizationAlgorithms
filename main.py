# Author : FRESARD Tobias


from TSP import TSP 
from SimulatedAnnealing import SimulatedAnnealing
from GeneticAlgorithm import GeneticAlgorithm
from AntColony import AntColony
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__' :

    # Données du problème (générées aléatoirement)
    NOMBRE_DE_VILLES = 20
    MAX_X = 2000
    MAX_Y = 2000
    tsp = TSP(NOMBRE_DE_VILLES,MAX_X,MAX_Y)
    
    
    # S1 = SimulatedAnnealing(temperature=500,factor=0.99)
    # S2 = GeneticAlgorithm(crossover_rate=0.6,mutation_rate=0.6)
    S1 = AntColony(evaporation_rate = 0.1,exploitation_rate=5,exploration_rate=1,k=100)
    S2 = AntColony(evaporation_rate = 0.5,exploitation_rate=5,exploration_rate=1,k=100)
    S3 = AntColony(evaporation_rate = 0.5,exploitation_rate=4,exploration_rate=4,k=100)
    
    TIMEOUT = 10
    best_solution, best_cost, _ = S1.solve(tsp,10000,NOMBRE_DE_VILLES,timeout=TIMEOUT)
    
    tsp.plot(best_solution)
    # nb_cities = np.linspace(10,70,10,dtype=int)
    # costs_S1 = np.zeros(nb_cities.size)
    # costs_S2 = np.zeros(nb_cities.size)
    # costs_S3 = np.zeros(nb_cities.size)
    # i = 0
    # for nb_city in nb_cities :
    #     tsp = TSP(nb_city,MAX_X,MAX_Y)
    #     S1_best_solution, costs_S1[i], _ =S1.solve(tsp,100000,nb_city,timeout=TIMEOUT)
    #     S2_best_solution, costs_S2[i], _ =S2.solve(tsp,100000,nb_city,timeout=TIMEOUT)
    #     S3_best_solution, costs_S3[i], _ =S3.solve(tsp,100000,nb_city,timeout=TIMEOUT)
    #     i+=1
    
    # plt.plot(nb_cities,costs_S1,label="expl=5;expr=1")
    # plt.plot(nb_cities,costs_S2,label="expl=1;expr=5")
    # plt.plot(nb_cities,costs_S3,label="expl=4;expr=4")
    plt.xlabel("Nombre de villes")
    plt.ylabel("Coût")
    plt.legend()
    
    
    
    plt.show()
   