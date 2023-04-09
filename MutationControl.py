import random
# from Individual import Individual
# import Population
import numpy as np
from Data import Data

from Individual import Individual

MUTATION_INDIVIDUALS = 10
MUTATION_FACTOR = 2


class MutationControl:
    mutation_individuals = MUTATION_INDIVIDUALS
    mutation_factor = MUTATION_FACTOR
    
    data: Data
    max_generations: int
    current_generation: int

    last_average: float
    current_average: float

    
    def __init__(self, data: Data, average_fitness):
        self.NONE = 0
        self.const_mutation = 1
        self.Decrease_linearly = 2
        self.Non_Linear_logistic_decay = 3
        self.data = data
        self.current_average = average_fitness[0]

    def mutation_selection_function(self, 
                                    mutation_control_selection: int, 
                                    individual: Individual):

        if self.mutation_average_test():
            return
        
        if mutation_control_selection == self.NONE:
            return self.mutation_control_0(individual)
        
        elif mutation_control_selection == self.const_mutation:
            return self.mutation_control_1(individual)
        
        elif mutation_control_selection == self.Decrease_linearly:
            return self.mutation_control_2(individual)
        
        elif mutation_control_selection == self.Non_Linear_logistic_decay:
            return self.mutation_control_3(individual)
        return
    
    def mutation_average_test():
        return
    
    def mutation_control_0():
        return
    
    def mutation_control_1():
        return
    
    def mutation_control_2():
        return
    
    def mutation_control_3():
        return
