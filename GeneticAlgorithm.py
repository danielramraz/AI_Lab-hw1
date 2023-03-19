import numpy as np
import time
import matplotlib.pyplot as plt
import random
import CrossoverOperator
import ParentOperator
from Individual import Individual
from Data import Data

MUTATION_INDIVIDUALS = 1
ELITE_PERCENTAGE = 0.1
# char range 32, 126

class GeneticAlgorithm:
    # def genetic_algorithm(self, data: Data, elite_parameter, mutation_func
#                           init_parameter, cross_func, parent_func):           -> later
    def genetic_algorithm(self, data: Data):
        # Initialize the population with random individuals
        n = data.num_genes
        population = []
        fitnesses = [(0, 0)]
        crossover_op = CrossoverOperator.CrossoverOperator()
        parent_op = ParentOperator.ParentOperator()

        for i in range(data.pop_size):
            # individual_gen = [random.randint(1, n) for j in range(data.num_genes)]
            
            individual_gen = self.create_n_queens_gen(n)
            
            # print(f" new ind is {individual_gen} and the len {len(individual_gen)}")
            individual = Individual(individual_gen)
            population.append(individual)

        # Evolve the population for a fixed number of generations
        for generation in range(data.max_generations):

            mutation_individuals = MUTATION_INDIVIDUALS
            old_average = self.average_fitness(fitnesses[0])
            fitnesses = [self.queens_fitness(individual) for individual in population]  # exploitation
            new_average = self.average_fitness(fitnesses[0])

            genTime = time.time()  # information
            print("=========================================")
            print(f"the start time for this gen is {time.asctime(time.gmtime(genTime))}")
            print(f"average for this gen is {new_average}")

            #self.show_histogram(fitnesses)

            # Select the best individuals for reproduction
            elite_size = int(data.pop_size * ELITE_PERCENTAGE)  # exploitation
            elite_indices = sorted(range(data.pop_size), key=lambda i: fitnesses[i], reverse=True)[:elite_size]
            elites = [population[i] for i in elite_indices]

            # Generate new individuals by applying crossover and mutation operators
            offspring = []
            next_generation = data.pop_size - elite_size
            while len(offspring) < data.pop_size - elite_size:
                parent1 = random.choice(elites)
                parent2 = random.choice(elites)
                # parent1 = parent_op.parent_selection_function(data.parent_selection, population, next_generation)
                # parent2 = parent_op.parent_selection_function(data.parent_selection, population, next_generation)
                
                # print(f"parent 1 = {type(parent1)}, parent 2 = {type(parent2)}")

                child = crossover_op.crossover_operator(data.cross_operator, parent1, parent2, data.num_genes)  # exploration
                offspring.append(child)

                if new_average == old_average and mutation_individuals > 0:
                    child = self.mutation(child)
                    # child = self.invertion_shuffle(child)
                    # child = self.just_shuffle(child)

                    mutation_individuals -= 1

            population = elites + offspring

            print(f"the absolute time for this gen is {time.time() - genTime} sec")
            print(f"the ticks time for this gen is {int(time.perf_counter())}")

        # Find the individual with the highest fitness
        best_individual = max(population, key=lambda individual: self.queens_fitness(individual))  # exploitation
        best_fitness = self.queens_fitness(best_individual)

        return best_individual, best_fitness

    def queens_fitness(self, individual: Individual):  # explotation
        score = 100
        cross_counter = 0
        for i in range(individual.gen_len):
            if individual.gen.count(i+1) != 1:
                score -= 10
                # print("same row / no row penalty")

            for j in range(individual.gen_len):
                if i!=j and abs(i-j) == abs(individual.gen[i] - individual.gen[j]):
                    score -= 1
                    # print("cross penalty")
                    # cross_counter += 1
                            
        individual.score = (score, cross_counter)
        return score, cross_counter

    def create_n_queens_gen(self, n):
        gen = random.sample(range(1,n+1), n )
        print(f"the new gen is {gen}")
        return gen
    
    def fitness(self, individual: Individual):  # explotation
        target = list("Hello, world!")
        score = 0
        for i in range(individual.gen_len):
            # print(f"individual gen len {individual.gen_len}")
            if individual.gen[i] == target[i]:
                score += 1

        bullsEyeScore = self.bulls_eye(individual, target, score)  # add rienforcement to fitness func
        # bullsEyeScore = 0
        # score = 0
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
        # print("mutation used")
        num_genes = individual.gen_len
        rand_gen = random.randint(0, num_genes - 1)
        # individual.gen[rand_gen] = chr(random.randint(32, 126))
        individual.gen[rand_gen] = random.randint(1, 8)
        return individual
    
    def invertion_shuffle(self, individual: Individual, start = 0, end = 0, replace = 0):
        start = random.randint(0, individual.gen_len) 
        end = random.randint(start, individual.gen_len) 
        replace = random.randint(0, individual.gen_len - (end - start)) 
        local_gen = individual.gen
        print(f"the randoms are start = {start}, end = {end}, relace = {replace}")
        print(f"the local_gen is = {local_gen}")

        if start == end:
            return individual
        
        sub_gen = local_gen[start:end]
        print(f"the sub gen is = {sub_gen}")

        for i in range(len(sub_gen)):
            local_gen.pop(start)

        print(f"the local_gen is = {local_gen}")

        random.shuffle(sub_gen)
        print(f"the shuffled sub gen is = {sub_gen}")
 
        local_gen = local_gen[:replace] + sub_gen + local_gen[replace:]

        individual.gen = local_gen
        print(f"the final gen is = {individual.gen}")
        return individual

    def just_shuffle(self, individual: Individual):
        print(f"the orig gen is {individual.gen}")
        random.shuffle(individual.gen)   
        print(f"and the shuffled one is {individual.gen}")         
        return individual
