import random
from Individual import Individual
import numpy as np

class ParentOperator:
    def __init__(self):
        self.RWS = 0
        self.SUS = 1
        self.TOURNAMENT_RANKING = 2

    def parent_selection_function(self, parent_selection_input: int, population: list, next_generation: int):
        if parent_selection_input == self.RWS:
            return self.rws(population)
        elif parent_selection_input == self.SUS:
            return self.sus(population, next_generation)
        elif parent_selection_input == self.TOURNAMENT_RANKING:
            return self.tournament_ranking()

    def rws(self, population: list) -> Individual:
        sum_score = self.score_sum(population)
        weight_arr = []
        for individual in population:
            weight_arr.append(individual.score[1]/sum_score)

        # print(f"result type {type(result)}")
        # print(f"choice {type(random.choices(population, weights = weight_arr, k = 1)[0])}")
        return (random.choices(population, weights=weight_arr, k=1))[0]

    def sus(self, population: list, next_generation: int):
        #sum_score = self.score_sum(population)
        #weight_arr = []
        #for individual in population:
            #weight_arr.append(individual.score[1]/sum_score)

        #parent1 = (random.choices(population, weights=weight_arr, k=1))[0]
        #slice_size = next_generation/360

        return

    def tournament_ranking(self):
        return 7

    def score_sum(self, population):
        sum_score = 0
        for individual in population:
            sum_score += individual.score[1]
        print(f"sum score {sum_score}")
        return sum_score
