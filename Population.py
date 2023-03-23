from StringIndividual import StringIndividual
from NqueensIndividual import NqueensIndividual
from BinPackingIndividual import BinPackingIndividual
# import StringIndividual
# import NqueensIndividual
# import BinPackingIndividual
import time
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import CrossoverOperator
import ParentOperator
from Data import Data
MUTATION_INDIVIDUALS = 10
ELITE_PERCENTAGE = 0.80


class Population:
    data: Data
    population: list
    fitnesses: list
    best_fitness: float

    def __init__(self):
        self.data = Data()
        self.population = []
        self.fitnesses = []
        self.best_individual = 0
        self.best_fitness = 0
        self.max_weight = 0
        self.objects = []
        if self.data.problem == 2:
            self.read_file_bin_packing()

        for index in range(self.data.pop_size):
            if self.data.problem == 0:
                individual = StringIndividual(self.data)
            elif self.data.problem == 1:
                individual = NqueensIndividual(self.data)
            elif self.data.problem == 2:
                individual = BinPackingIndividual(self.data, self.objects.copy(), self.max_weight)
                self.data.num_genes = math.ceil(sum(self.objects) / self.max_weight)

            self.population.append(individual)

        for individual in self.population:
            self.fitnesses.append(individual.score)

    def genetic_algorithm(self):
        crossover_op = CrossoverOperator.CrossoverOperator()
        parent_op = ParentOperator.ParentOperator()

        for generation in range(self.data.max_generations):
            mutation_individuals = MUTATION_INDIVIDUALS

            old_average, old_sd = self.average_fitness(self.fitnesses)
            for index, individual in enumerate(self.population):
                self.fitnesses[index] = individual.score

            new_average, new_sd = self.average_fitness(self.fitnesses)
            var = new_sd ** 2

            gen_time = time.time()  # information
            print("=========================================")
            print(f"Average for this gen is {new_average}")
            print(f"Selection Pressure for this gen is {var}")
            # self.show_histogram(self.fitnesses)

            # Select the best individuals for reproduction
            elite_size = int(self.data.pop_size * ELITE_PERCENTAGE)  # exploitation
            elite_indices = sorted(range(self.data.pop_size), key=lambda i: self.fitnesses[i], reverse=True)[:elite_size]
            elites = [self.population[i] for i in elite_indices]

            # Generate new individuals by applying crossover and mutation operators
            offspring = []
            while len(offspring) < self.data.pop_size - elite_size:
                parents = parent_op.parent_selection_function(self.data.parent_selection, self.population, elites)
                parent1 = parents[0]
                parent2 = parents[1]

                if self.data.problem == 0:
                    child = StringIndividual(self.data)
                elif self.data.problem == 1:
                    child = NqueensIndividual(self.data)
                elif self.data.problem == 2:
                    temp_objects = self.objects.copy()
                    child = BinPackingIndividual(self.data, temp_objects, self.max_weight)

                child_gen = crossover_op.crossover_operator(self.data.cross_operator, parent1, parent2, self.data.num_genes, self.data)  # exploration
                child.gen = child_gen
                child.gen_len = len(child_gen)
                child.update_score(self.data)

                if new_average == old_average and mutation_individuals > 0:
                    child.mutation(self.data)
                    child.update_score(self.data)
                    mutation_individuals -= 1

                offspring.append(child)

            self.population = elites + offspring

            # Update the age of each individual, if reached max_age - remove from population
            for individual in self.population:
                individual.age += 1
                individual.update_score(self.data)
                if individual.age == self.data.max_age:
                    self.population.remove(individual)

            # Update the size of the   population MAYBE DELETE IT
            # self.data.pop_size = len(self.population)

            #Genetic Diversification
            distance = 0
            for individual in self.population:
                distance += individual.genetic_diversification_distance(self.population)

            special = self.population[0].genetic_diversification_special(self.population)

            print("The genetic diversification distance for this gen is:", distance)
            print("The genetic diversification special for this gen is:", special)
            print(f"The absolute time for this gen is {time.time() - gen_time} sec")
            print(f"The ticks time for this gen is {int(time.perf_counter())}")

        # Find the individual with the highest fitness
        self.best_individual = self.population[0]
        for individual in self.population:
            individual.update_score(self.data)
            if self.best_individual.score < individual.score:
                self.best_individual = individual

        self.best_fitness = self.best_individual.score

        return

    def average_fitness(self, fitness: list):  # information
        if not fitness:
            return 0
        average = sum(fitness) / len(fitness)
        variance = sum([((x - average) ** 2) for x in fitness]) / len(fitness) - 1
        sd = variance ** 0.5
        return average, sd

    def show_histogram(self, array):
        np_array = np.array(array)
        plt.hist(np_array)
        plt.show()
        return

    def read_file_bin_packing(self):
        with open("binpack1.txt") as f:
            f.readline()
            f.readline()
            list_info = f.readline().split()
            print(list_info)
            self.max_weight = int(list_info[0])
            num_items = int(list_info[1])
            self.best_fitness = int(list_info[2])

            for i in range(num_items):
                self.objects.append(int(f.readline()))




