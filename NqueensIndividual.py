from Individual import Individual
import Data
import random


class NqueensIndividual(Individual):

    def __init__(self, data: Data):
        self.gen =
        self.gen_len = len(self.gen)
        self.age = 0
        self.fitness_function = data.fitness_function
        if self.fitness_function == 0:
            self.score = self.original_fitness(data)

    def original_fitness(self, data: Data):
        score = 0



        score = data.age_factor*self.age + (1 - data.age_factor)*score
        return score

