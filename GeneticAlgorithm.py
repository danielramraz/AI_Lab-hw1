import numpy as np
import time
import matplotlib.pyplot as plt
import random
import CrossoverOperator
import ParentOperator
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
            individual = [chr(random.randint(32, 126)) for j in range(data.num_genes)]
            population.append(individual)

        # Evolve the population for a fixed number of generations
        for generation in range(data.max_generations):

            mutation_individuals = MUTATION_INDIVIDUALS
            old_average = self.average_fitness(fitnesses[0])
            fitnesses = [self.fitness(individual) for individual in population]  # exploitation
            new_average = self.average_fitness(fitnesses[0])

            genTime = time.time()  # information
            print("=========================================")
            print(f"the start time for this gen is {time.asctime(time.gmtime(genTime))}")
            print(f"average for this gen is {new_average}")

            self.show_histogram(fitnesses)

            # Select the best individuals for reproduction
            elite_size = int(data.pop_size * 0.1)  # exploitation
            elite_indices = sorted(range(data.pop_size), key=lambda i: fitnesses[i], reverse=True)[:elite_size]
            elites = [population[i] for i in elite_indices]

            # Generate new individuals by applying crossover and mutation operators
            offspring = []
            while len(offspring) < data.pop_size - elite_size:
                parent1 = random.choice(elites)
                parent2 = random.choice(elites)
                # parent1 = parent_op.parent_selection_function(data.parent_selection, population)
                # parent2 = parent_op.parent_selection_function(data.parent_selection, population)
                child = crossover_op.crossover_operator(data.cross_operator, parent1, parent2, data.num_genes)  # exploration
                offspring.append(child)

                if new_average == old_average and mutation_individuals > 0:
                    child = self.mutation(child)
                    mutation_individuals -= 1

            population = elites + offspring

            print(f"the absolute time for this gen is {time.time() - genTime} sec")
            print(f"the ticks time for this gen is {int(time.perf_counter())}")

        # Find the individual with the highest fitness
        best_individual = max(population, key=lambda individual: self.fitness(individual))  # exploitation
        best_fitness = self.fitness(best_individual)

        return best_individual, best_fitness

    def fitness(self, individual):  # explotation
        target = list("Hello, world!")
        score = 0
        for i in range(len(individual)):
            if individual[i] == target[i]:
                score += 1

        bullsEyeScore = self.bulls_eye(individual, target, score)  # add rienforcement to fitness func
        # bullsEyeScore = 0
        # score = 0

        return score, bullsEyeScore

    def bulls_eye(self, individual, target, score):  # exploitation
        for i in range(len(individual)):
            if individual[i] == target[i]:
                score += 10
            elif individual[i] in target:
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

    def mutation(self, individual):  # exploration
        num_genes = len(individual)
        rand_gen = random.randint(0, num_genes - 1)
        individual[rand_gen] = chr(random.randint(32, 126))
        return individual
