import random
# from Individual import Individual
# import Population
import numpy as np

MUTATION_INDIVIDUALS = 10

class MutationControl:
    mutation_individuals = MUTATION_INDIVIDUALS
    
    def __init__(self):
        self.NONE = 0
        self.const_mutation = 1
        self.Decrease_linearly = 2
        self.Non_Linear_logistic_decay = 3

    def mutation_selection_function(self, 
                                    mutation_control_selection: int, 
                                    population: list):
        
        if mutation_control_selection == self.NONE:
            return self.mutation_control_0(population)
        
        elif mutation_control_selection == self.const_mutation:
            return self.mutation_control_1(population)
        
        elif mutation_control_selection == self.Decrease_linearly:
            return self.mutation_control_2(population)
        
        elif mutation_control_selection == self.Non_Linear_logistic_decay:
            return self.mutation_control_3(population)
        return
    
    def mutation_control_0():
        return
    
    def mutation_control_1():
        return
    
    def mutation_control_2():
        return
    
    def mutation_control_3():
        return
