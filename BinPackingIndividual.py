import numpy as np
from Individual import Individual
import Data
import random
import math


class BinPackingIndividual(Individual):

    def __init__(self, data: Data, objects: list, max_weight: int, best_solution: int):
        self.objects = objects.copy()
        self.max_weight = max_weight
        self.best_solution = best_solution
        self.gen = self.init_bins(data,  self.objects, self.max_weight)
        self.gen_len = len(self.gen)
        self.age = 0
        self.score = 0
        self.max_weight = max_weight
        self.fitness_function = data.fitness_function
        self.update_score(data)

    def update_score(self, data: Data):
        if self.fitness_function == 0:
            self.score = self.original_fitness(data)

    def init_bins(self, data: Data, objects: list, max_weight: int):    ############
        copy_objects = objects.copy()
                                                                        # how many bins to start with ?
        # num_bins = len(copy_objects)                                  # as many as the objects
        num_bins = int(1.5*(np.sum(copy_objects)/self.max_weight))        # K times the lower bound (average weight)
        # num_bins = int(1.5 * self.best_solution)                      # K times the best solution

        # bins_list = []
        gen = []

        for i in range(num_bins):                               #init the gen with empty num_bins
            gen.append([])
            # bins_list.append(i)

        # while copy_objects:                                          
        #     num_object_in_bin = random.randint(1, len(copy_objects))
        #     bin = random.sample(bins_list, 1)[0]
        #     bins_list.remove(bin)
        #     for i in range(num_object_in_bin):
        #         object = random.sample(copy_objects, 1)[0]
        #         gen[bin].append(object)
        #         # removing objects that been chosen
        #         copy_objects.remove(object)

        gen_index = 0
        while copy_objects:                                         # insert objects to bins randomly but uniformly
            # print(f"copy objects len is {len(copy_objects)}")
            rand_objects_index = random.randint(0, len(copy_objects)-1)
            # print(f"rand_index is {rand_objects_index}")
            gen[gen_index].append(copy_objects[rand_objects_index])
            copy_objects.pop(rand_objects_index)
            rand_int = random.randint(1, 100)
            gen_index = (gen_index + rand_int) % num_bins

        # print(gen)
        return gen

    def original_fitness(self, data: Data):                             ############
        score = 0
        over_weight_punishment = 1000000
        empty_bin_score = 100
        under_wieght_punishment = 10   
        for i in range(self.gen_len):
            bin_is_over_wieght = sum(self.gen[i]) > self.max_weight
            bin_is_empty = not bool(self.gen[i])
            if bin_is_empty:                                                    #reword for empty bin
                score += empty_bin_score
            elif bin_is_over_wieght:                                            #punishment for over wieght bin
                over_weight_deviation = sum(self.gen[i]) - self.max_weight
                score -= over_weight_deviation * over_weight_punishment
                # score -= over_wieght_punishment       
                # illegal_bins += 1
            else:                                                               #punishment for empty space in the bin
                under_weight_deviation = self.max_weight - sum(self.gen[i])
                score -= under_weight_deviation **2 # under_wieght_punishment

        normalized_age = self.age / data.max_age
        age_score = 1 - normalized_age
        score = (1 - data.age_factor) * score + data.age_factor * age_score

        return score

    def jankovic_fitness(self, data: Data):
        score = 0
        k :float = 2                        #constant greater then 1
        for i in range(self.gen_len):
            sum_of_relative_fill = sum(self.gen[i]) / self.max_weight
        clean_gen_sol = list(filter(None, self.gen))
        score = (sum_of_relative_fill / len(clean_gen_sol))** k
        return score

    def mutation(self, data: Data):                                     ############
        copy_objects = self.objects.copy()
        num_objects_change = random.randint(0, len(copy_objects))

        for i in range(num_objects_change):
            random_bin = random.randint(0, len(self.gen) - 1)
            object = random.sample(copy_objects, 1)[0]
            for bin in range(len(self.gen)):
                if object in self.gen[bin]:
                    while object + sum(self.gen[random_bin])>self.max_weight :
                        random_bin = random.randint(0, self.gen_len-1)
                    self.gen[bin].remove(object)
                    copy_objects.remove(object)
                    self.gen[random_bin].append(object)
                    break

        # copy_gen = self.gen.copy()
        # lowest_bin = self.max_weight
        # lowest_bin_index:int
        # for bin, index in copy_gen:
        #     if sum(bin) < lowest_bin:
        #         lowest_bin = sum(bin)
        #         lowest_bin_index = index

        # for object in copy_gen[lowest_bin_index]:
        #     while 

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

    def best_bin_func(self):
        best_fit = []
        objects_best_fit_bins_num = []

        # mack best fit gen
        copy_objects = self.objects.copy()
        copy_objects.sort()
        copy_objects.reverse()
        min_dif = float('inf')
        best_bin = 0

        for object in copy_objects:
            if not best_fit:
                best_fit.append([])
                best_fit[0].append(object)
                objects_best_fit_bins_num.append(0)
            else:
                for index, bin in enumerate(best_fit):
                    if self.max_weight - sum(bin) < min_dif and sum(bin) + int(object) <= self.max_weight:
                        min_dif = self.max_weight - sum(bin)
                        best_bin = index
                if min_dif != float('inf'):
                    best_fit[best_bin].append(object)
                    objects_best_fit_bins_num.append(best_bin)
                else:
                    best_fit.append([])
                    best_fit[len(best_fit) - 1].append(object)
                    objects_best_fit_bins_num.append(len(best_fit) - 1)
            min_dif = float('inf')

        bad_bins = 0
        best_fit = list(filter(None, best_fit))
        for item in best_fit:
            if sum(item) > self.max_weight:
                bad_bins += 1

        print("Best individual:", best_fit)
        print("NUM bins:", len(best_fit))
        print("BAD bins:", bad_bins)
        return