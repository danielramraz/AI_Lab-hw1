import random
from Individual import Individual
import Population
import numpy as np
from Data import Data

MUTATION_INDIVIDUALS = 10
MUTATION_DECREASE_FACTOR = 1
MUTATION_LOG_DECREASE_FACTOR = 1.1

class MutationControl:    
    data: Data
    current_generation_index: int
    last_average: float
    current_average: float
    mutation_counter: int

    def __init__(self, data: Data, average_fitness):
        self.NONE = 0
        self.const_mutation = 1
        self.Decrease_linearly = 2
        self.Non_Linear_logistic_decay = 3

        self.current_generation_index = 0
        self.mutation_counter = 0
        self.data = data
        self.current_average = average_fitness[0]
    
    def mutation_selection_function(self, 
                                    individual: Individual,
                                    generation_index: int,
                                    new_average_fitness: float):
        
        if generation_index != self.current_generation_index:
            self.last_average = self.current_average
            self.current_average = new_average_fitness

            if self.data.mutation_control_selection == self.NONE:
                self.average_const_mutation()
            
            elif self.data.mutation_control_selection == self.const_mutation:
                self.const_mutation()
            
            elif self.data.mutation_control_selection == self.Decrease_linearly:
                self.decrease_linearly_mutation()
            
            elif self.data.mutation_control_selection == self.Non_Linear_logistic_decay:
                self.decrease_non_linearly_mutation()

        self.current_generation_index = generation_index 

        if self.mutation_counter > 0:
            individual.mutation(self.data)
            print(f"mutation counter {self.mutation_counter}")
            self.mutation_counter -=1
        return

    def average_const_mutation(self):
        if self.current_average == self.last_average:
            self.mutation_counter = MUTATION_INDIVIDUALS
        else:
            self.mutation_counter = 0
        # print("mutation control 0")
        return
    
    def const_mutation(self):
        self.mutation_counter = MUTATION_INDIVIDUALS
        # print("mutation control 1")
        return
    
    def decrease_linearly_mutation(self):
        # print(f"mutation_counter {self.mutation_counter}, current_generation_index {self.current_generation_index} ")
        self.mutation_counter = int( MUTATION_INDIVIDUALS - (self.current_generation_index * MUTATION_DECREASE_FACTOR))
        return
    
    def decrease_non_linearly_mutation(self):
        # print(f"mutation_counter {self.mutation_counter}, current_generation_index {self.current_generation_index} ")
        self.mutation_counter = int(MUTATION_INDIVIDUALS - self.current_generation_index ** MUTATION_LOG_DECREASE_FACTOR)
        return
