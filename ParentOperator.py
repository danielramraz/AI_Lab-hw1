import random
from Individual import Individual
import numpy as np

class ParentOperator:
    def __init__(self):
        self.NONE = 0
        self.RWS = 1
        self.SUS = 2
        self.TOURNAMENT_RANKING = 3

    def parent_selection_function(self, parent_selection_input: int, population: list):
        if parent_selection_input == self.RWS:
            return self.rws(population)
        elif parent_selection_input == self.SUS:
            return self.sus(population)
        elif parent_selection_input == self.TOURNAMENT_RANKING:
            return self.tournament_ranking(population)
        
        return 
    
    def rws(self, population: list):
        sum_score = self.score_sum(population)
        fitness = self.scale(population)
        weight_arr = []
        for index in range(len(fitness)):
            weight_arr.append(fitness[index]/sum_score)

        return random.choices(population, weights=weight_arr, k=2)

    def sus(self, population: list):
        sum_score = self.score_sum(population)
        fitness = self.scale(population)
        for index, individual in enumerate(population):
            if index > 0:
                fitness[index] += fitness[index-1]

        parents = []
        number_of_parents = 2
        slice_size = int(sum_score/len(population))
        first_spine_pointer = int(random.uniform(0, slice_size))
        delta = sum_score / number_of_parents

        for i in range(number_of_parents):
            fit = first_spine_pointer + i * delta
            current, j = 0, 0
            while current < fit:
                current += population[j].score[1]
                j += 1
            parents.append(population[j])

        return parents

    def tournament_ranking(self, population: list):

        number_of_competitors = 30
        number_of_parents = 2
        k_fitness = []

        k_individual = random.choices(population, k=number_of_competitors)
        for individual in k_individual:
            k_fitness.append(individual.score[1])

        k_sorted = sorted(range(number_of_competitors), key=lambda i: k_fitness[i], reverse=True)[:number_of_parents]
        parents = [k_individual[i] for i in k_sorted]

        return parents

    def score_sum(self, population):
        sum_score = 0
        for individual in population:
            sum_score += individual.score[1]
        # print(f"sum score {sum_score}")
        return sum_score

    def return_fitnesses(self, individual: Individual):
        return individual.score[1]

    def scale(self, population: list):
        scaled_fitnesses = []
        for individual in population:
            if individual.score[1] != 0:
                scaled_fitnesses.append(1/individual.score[1]**0.5)
            else:
                scaled_fitnesses.append(0)
        return scaled_fitnesses
