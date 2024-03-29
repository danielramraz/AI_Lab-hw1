# ----------- File Form Lab -----------
import random
from CartesianIndividual import CartesianIndividual
import Data
import Individual
import CrossoverOperator
from MutationControl import MutationControl
import ParentOperator
from StringIndividual import StringIndividual
from NqueensIndividual import NqueensIndividual
from BinPackingIndividual import BinPackingIndividual
# ----------- Python Package -----------
import numpy as np
import math
# ----------- Consts Parameters -----------
ELITE_PERCENTAGE = 0.20
# ----------- Consts Name  -----------
STRING = 0
N_QUEENS = 1
BIN_PACKING = 2
CARTESIAN = 3

SIGMA_SHARE = 2
SHARED_FIT = 0
CLUSTER = 1
CROWDING = 2

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
        self.similarity_matrix = self.init_matrix()
        self.update_score_share()
        self.fitnesses = [ind.score for ind in self.individuals]

    def init_matrix(self):
        niche_size = len(self.individuals)
        matrix = np.zeros((niche_size, niche_size))
        for i in range(niche_size):
            for j in range(niche_size):
                matrix[i][j] = self.individuals[i].distance_func(self.individuals[j], True)

        return matrix

    def update_score_share(self):
        for ind in self.individuals:
            share_score = []
            index_ind = self.individuals.index(ind)
            for j in range(len(self.individuals)):
                dist = self.similarity_matrix[index_ind][j]
                if dist < self.sigma_share:
                    share_score_j = 1 - ((dist/self.sigma_share) ** self.Alpha)
                    share_score.append(share_score_j)
            ind.score_share = ind.score / sum(share_score)
        return

    def generate_individuals(self, data: Data, objects, max_weight, best_fitness, generation_index, elites):
        mutation_control = MutationControl(data, self.average_fitness(self.fitnesses))

        offspring = []
        parents_next_generation = []
        niche_size = len(self.individuals)

        while len(offspring) + len(parents_next_generation) < niche_size:
            # ----------- Parent Selection -----------
            pop = self.individuals + elites
            parents = ParentOperator.parent_selection_function(data.parent_selection, pop, elites)
            parent1 = parents[0]
            parent2 = parents[1]
            # Keeping the chosen parents for the next generation
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
            elif data.problem == CARTESIAN:
                child = CartesianIndividual(data)

            child_gen = CrossoverOperator.crossover_operator(data.cross_operator, parent1, parent2, data.num_genes)
            child.gen = child_gen
            child.gen_len = len(child_gen)

            # ----------- Mutation -----------
            mutation_control.mutation_selection_function(child, 
                                                         generation_index, 
                                                         self.average_fitness(self.fitnesses))
            child.update_score(data)

            # ----------- Crowding -----------
            if data.niche_algorithm == CROWDING:
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

    def average_fitness(self, fitness: list):
        if not fitness:
            return 0
        try:
            average = sum(fitness) / len(fitness)
            variance = sum([((x - average) ** 2) for x in fitness]) / (len(fitness) - 1)
        except:
            average = 0
            variance = 0
        sd = variance ** 0.5
        return average, variance, sd
