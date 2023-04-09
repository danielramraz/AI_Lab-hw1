# ----------- File Form Lab -----------
import random
import Data
import Individual
import CrossoverOperator
import ParentOperator
from StringIndividual import StringIndividual
from NqueensIndividual import NqueensIndividual
from BinPackingIndividual import BinPackingIndividual
# ----------- Python Package -----------
import numpy as np
import math
# ----------- Consts Name  -----------
STRING = 0
N_QUEENS = 1
BIN_PACKING = 2


class Niche:
    sigma_share: float
    Alpha: float
    t_boltzmann: float
    individuals: list
    fitnesses: list

    def __init__(self, individuals: list):
        self.sigma_share = 2
        self.Alpha = 1
        self.t_boltzmann = 100
        self.individuals = individuals
        self.similarity_matrix = self.init_matrix(individuals)
        self.update_score_share()
        self.fitnesses = [ind.score_share for ind in self.individuals]

    def init_matrix(self, individuals: list):
        matrix = np.zeros((len(individuals), len(individuals)))
        for i in range(len(individuals)):
            for j in range(len(individuals)):
                matrix[i][j] = individuals[i].distance_func(individuals[j], True)

        return matrix

    def update_score_share(self):
        share_score = []

        for ind in self.individuals:
            index_ind = self.individuals.index(ind)
            for j in range(len(self.individuals)):
                dist = self.similarity_matrix[index_ind][j]
                if dist < self.sigma_share:
                    share_score_j = 1 - ((dist/self.sigma_share) ** self.Alpha)
                    share_score.append(share_score_j)
            ind.score_share = ind.score / sum(share_score)

        return

    def generate_individuals(self, data: Data, objects, max_weight, best_fitness):

        offspring = []
        parents_next_generation = []
        niche_size = len(self.individuals)
        while len(offspring) + len(parents_next_generation) < niche_size:
            # ----------- Parent Selection -----------
            parents = ParentOperator.parent_selection_function(data.parent_selection, self.individuals, [])
            parent1 = parents[0]
            parent2 = parents[1]
            parents_next_generation.append(parent1)
            parents_next_generation.append(parent2)

            # ----------- Creating Child -----------
            if data.problem == STRING:
                child = StringIndividual(data)
            elif data.problem == N_QUEENS:
                child = NqueensIndividual(data)
            elif data.problem == BIN_PACKING:
                temp_objects = objects.copy()
                child = BinPackingIndividual(data, temp_objects, max_weight, best_fitness)

            child_gen = CrossoverOperator.crossover_operator(data.cross_operator, parent1, parent2, data.num_genes)
            child.gen = child_gen
            child.gen_len = len(child_gen)

            # ----------- Mutation -----------

            # ----------- Crowding -----------
            # offspring.append(parent1)
            # offspring.append(parent2)
            # offspring = self.crowding(child, parent1, parent2, offspring,)
            parents_next_generation = self.crowding(child, parent1, parent2, offspring, parents_next_generation, niche_size)
            offspring.append(child)

        self.individuals = offspring + parents_next_generation
        while len(self.individuals) > niche_size:
            self.remove_worst_ind()

        return

    def crowding(self, child: Individual, parent1: Individual, parent2: Individual, offspring: list, parents_next_generation: list, niche_size):
        p1_child_dif = -(child.distance_func(parent1, True)) / self.t_boltzmann
        pr_p1 = math.exp(p1_child_dif) / (1 + math.exp(p1_child_dif))

        p2_child_dif = -(child.distance_func(parent2, True)) / self.t_boltzmann
        pr_p2 = math.exp(p2_child_dif) / (1 + math.exp(p2_child_dif))

        if pr_p1 > pr_p2:
            parents_next_generation.remove(parent1)
        else:
            parents_next_generation.remove(parent2)

        if random.random() < pr_p1 and parent1 in parents_next_generation:
            parents_next_generation.remove(parent1)
        elif random.random() <= pr_p2 and parent2 in parents_next_generation:
            parents_next_generation.remove(parent2)

        return parents_next_generation

    def remove_worst_ind(self):
        worst_score = float('inf')
        for ind in self.individuals:
            if ind.score < worst_score:
                worst_score = ind.score
                worst_individual = ind

        self.individuals.remove(worst_individual)
        return





