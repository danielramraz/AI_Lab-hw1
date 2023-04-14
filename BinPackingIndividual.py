# ----------- File Form Lab -----------
from Individual import Individual
import Data
# ----------- Python Package -----------
import numpy as np
import random
# ----------- Consts Name  -----------
ORIGINAL_FIT = 0
NOT_EMPTY_BINS_DIST = 0
FULL_BINS_DIST = 1


class BinPackingIndividual(Individual):

    def __init__(self, data: Data, objects: list, max_weight: int, best_solution: int):
        self.objects = objects.copy()
        self.max_weight = max_weight
        self.best_solution = best_solution
        self.gen = self.init_bins(data, self.objects, self.max_weight)
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0
        self.fitness_function = data.fitness_function
        self.update_score(data)
        self.distance_func_type = NOT_EMPTY_BINS_DIST

    def update_score(self, data: Data):
        if self.fitness_function == ORIGINAL_FIT:
            self.score = self.original_fitness(data)

    def init_bins(self, data: Data, objects: list, max_weight: int):
        copy_objects = objects.copy()
        num_bins = int(1.5 * (np.sum(copy_objects) / self.max_weight))
        gen = []

        for i in range(num_bins):  # init the gen with empty num_bins
            gen.append([])

        gen_index = 0
        while copy_objects:  # insert objects to bins randomly but uniformly
            rand_objects_index = random.randint(0, len(copy_objects) - 1)
            gen[gen_index].append(copy_objects[rand_objects_index])
            copy_objects.pop(rand_objects_index)
            rand_int = random.randint(1, 100)
            gen_index = (gen_index + rand_int) % num_bins

        return gen

    def original_fitness(self, data: Data):
        # #------------------------------------------
        # best_fit = list(filter(None, self.gen))
        # for bin in best_fit:
        #     score += (sum(bin) / self.max_weight)
        #
        # score = score / len(best_fit)
        # #----------------------------------------
        score = 0
        over_weight_punishment = 10000
        empty_bin_score = 100

        for i in range(self.gen_len):
            bin_is_over_wieght = sum(self.gen[i]) > self.max_weight
            bin_is_empty = not bool(self.gen[i])

            if bin_is_empty:  # reword for empty bin
                score += empty_bin_score

            elif bin_is_over_wieght:  # punishment for over wieght bin
                over_weight_deviation = sum(self.gen[i]) - self.max_weight
                score -= over_weight_deviation * over_weight_punishment
                # score -= over_wieght_punishment
                # illegal_bins += 1

            else:  # punishment for empty space in the bin
                under_weight_deviation = self.max_weight - sum(self.gen[i])
                score -= under_weight_deviation ** 2  # under_wieght_punishment

        # if illegal_bins > 0:
        # score -= illegal_bins * 10
        # if illegal_bins > 0:
        # score -= illegal_bins * 10

        normalized_age = self.age / data.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score

        return score

    def mutation(self, data: Data):

        max_try = len(self.objects)*2
        min_bin = 0
        min_bin_avr = float('inf')
        for index, bin in enumerate(self.gen):
            if len(bin) > 0 and sum(bin)/len(bin) < min_bin_avr:
                min_bin = index
                min_bin_avr = sum(bin)/len(bin)

        for object in self.gen[min_bin]:
            random_bin = random.randint(0, self.gen_len-1)
            while max_try and(min_bin == random_bin or object + sum(self.gen[random_bin]) > self.max_weight or sum(self.gen[random_bin]) == 0):
                random_bin = random.randint(0, self.gen_len-1)
                max_try -= 1
            if max_try > 0:
                self.gen[random_bin].append(object)
        if max_try > 0:
            self.gen[min_bin] = []
            self.gen_len = len(self.gen)

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
                dist += abs(full_cells_self - full_cells_item)
                dist += abs(full_cells_self - full_cells_item)
                full_cells_item = 0

        dist = dist / len(population)
        dist = dist / len(population)
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

    def distance_func(self, population, for_individual: bool):
        if self.distance_func_type == NOT_EMPTY_BINS_DIST:
            if for_individual:
                return self.not_empty_bins_distance_individual(population)
            else:
                return self.not_empty_bins_distance(population)

        elif self.distance_func_type == FULL_BINS_DIST:
            if for_individual:
                return self.max_full_bins_distance_individual(population)
            else:
                return self.max_full_bins_distance(population)

    def not_empty_bins_distance(self, population: list):
        dist = 0
        full_cells_self = 0
        full_cells_item = 0
        for item in self.gen:
            if sum(item) > 0:
                full_cells_self += 1

        for individual in population:
            for item in individual.gen:
                if sum(item) > 0:
                    full_cells_item += 1
                dist += abs(full_cells_self - full_cells_item)
                full_cells_item = 0

        dist = dist / len(population)
        return dist+1

    def max_full_bins_distance(self, population: list):
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
                dist += abs(full_cells_self - full_cells_item)
                full_cells_item = 0

        dist = dist / len(population)
        return dist+1

    def not_empty_bins_distance_individual(self, ind: Individual):
        full_cells_self = 0
        full_cells_ind = 0
        for item in self.gen:
            if sum(item) > 0:
                full_cells_self += 1

        for item in ind.gen:
            if sum(item) > 0:
                full_cells_ind += 1

        dist = abs(full_cells_self - full_cells_ind)
        return dist+1

    def max_full_bins_distance_individual(self, ind: Individual):
        full_cells_self = 0
        full_cells_ind = 0
        for item in self.gen:
            if sum(item) >= self.max_weight:
                full_cells_self += 1

        for item in ind.gen:
            if sum(item) >= self.max_weight:
                full_cells_ind += 1
        dist = abs(full_cells_self - full_cells_ind)

        return dist+1

    def best_bin_func(self):
        # best_fit = []
        # objects_best_fit_bins_num = []
        #
        # # mack best fit gen
        # copy_objects = self.objects.copy()
        # copy_objects.sort()
        # copy_objects.reverse()
        # min_dif = float('inf')
        # best_bin = 0
        #
        # for object in copy_objects:
        #     if not best_fit:
        #         best_fit.append([])
        #         best_fit[0].append(object)
        #         objects_best_fit_bins_num.append(0)
        #     else:
        #         for index, bin in enumerate(best_fit):
        #             if self.max_weight - sum(bin) < min_dif and sum(bin) + int(object) <= self.max_weight:
        #                 min_dif = self.max_weight - sum(bin)
        #                 best_bin = index
        #         if min_dif != float('inf'):
        #             best_fit[best_bin].append(object)
        #             objects_best_fit_bins_num.append(best_bin)
        #         else:
        #             best_fit.append([])
        #             best_fit[len(best_fit) - 1].append(object)
        #             objects_best_fit_bins_num.append(len(best_fit) - 1)
        #     min_dif = float('inf')
        #
        # bad_bins = 0
        # best_fit = list(filter(None, best_fit))
        # for item in best_fit:
        #     if sum(item) > self.max_weight:
        #         bad_bins += 1
        #
        # print("Best individual:", best_fit)
        # print("NUM bins:", len(best_fit))
        # print("BAD bins:", bad_bins)
        return