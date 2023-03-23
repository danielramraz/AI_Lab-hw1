from Individual import Individual
import Data
import random


class StringIndividual(Individual):

    def __init__(self, data: Data):
        self.gen = [chr(random.randint(32, 126))for j in range(data.num_genes)]
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0
        self.fitness_function = data.fitness_function
        self.update_score(data)

    def update_score(self, data: Data):
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

        normalized_age = self.age / self.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score

        return score
        # score = data.age_factor*self.age + (1 - data.age_factor)*score

    def bulls_eye_fitness(self, data: Data):
        target = list("Hello, world!")
        score = 0

        for i in range(self.gen_len):
            if self.gen[i] == target[i]:
                score += 1

        for i in range(self.gen_len):
            if self.gen[i] == target[i]:
                score += 10
            elif self.gen[i] in target:
                score += 5

        # bulls_eye_score = data.age_factor * self.age + (1 - data.age_factor) * score
        normalized_age = self.age / self.max_age
        age_score = 1 - normalized_age
        bulls_eye_score = (1 - data.age_factor) * score + data.age_factor * age_score

        return bulls_eye_score

    def mutation(self, data: Data):
        num_genes = self.gen_len
        rand_gen = random.randint(0, num_genes - 1)
        self.gen[rand_gen] = chr(random.randint(32, 126))

    def genetic_diversification_distance(self, population: list):
        dist = 0
        for item in population:
            for index in range(len(self.gen)):
                if item.gen[index] != self.gen[index]:
                    dist += 1

        return dist

    def genetic_diversification_special(self, population: list):
        special_letters = []
        for item in population:
            for letter in item.gen:
                if letter not in special_letters:
                    special_letters.append(letter)

        return len(special_letters)




