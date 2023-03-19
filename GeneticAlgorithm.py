import numpy as np
import time
import matplotlib.pyplot as plt
import random
import CrossoverOperator
import ParentOperator
import GeneticDiversification
from Individual import Individual
from Data import Data
MUTATION_INDIVIDUALS = 10

class GeneticAlgorithm:

    def genetic_algorithm(self, data: Data):
        # Initialize the population with random individuals
        population = []
        fitnesses = [(0, 0)]
        crossover_op = CrossoverOperator.CrossoverOperator()
        parent_op = ParentOperator.ParentOperator()

        for i in range(data.pop_size):
            individual_gen = [chr(random.randint(32, 126)) for j in range(data.num_genes)]
            # print(f" new ind is {individual_gen} and the len {len(individual_gen)}")
            individual = Individual(individual_gen)
            population.append(individual)

        # Evolve the population for a fixed number of generations
        for generation in range(data.max_generations):

            mutation_individuals = MUTATION_INDIVIDUALS

            old_average, old_sd = self.average_fitness(fitnesses[0])
            fitnesses = [self.fitness(individual, data) for individual in population]  # exploitation
            new_average, new_sd = self.average_fitness(fitnesses[0])
            var = new_sd**2

            genTime = time.time()  # information
            print("=========================================")
            # print(f"The start time for this gen is {time.asctime(time.gmtime(genTime))}")
            print(f"Average for this gen is {new_average}")
            print(f"Selection Pressure for this gen is {var}")

            #self.show_histogram(fitnesses)

            # Select the best individuals for reproduction
            elite_size = int(data.pop_size * 0.1)  # exploitation
            elite_indices = sorted(range(data.pop_size), key=lambda i: fitnesses[i], reverse=True)[:elite_size]
            elites = [population[i] for i in elite_indices]

            # Generate new individuals by applying crossover and mutation operators
            offspring = []
            while len(offspring) < data.pop_size - elite_size:
                # parent1 = random.choice(elites)
                # parent2 = random.choice(elites)
                parents = parent_op.parent_selection_function(data.parent_selection, population)
                parent1 = parents[0]
                parent2 = parents[1]

                child = crossover_op.crossover_operator(data.cross_operator, parent1, parent2, data.num_genes)  # exploration
                offspring.append(child)

                if new_average == old_average and mutation_individuals > 0:
                    child = self.mutation(child)
                    mutation_individuals -= 1

            population = elites + offspring

            # Update the age of each individual, if reached max_age - remove from population
            for individual in population:
                individual.age += 1
                if individual.age == data.max_age:
                    population.remove(individual)

            # Update the size of the   population
            data.pop_size = len(population)

            print(f"The absolute time for this gen is {time.time() - genTime} sec")
            print(f"The ticks time for this gen is {int(time.perf_counter())}")

        # Find the individual with the highest fitness
        best_individual = max(population, key=lambda individual: self.fitness(individual, data))  # exploitation
        best_fitness = self.fitness(best_individual, data)

        return best_individual, best_fitness

    # def generation_manufacturing(self, data: Data, population: list, crossover_op: CrossoverOperator, parent_op: ParentOperator, elite_size: int):
    #     next_generation = data.pop_size - elite_size
    #     return parent_op.parent_selection_function(data.parent_selection, population, next_generation)
    #
    #     while len(offspring) < data.pop_size - elite_size:
    #         # parent1 = random.choice(elites)
    #         # parent2 = random.choice(elites)
    #         parent1 = parent_op.parent_selection_function(data.parent_selection, population, next_generation)
    #         parent2 = parent_op.parent_selection_function(data.parent_selection, population, next_generation)
    #
    #         print(f"parent 1 = {type(parent1)}, parent 2 = {type(parent2)}")
    #
    #         child = crossover_op.crossover_operator(data.cross_operator, parent1, parent2,
    #                                                 data.num_genes)  # exploration
    #         offspring.append(child)
    #
    #         if new_average == old_average and mutation_individuals > 0:
    #             child = self.mutation(child)
    #             mutation_individuals -= 1

    def fitness(self, individual: Individual, data: Data):  # explotation
        target = list("Hello, world!")
        score = 0
        for i in range(individual.gen_len):
            # print(f"individual gen len {individual.gen_len}")
            if individual.gen[i] == target[i]:
                score += 1

        bullsEyeScore = self.bulls_eye(individual, target, score)
        score = data.age_factor*individual.age + (1 - data.age_factor)*score
        bullsEyeScore = data.age_factor*individual.age + (1 - data.age_factor)*bullsEyeScore

        individual.score = (score, bullsEyeScore)

        return score, bullsEyeScore

    def bulls_eye(self, individual: Individual, target, score):  # exploitation
        for i in range(individual.gen_len):
            if individual.gen[i] == target[i]:
                score += 10
            elif individual.gen[i] in target:
                score += 5
        return score

    def average_fitness(self, fitness):  # information
        if not fitness:
            return (0, 0)
        average = sum(fitness) / len(fitness)
        variance = sum([((x - average) ** 2) for x in fitness]) / len(fitness) - 1
        sd = variance ** 0.5
        return average, sd

    def show_histogram(self, array):
        np_array = np.array(array)
        plt.hist(np_array)
        plt.show()
        return

    def mutation(self, individual: Individual):  # exploration
        num_genes = individual.gen_len
        rand_gen = random.randint(0, num_genes - 1)
        individual.gen[rand_gen] = chr(random.randint(32, 126))
        return individual
