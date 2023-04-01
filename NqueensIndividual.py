import numpy as np
from Individual import Individual
import Data
import random


class NqueensIndividual(Individual):

    def __init__(self, data: Data):
        self.gen = random.sample(range(1, data.num_genes+1), data.num_genes)
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0
        self.fitness_function = data.fitness_function
        self.update_score(data)

    def update_score(self, data: Data):
        if self.fitness_function == 0:
            self.score = self.original_fitness(data)

    def original_fitness(self, data: Data):
        score = 100
        for i in range(self.gen_len):
            if self.gen.count(i + 1) != 1:
                score -= 10

            for j in range(self.gen_len):
                if i != j and abs(i - j) == abs(self.gen[i] - self.gen[j]):
                    score -= 1

        normalized_age = self.age / data.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score
        return score

    def mutation(self, data: Data):
        if data.mutation == 2:
            self.invertion_shuffle()
        elif data.mutation == 3:
            self.just_shuffle()
        return

    def invertion_shuffle(self):
        start = random.randint(0, self.gen_len)
        end = random.randint(start, self.gen_len)
        replace = random.randint(0, self.gen_len - (end - start))
        local_gen = self.gen

        if start == end:
            return

        sub_gen = local_gen[start:end]
        for i in range(len(sub_gen)):
            local_gen.pop(start)

        random.shuffle(sub_gen)
        local_gen = local_gen[:replace] + sub_gen + local_gen[replace:]
        self.gen = local_gen

        return

    def just_shuffle(self):
        random.shuffle(self.gen)

        return

    # Calculates the amount of swap to get from the current gene to every other gene in the population
    def genetic_diversification_distance(self, population: list):
        dist = 0
        conflict_self = 0
        conflict_item = 0
        for i in range(self.gen_len):
            for j in range(self.gen_len):
                if i != j and abs(i - j) == abs(self.gen[i] - self.gen[j]):
                    conflict_self += 1

        for item in population:
            for i in range(self.gen_len):
                for j in range(self.gen_len):
                    if i != j and abs(i - j) == abs(self.gen[i] - self.gen[j]):
                        conflict_item += 1
            dist += abs(conflict_self-conflict_item)
            conflict_item = 0

        dist = dist / len(population)
        return dist

    # Calculates the number of unique promotions
    def genetic_diversification_special(self, population: list):
        special_permutation = []
        for item in population:
            if item.gen not in special_permutation:
                special_permutation.append(item.gen)

        return len(special_permutation)

    def kendall_tau_distance(self, population: list):

        dist = 0
        ndisordered = 0
        for item in population:
            i, j = np.meshgrid(np.arange(self.gen_len), np.arange(item.gen_len))
            a = np.argsort(self.gen)
            b = np.argsort(item.gen_len)
            ndisordered = np.logical_or(np.logical_and(a[i] < a[j], b[i] > b[j]),
                                        np.logical_and(a[i] > a[j], b[i] < b[j])).sum()
            dist += ndisordered / (self.gen_len * (self.gen_len - 1))

        dist = dist / len(population)  # ask shy???

        return dist
