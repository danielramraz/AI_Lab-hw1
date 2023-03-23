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

        bad_bins = 0
        self.population.best_individual.gen = list(filter(None, self.population.best_individual.gen))

        for item in self.population.best_individual.gen:
            if sum(item) > self.population.max_weight:
                bad_bins += 1

        print("Best individual:", self.population.best_individual.gen)
        print("BAD bins:", bad_bins)
        print("num bins:", len(self.population.best_individual.gen))
        print("Best fitness:", self.population.best_individual.score)

    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")

    # def genetic_algorithm(self):
    #     genetic = GeneticAlgorithm.GeneticAlgorithm()
    #     return genetic.genetic_algorithm(self.data)

    # if type(self.population.best_individual.gen[0]) != int:
    #     print("Best individual:", ''.join(self.population.best_individual.gen))
    # else: