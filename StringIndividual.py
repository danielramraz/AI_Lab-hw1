# ----------- File Form Lab -----------
from Individual import Individual
import Data
# ----------- Python Package -----------
import random
import numpy as np
# ----------- Consts Name  -----------
EDIT_DIST = 0
HAMMING_DIST = 1
ORIGINAL_FIT = 0
BULLS_EYE_FIT = 1
BITWISE_BULLS_EYE_FIT = 2


class StringIndividual(Individual):
    target = list("Hello, world!")

    def __init__(self, data: Data):
        self.gen = [chr(random.randint(32, 126)) for j in range(data.num_genes)]
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0
        self.fitness_function = data.fitness_function
        self.update_score(data)
        self.distance_func_type = EDIT_DIST

    def update_score(self, data: Data):
        if self.fitness_function == ORIGINAL_FIT:
            self.score = self.original_fitness(data)
        elif self.fitness_function == BULLS_EYE_FIT:
            self.score = self.bulls_eye_fitness(data)
        elif self.fitness_function == BITWISE_BULLS_EYE_FIT:
            self.score = self.bitwise_bulls_eye_fitness(data)

    def original_fitness(self, data: Data):
        score = 0

        for i in range(self.gen_len):
            if self.gen[i] == self.target[i]:
                score += 1

        normalized_age = self.age / data.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score

        return score

    def bitwise_bulls_eye_fitness(self, data: Data):
        bitwise_score = 0

        for i in range(self.gen_len):
            if self.gen[i] == self.target[i]:
                bitwise_score += 50
            else:
                score = ord(self.target[i]) | ord(self.gen[i])
                score = bin(~score).count("1")
                bitwise_score += score
        return bitwise_score

    def bulls_eye_fitness(self, data: Data):
        score = 0

        for i in range(self.gen_len):
            if self.gen[i] == self.target[i]:
                score += 1

        for i in range(self.gen_len):
            if self.gen[i] == self.target[i]:
                score += 10
            elif self.gen[i] in self.target:
                score += 5

        normalized_age = self.age / data.max_age
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

        dist = dist / len(population)
        return dist

    def genetic_diversification_special(self, population: list):
        special_letters = []
        for item in population:
            for letter in item.gen:
                if letter not in special_letters:
                    special_letters.append(letter)

        return len(special_letters)

    def distance_func(self, population, for_individual: bool):
        if self.distance_func_type == EDIT_DIST:
            if for_individual:
                return self.edit_distance_individual(population)
            else:
                return self.edit_distance(population)

        elif self.distance_func_type == HAMMING_DIST:
            if for_individual:
                return self.hamming_distance_individual(population)
            else:
                return self.hamming_distance(population)

    def edit_distance(self, population: list):
        dist = 0
        for item in population:
            dist_matrix = np.zeros([self.gen_len, item.gen_len])
            for index_gen in range(len(self.gen)):
                dist_matrix[index_gen, 0] = index_gen
            for index_item in range(len(item.gen)):
                dist_matrix[0, index_item] = index_item

            for index_item in range(item.gen_len):
                for index_gen in range(self.gen_len):
                    if self.gen[index_gen] == item.gen[index_item]:
                        dist_matrix[index_gen, index_item] = dist_matrix[index_gen - 1, index_item - 1]
                    else:
                        dist_matrix[index_gen, index_item] = min(dist_matrix[index_gen - 1, index_item] + 1,        # deletion
                                                                 dist_matrix[index_gen, index_item - 1] + 1,        # insertion
                                                                 dist_matrix[index_gen - 1, index_item - 1] + 1)    # substitution
            dist += dist_matrix[self.gen_len - 1, item.gen_len - 1]

        dist = dist / len(population)
        return dist

    def hamming_distance(self, population: list):
        dist = 0
        for item in population:
            for index in range(self.gen_len):
                if item.gen[index] != self.gen[index]:
                    dist += 1

        dist = dist / len(population)
        return dist

    def edit_distance_individual(self, ind: Individual):
        dist_matrix = np.zeros([self.gen_len, ind.gen_len])
        for index_item in range(ind.gen_len):
            for index_gen in range(self.gen_len):
                if self.gen[index_gen] == ind.gen[index_item]:
                    dist_matrix[index_gen, index_item] = dist_matrix[index_gen - 1, index_item - 1]
                else:
                    dist_matrix[index_gen, index_item] = min(dist_matrix[index_gen - 1, index_item] + 1,  # deletion
                                                             dist_matrix[index_gen, index_item - 1] + 1,  # insertion
                                                             dist_matrix[
                                                                 index_gen - 1, index_item - 1] + 1)  # substitution
        dist = dist_matrix[self.gen_len - 1, ind.gen_len - 1]
        return dist

    def hamming_distance_individual(self, ind: Individual):
        dist = 0
        for index in range(self.gen_len):
            if ind.gen[index] != self.gen[index]:
                dist += 1

        return dist






