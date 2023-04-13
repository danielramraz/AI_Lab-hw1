# ----------- File For Genetic Algorithm -----------
import Population
import PopulationLab2
# ----------- Python Package -----------
import time
from threading import Thread

single_test_setting_vector = [0, 13, 0, 1, 
                              3, 3, 2, 1, 0]

multi_tests_setting_vectors = []


class FlowManger:
    population: PopulationLab2

    def __init__(self, current_time: time):
        
        # ----------- single run by user -----------
        # self.total_time = current_time
        # self.population = PopulationLab2.PopulationLab2()

        # ----------- test Program single thread -----------
        self.total_time = current_time
        self.population = PopulationLab2.PopulationLab2(single_test_setting_vector)

        # ----------- Program with the island model -----------
        # self.threads = []
        # for thr in range(2):
        #     thread = Thread(target=PopulationLab2.PopulationLab2(),
        #                     args=[])
        #     thread.start()
        #
        # for thread in self.threads:
        #     thread.join()

        return

    def show_result(self):
        print("==============Final Result==================")
        self.print_time()
        # bad_bins = 0
        # self.population.best_individual.gen = list(filter(None, self.population.best_individual.gen))
        # for item in self.population.best_individual.gen:
        #     if sum(item) > self.population.max_weight:
        #         bad_bins += 1

        print("Best individual:", self.population.best_individual.gen)
        print("Best fitness:", self.population.best_individual.score)
        # print("BAD bins:", bad_bins)
        # print("num bins:", len(self.population.best_individual.gen))

    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")