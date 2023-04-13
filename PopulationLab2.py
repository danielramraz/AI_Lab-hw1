# ----------- File For Genetic Algorithm -----------
from Data import Data
import FlowManger
from MutationControl import MutationControl
from StringIndividual import StringIndividual
from NqueensIndividual import NqueensIndividual
from BinPackingIndividual import BinPackingIndividual
import Individual
import ParentOperator
import CrossoverOperator
import Clustering
import Niche
# ----------- Python Package -----------
import time
import numpy as np
import matplotlib.pyplot as plt
import math
# ----------- Consts Parameters -----------
MUTATION_INDIVIDUALS = 20
ELITE_PERCENTAGE = 0.20
# ----------- Consts Name  -----------
STRING = 0
N_QUEENS = 1
BIN_PACKING = 2
SHARED_FIT = 0
CLUSTER = 1

class PopulationLab2:
    data: Data
    population: list
    best_fitness: float
    center: Individual
    optimization_func: int
    fitnesses: list

    def __init__(self, setting_vector = None):
        self.data = Data(setting_vector)
        self.population = []
        self.fitnesses = []
        self.best_individual = 0
        self.best_fitness = 0
        self.max_weight = 0
        self.objects = []
        self.niches = []
        
        if self.data.problem == BIN_PACKING:
            self.read_file_bin_packing()
            self.data.num_genes = int(1.5 * (np.sum(self.objects) / self.max_weight))


        for index in range(self.data.pop_size):
            if self.data.problem == STRING:
                individual = StringIndividual(self.data)
            elif self.data.problem == N_QUEENS:
                individual = NqueensIndividual(self.data)
            elif self.data.problem == BIN_PACKING:
                individual = BinPackingIndividual(self.data, self.objects.copy(), self.max_weight, self.best_fitness)

            self.population.append(individual)
        return
    
    def set_fitnesses(self):
        for individual in self.population:
            self.fitnesses.append(individual.score)
        return

    def genetic_algorithm(self):

        # ----------- Printing graphs for the report -----------
        # x1 = []
        # y1 = []
        # ax = plt.axes()
        # ax.set(xlim=(0, 100), ylim=(0, 100), xlabel='Generation number', ylabel='Average fitness')
                
        for generation_index in range(self.data.max_generations):

            # ----------- Clustering -----------
            clusters = Clustering.niche_algorithm(self.population, self.data.niche_algorithm)
            # clusters = Clustering.clustering(self.population)
            self.niches = []

            if self.data.niche_algorithm == SHARED_FIT:
                niche = Niche.Niche(self.population)
                self.niches.append(niche)
            elif self.data.niche_algorithm == CLUSTER:
                for cluster in clusters:
                    niche = Niche.Niche(cluster)
                    self.niches.append(niche)

            # ----------- Print Fitness Information -----------
            gen_time = time.time()
            print(f"========================================= {generation_index}")
            for index, niche in enumerate(self.niches):
                average, variance, sd = self.average_fitness(niche.fitnesses)
                print(f"Average for niche {index} is {average}")
                print(f"Selection Pressure for niche {index} is {variance}")
                # self.show_histogram(niche.fitnesses)
                # x1.append(generation)
                # y1.append(average)

            # ----------- Generate New Individuals -----------
            for niche in self.niches:
                niche.generate_individuals(self.data, 
                                           self.objects, 
                                           self.max_weight, 
                                           self.best_fitness,
                                           generation_index)

            # ----------- Update Population -----------
            self.population = []
            for niche in self.niches:
                for ind in niche.individuals:
                    self.population.append(ind)

            # Update the age of each individual, if reached max_age - remove from population
            for individual in self.population:
                individual.age += 1
                individual.update_score(self.data)
                if individual.age == self.data.max_age:
                    self.population.remove(individual)

            # Update the size of the  population
            self.data.pop_size = len(self.population)

            # ----------- Genetic Diversification -----------
            distance = 0
            for index, niche in enumerate(self.niches):
                for ind in niche.individuals:
                    distance += ind.genetic_diversification_distance(niche.individuals)
                distance = distance / len(self.population)
                special = niche.individuals[0].genetic_diversification_special(niche.individuals)
                print(f"The genetic diversification distance for niche {index} is: {distance}")
                print(f"The genetic diversification special for niche {index} is: {special}")

            # ----------- Print Time Information -----------
            print(f"The absolute time for this gen is {time.time() - gen_time} sec")
            print(f"The ticks time for this gen is {int(time.perf_counter())}")

        # ----------- Best Solution -----------
        # Find the individual with the highest fitness
        self.best_individual = self.population[0]
        for individual in self.population:
            individual.update_score(self.data)
            if self.best_individual.score < individual.score:
                self.best_individual = individual

        self.best_fitness = self.best_individual.score
        # ax.plot(np.array(x1), np.array(y1))
        # plt.show()
        return

    def average_fitness(self, fitness: list):  # information
        if not fitness:
            return 0
        average = sum(fitness) / len(fitness)
        variance = sum([((x - average) ** 2) for x in fitness]) / (len(fitness) - 1)
        sd = variance ** 0.5
        return average, variance, sd

    def show_histogram(self, array):
        np_array = np.array(array)
        plt.hist(np_array)
        plt.show()
        return

    def read_file_bin_packing(self):
        with open("BinPackingTests/binpack1.txt") as f:
            f.readline()
            f.readline()
            list_info = f.readline().split()
            print(list_info)
            self.max_weight = int(list_info[0])
            num_items = int(list_info[1])
            self.best_fitness = int(list_info[2])

            for i in range(num_items):
                self.objects.append(int(f.readline()))