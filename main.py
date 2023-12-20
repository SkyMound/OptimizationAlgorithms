# Author : FRESARD Tobias


from Problems.KnapSac import KnapSac
from Algorithms.QuanticGeneticAlgorithm import QuanticGeneticAlgorithm
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__' :

    # Données du problème générées aléatoirement
    NB_OBJECTS = 10   #Le nombre d'objets
    CAPACITY_MAX = 30    #La capacité du sac 
    ks = KnapSac(NB_OBJECTS,CAPACITY_MAX)
    
    
    S1 = QuanticGeneticAlgorithm()
    
    
    TIMEOUT = 10
    best_solution, best_cost, costs = S1.solve(ks,100,1)
    print(best_solution)
    # ks.plot(best_solution)
    
    # plt.xlabel("Nombre de villes")
    # plt.ylabel("Coût")
    # plt.legend()
    
    plt.plot(costs)
    
    plt.show()
   