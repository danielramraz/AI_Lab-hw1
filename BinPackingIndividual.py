from Individual import Individual
import Data
import random
import math


class BinPackingIndividual(Individual):

    def __init__(self, data: Data, objects: list, max_weight: int, best_solution: int):
        self.objects = objects.copy()
        self.max_weight = max_weight
        self.best_solution = best_solution
        self.gen = self.mack_bins(data,  self.objects, self.max_weight)
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0
        self.max_weight = max_weight
        self.fitness_function = data.fitness_function
        self.update_score(data)

    def update_score(self, data: Data):
        if self.fitness_function == 0:
            self.score = self.original_fitness(data)

    def mack_bins(self, data: Data, objects: list, max_weight: int):
        copy_objects = objects.copy()
        num_bins = len(copy_objects)
        bins_list = []
        gen = []

        for i in range(num_bins):
            gen.append([])
            bins_list.append(i)

        while copy_objects:
            num_object_in_bin = random.randint(1, len(copy_objects))
            bin = random.sample(bins_list, 1)[0]
            bins_list.remove(bin)
            for i in range(num_object_in_bin):
                object = random.sample(copy_objects, 1)[0]
                gen[bin].append(object)
                # removing objects that been chosen
                copy_objects.remove(object)

        return gen

    def original_fitness(self, data: Data):
        score = 10000
        illegal_bins = 0

        for i in range(self.gen_len):
            if sum(self.gen[i]) > self.max_weight:
                score -= 5 * (sum(self.gen[i]) - self.max_weight)
                illegal_bins += 1

        if illegal_bins > 0:
            score -= illegal_bins * 10

        normalized_age = self.age / data.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score

        return score

    def mutation(self, data: Data):
        copy_objects = self.objects.copy()
        num_objects_change = random.randint(0, len(copy_objects))

        for i in range(num_objects_change):
            random_bin = random.randint(0, len(self.gen) - 1)
            object = random.sample(copy_objects, 1)[0]
            for bin in range(len(self.gen)):
                if object in self.gen[bin]:
                    self.gen[bin].remove(object)
                    copy_objects.remove(object)
                    self.gen[random_bin].append(object)
                    break
        return

    # Calculates the difference between the amount of full cells in the current gene and every other gene in the population
    def genetic_diversification_distance(self, population: list):
        dist = 0
        full_cells_self = 0
        full_cells_item = 0
        for item in self.gen:
            if sum(item) >= self.max_weight:
                full_cells_self += 1

        for individual in population:
            for item in individual.gen:
                if sum(item) >= self.max_weight:
                    full_cells_item += 1
                dist += abs(full_cells_self-full_cells_item)
                full_cells_item = 0

        return dist

    # Calculates the number of unique individual by number of full cells
    def genetic_diversification_special(self, population: list):
        special_individual = []
        full_cells_self = 0
        for individual in population:
            for item in individual.gen:
                if sum(item) >= self.max_weight:
                    full_cells_self += 1
            if full_cells_self not in special_individual:
                special_individual.append(full_cells_self)
            full_cells_self = 0

        return len(special_individual)
