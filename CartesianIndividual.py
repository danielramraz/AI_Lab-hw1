from Individual import Individual
import Data
# ----------- Python Package -----------
import random
import numpy as np
# ----------- Consts Parameters -----------
MAX_VALUE = 100000

# ----------- Consts Name  -----------
ORIGINAL_FIT = 0


class CartesianIndividual(Individual):
    
    def __init__(self, data: Data):
        x = random.randint(-MAX_VALUE, MAX_VALUE)
        y = random.randint(-MAX_VALUE, MAX_VALUE)
        self.gen = (x, y)
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0
        self.fitness_function = data.fitness_function
        self.update_score(data)

    def update_score(self, data: Data):
        if self.fitness_function == ORIGINAL_FIT:
            self.score = self.original_fitness(data)

    def original_fitness(self, data: Data):
        score = -(self.gen[0]**2 + self.gen[1]**2)**0.5

        normalized_age = self.age / data.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score

        return int(score)

    def mutation(self, data: Data):
        rand_gen = random.choice([0, 1])
        temp_list = list(self.gen)
        temp_list[rand_gen] = int(self.gen[rand_gen] * random.random())
        self.gen = tuple(temp_list)
        return
    
    def distance_func(self, other_individual, for_individual: bool):
        dist = 0
        dist = (self.gen[0] - other_individual.gen[0])**2 + (self.gen[1] - other_individual.gen[1])**2
        dist = int(dist**0.5)
        return dist + 1

    def genetic_diversification_distance(self, population: list):
        return 0

    def genetic_diversification_special(self, population: list):
        return 0
    