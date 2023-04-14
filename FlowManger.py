# ----------- File For Genetic Algorithm -----------
import Population
import PopulationLab2
# ----------- Python Package -----------
import time
import threading
# ----------- Consts Name  ----------
NUM_ISLANDS = 2

single_test_setting_vector = [0, 13, 0, 1, 
                              3, 3, 2, 1, 0]

multi_tests_setting_vectors = []


class FlowManger:
    population: PopulationLab2

    def __init__(self, current_time: time):
        self.total_time = current_time
        
        # ----------- single run by user -----------
        # self.population = PopulationLab2.PopulationLab2()

        # ----------- test Program single thread -----------
        # self.population = PopulationLab2.PopulationLab2(single_test_setting_vector)

        # ----------- Program with the island model -----------

        # Initialize the populations for each island
        self.populations = []
        for i in range(NUM_ISLANDS):
            population = []  # Initialize the population for the current island
            self.populations.append(PopulationLab2.PopulationLab2())
            # Create and start threads for each island

        threads = []
        for i in range(NUM_ISLANDS):
            thread = threading.Thread(target=populations[i].genetic_algorithm(), args=(i, populations[i]))
            thread.start()
            threads.append(thread)

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

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