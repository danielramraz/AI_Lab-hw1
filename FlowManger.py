from Data import Data
import time
import GeneticAlgorithm as GeneticAlgorithm


class FlowManger:
    data: Data

    def __init__(self, current_time: time):
        self.total_time = current_time
        crossover_operator_input = int(input("Enter the number of crossover operator:\nNone = 0 \nSingel = 1\nTwo = 2\nUniform = 3\nPMX = 4\nCX =5\n"))
        parent_selection_input = int(input("Enter the parent selection oprator:\nRWS = 0 \nSUS = 1\nTOURNAMENT RANKING = 2\n"))
        self.data = Data(pop_size = 100,
                         num_genes = 8,
                         max_generations = 100,
                         cross_operator = crossover_operator_input,
                         parent_selection = parent_selection_input)
        return

    def genetic_algorithm(self):
        genetic = GeneticAlgorithm.GeneticAlgorithm()
        return genetic.genetic_algorithm(self.data)

    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")

