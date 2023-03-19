import random
from Individual import Individual


class GeneticDiversification:

    def __init__(self):
        self.DISTANCE_GENES = 0
        self.BEST_INDIVIDUAL = 1

    # def genetic_diversification_operator(self, diversification_operator_input: int, population: list, ):  # exploration
    #
    #     if diversification_operator_input == self.DISTANCE_GENES:
    #        return self.distance_genes(population)
    #
    #     elif diversification_operator_input == self.BEST_INDIVIDUAL:
    #         return self.best_individual(population)
    #
    # def distance_genes(self, population: list):
    #     target = list("Hello, world!")
    #     diversity = 0
    #     for individual in population:
    #         for i in range(individual.gen_len):
    #            if individual.gen[i] != target[i]
    #                diversity += 1
    #
    #     return  6
    #
    # def best_individual(self, population: list):
    #     return 5