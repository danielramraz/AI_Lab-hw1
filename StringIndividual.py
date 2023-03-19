from Individual import Individual
import Data
import random


class StringIndividual(Individual):

    def __init__(self, data: Data):
        self.gen = [chr(random.randint(32, 126))for j in range(data.num_genes)]
        self.gen_len = len(self.gen)
        self.age = 0
        self.fitness_function = data.fitness_function
        if self.fitness_function == 0:
            self.score = self.original_fitness(data)
        elif self.fitness_function == 1:
            self.score = self.bulls_eye_fitness(data)

    def original_fitness(self, data: Data):
        target = list("Hello, world!")
        score = 0

        for i in range(self.gen_len):
            if self.gen[i] == target[i]:
                score += 1

        score = data.age_factor*self.age + (1 - data.age_factor)*score
        return score

    def bulls_eye_fitness(self, data: Data):
        target = list("Hello, world!")
        score = self.original_fitness()

        for i in range(self.gen_len):
            if self.gen[i] == target[i]:
                score += 10
            elif self.gen[i] in target:
                score += 5

        bulls_eye_score = data.age_factor*self.age + (1 - data.age_factor)*score
        return bulls_eye_score
