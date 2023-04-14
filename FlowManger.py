# ----------- File For Genetic Algorithm -----------
import Population
import PopulationLab2
# ----------- Python Package -----------
import time
import threading
# ----------- Consts Name  ----------
NUM_ISLANDS = 2


class FlowManger:
    population: PopulationLab2

    def __init__(self, current_time: time):
        self.total_time = current_time

        # ----------- Program without threads -----------
        # self.population = PopulationLab2.PopulationLab2()

        # ----------- Program with the island model -----------
        # Initialize the populations for each island
        populations = []
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