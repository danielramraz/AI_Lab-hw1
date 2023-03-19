from Data import Data
import time
import GeneticAlgorithm as GeneticAlgorithm


class FlowManger:
    data: Data

    def __init__(self, current_time: time):
        self.total_time = current_time
        crossover_operator_input = int(input("Enter the number of crossover operator:\nNone = 0 \nSingel = 1\nTwo = 2\nUniform = 3\n"))
        parent_selection_input = int(input("Enter the parent selection oprator:\nRWS = 0 \nSUS = 1\nTOURNAMENT RANKING = 2\n"))
        self.data = Data(pop_size=100,
                         num_genes=13,
                         max_generations=100,
                         cross_operator=crossover_operator_input,
                         parent_selection=parent_selection_input,
                         age_factor=0.5,
                         max_age=10)
        return

    def genetic_algorithm(self):
        genetic = GeneticAlgorithm.GeneticAlgorithm()
        return genetic.genetic_algorithm(self.data)

    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")

        # def genetic_algorithm():
        # # Initialize the population with random individuals
        # population = []
        # fitnesses = [(0, 0)]
        # for i in range(pop_size):
        #     individual = [chr(random.randint(32, 126)) for j in range(num_genes)]
        #     population.append(individual)
        #
        # # Evolve the population for a fixed number of generations
        # for generation in range(max_generations):
        #     mutation_individuals = MUTATION_INDIVIDUALS
        #     old_average = averege_fitness(fitnesses[0])
        #     fitnesses = [fitness_func(individual) for individual in population]  # exploitation
        #     new_average = averege_fitness(fitnesses[0])
        #
        #     genTime = time.time()  # information
        #     print("=========================================")
        #     print(f"the start time for this gen is {time.asctime(time.gmtime(genTime))}")
        #     print(f"--------averege for this gen is {new_average}")
        #
        #     show_histogram(fitnesses)
        #
        #     # Select the best individuals for reproduction
        #     elite_size = int(pop_size * 0.1)  # exploitation
        #     elite_indices = sorted(range(pop_size), key=lambda i: fitnesses[i], reverse=True)[:elite_size]
        #     elites = [population[i] for i in elite_indices]
        #
        #     # Generate new individuals by applying crossover and mutation operators
        #     offspring = []
        #     while len(offspring) < pop_size - elite_size:
        #
        #         parent1 = random.choice(elites)
        #         parent2 = random.choice(elites)
        #         child = crossover_operator(cross_operator, parent1, parent2, num_genes)  # exploration
        #         offspring.append(child)
        #
        #         if (new_average == old_average and mutation_individuals > 0):
        #             child = mutation(child)
        #             mutation_individuals -= 1
        #
        #     population = elites + offspring
        #
        #     print(f"the absolute time for this gen is {time.time() - genTime} sec")
        #     # print(f"the ticks time for this gen is {int(time.perf_counter())}")
        #
        # # Find the individual with the highest fitness
        # best_individual = max(population, key=lambda individual: fitness_func(individual))  # exploitation
        # best_fitness = fitness_func(best_individual)
        #
        # return best_individual, best_fitness




