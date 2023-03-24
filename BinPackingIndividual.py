from Individual import Individual
import Data
import random
import math


class BinPackingIndividual(Individual):

    def __init__(self, data: Data, objects: list, max_weight: int):
        self.objects = objects.copy()
        self.max_weight = max_weight
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
        temp_objects = objects.copy()
        temp_objects.sort()
        sum_objects = sum(temp_objects)
        num_bins = math.ceil(sum_objects / max_weight) * 2
        gen = []
        for i in range(num_bins):
            gen.append([])

        while temp_objects:
            num_object_in_bin = random.randint(1, len(temp_objects))
            bin = random.randint(0, len(gen)-1)
            for i in range(num_object_in_bin):
                gen[bin].append(temp_objects[0])
                # removing objects that been chosen
                temp_objects.remove(temp_objects[0])

        # temp_objects = (objects.copy()).sort()
        # sum_objects = sum(temp_objects)
        # num_bins = math.ceil(sum_objects/max_weight) * 2
        # gen = []
        #
        # for i in range(num_bins):
        #     num_objects = len(temp_objects)
        #     if i == num_bins-1 or num_objects == 0:
        #         try:
        #             gen.append(temp_objects)
        #         except:
        #             gen.append([])
        #     else:
        #         num_object_in_bin = random.randint(1, num_objects)
        #         gen.append(random.sample(temp_objects, num_object_in_bin))
        #         # removing objects that been chosen
        #         for item in gen[i]:
        #             temp_objects.remove(item)
        return gen

    def original_fitness(self, data: Data):
        score = 100
        illegal_bins = 0
        num_no_empty_bin = 0
        sum_objects = sum(self.objects)

        for i in range(self.gen_len):
            if sum(self.gen[i]) > self.max_weight:
                score -= 1 * (sum(self.gen[i]) - self.max_weight)
                illegal_bins += 1
            if sum(self.gen[i]) > 0:
                num_no_empty_bin += 1

        if illegal_bins > 0:
            score -= illegal_bins * 10

        # # הוספת עונש על גנים עם יותר מדי בינים מלאים
        # if num_no_empty_bin > math.ceil(sum_objects/self.max_weight):
        #     score -= num_no_empty_bin * 5

        normalized_age = self.age / data.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score

        return score

    def mutation(self, data: Data):
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
