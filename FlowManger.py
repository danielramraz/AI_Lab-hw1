# from Data import Data
# import GeneticAlgorithm as GeneticAlgorithm
import time
import Population


class FlowManger:
    population: Population

    def __init__(self, current_time: time):
        self.total_time = current_time
        self.population = Population.Population()
        return

    def show_result(self):
        print("==============Final Result==================")
        self.print_time()
        print("Best individual:", self.population.best_individual.gen)
        print("Best fitness:", self.population.best_individual.score)

    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")
