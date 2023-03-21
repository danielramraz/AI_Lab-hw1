# from Data import Data
# import GeneticAlgorithm as GeneticAlgorithm
import time
import Population


class FlowManger:
    population: Population

    def __init__(self, current_time: time):
        self.total_time = current_time
        self.population = Population.Population()
        # crossover_operator_input = int(input("Enter the number of crossover operator:\nNone = 0 \nSingel = 1\nTwo = 2\nUniform = 3\nPMX = 4\nCX =5\n"))
        # parent_selection_input = int(input("Enter the parent selection oprator:\nNone = 0 \nRWS = 1 \nSUS = 2\nTOURNAMENT RANKING = 3\n"))
        # self.data = Data(pop_size=100,
        #                  num_genes=8,
        #                  max_generations=100,
        #                  cross_operator=crossover_operator_input,
        #                  parent_selection=parent_selection_input,
        #                  age_factor=0.5,
        #                  max_age=10)
        return

    # def genetic_algorithm(self):
    #     genetic = GeneticAlgorithm.GeneticAlgorithm()
    #     return genetic.genetic_algorithm(self.data)

    def show_result(self):
        print("==============Final Result==================")
        self.print_time()
        # if type(self.population.best_individual.gen[0]) != int:
        #     print("Best individual:", ''.join(self.population.best_individual.gen))
        # else:
        print("Best individual:", self.population.best_individual.gen)
        print("num bins:", len(self.population.best_individual.gen))
        print("Best fitness:", self.population.best_fitness)

    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")

