# -*- coding: utf-8 -*-
"""implement ACO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SSoKmmVULLr-seEm_ipvKYUGKckFiZHH
"""

import numpy as np
import pandas as pd
import random

# define the ACO function
def ACO(data, num_ants, num_iterations, alpha, beta, rho, Q):
    
    # create a distance matrix from the data
    dist_matrix = np.array(data)
    np.fill_diagonal(dist_matrix, np.inf)
    
    # initialize the pheromone trail matrix
    pheromone_matrix = np.ones(dist_matrix.shape) / dist_matrix
    
    # initialize the best solution and its length
    best_solution = []
    best_length = np.inf
    
    # perform iterations of the algorithm
    for iter in range(num_iterations):
        
        # initialize the ant solutions and their lengths
        ant_solutions = []
        ant_lengths = []
        
        # run the ant colony
        for ant in range(num_ants):
            
            # initialize the ant's solution and visited nodes
            curr_node = random.randint(0, dist_matrix.shape[0] - 1)
            ant_solution = [curr_node]
            visited = [curr_node]
            
            # move the ant to the next node until all nodes are visited
            while len(visited) < dist_matrix.shape[0]:
                
                # calculate the probabilities of moving to each neighboring node
                probs = np.power(pheromone_matrix[curr_node] , alpha) * \
                        np.power(1.0 / dist_matrix[curr_node], beta)
                probs[visited] = 0
                probs /= np.sum(probs)
                
                # choose the next node based on the probabilities
                next_node = np.random.choice(np.arange(dist_matrix.shape[0]), p=probs)
                
                # update the ant's solution and visited nodes
                ant_solution.append(next_node)
                visited.append(next_node)
                curr_node = next_node
                
            # calculate the length of the ant's solution
            ant_length = sum([dist_matrix[ant_solution[i], ant_solution[i+1]] for i in range(len(ant_solution)-1)])
            
            # update the best solution if the ant's solution is better
            if ant_length < best_length:
                best_solution = ant_solution
                best_length = ant_length
                
            # store the ant's solution and its length
            ant_solutions.append(ant_solution)
            ant_lengths.append(ant_length)
        
        # update the pheromone trail on each edge
        delta_pheromone = np.zeros(dist_matrix.shape)
        for ant_solution, ant_length in zip(ant_solutions, ant_lengths):
            for i in range(len(ant_solution)-1):
                delta_pheromone[ant_solution[i], ant_solution[i+1]] += Q / ant_length
        pheromone_matrix = (1 - rho) * pheromone_matrix + delta_pheromone
        
    # return the best solution and its length
    return best_solution, best_length

# read the data from a CSV file
data = pd.read_csv('data.csv')
cardiff_scale = data['cardiff_scale'].values
gdp = data['gdp'].values

# normalize the data
cardiff_scale_norm = (cardiff_scale - np.min(cardiff_scale)) / (np.max(cardiff_scale) - np.min(cardiff_scale))
gdp_norm = (gdp - np.min(gdp)) / (np.max(gdp) - np.min(gdp))

# combine the normalized data into a matrix
data_norm = np.column_stack((cardiff_scale_norm, gdp_norm))