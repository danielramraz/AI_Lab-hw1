# ----------- File For Genetic Algorithm -----------
import Population
import PopulationLab2
# ----------- Python Package -----------
import time
import threading
# ----------- Consts Name  ----------
NUM_ISLANDS = 2

single_test_setting_vector = [0, 13, 0, 1, 3, 3, 2, 1, 0]

multi_tests_setting_vectors = [[0, 13, 0, 1, 3, 3, 2, 1, 0], 
                               [0, 13, 1, 1, 3, 3, 2, 1, 0]]


class FlowManager:
    
    population: PopulationLab2
    islands: list
    results: list

    def __init__(self):
        self.total_time = time.time()
        self.results = []
        return

    def run_single_population_solution(self):
        # ----------- single run by user -----------
        # self.population = PopulationLab2.PopulationLab2()

        # ----------- test Program single thread -----------
        self.population = PopulationLab2.PopulationLab2(single_test_setting_vector)
        
        self.results.append(self.population.best_individual)
        return
    
    def run_multi_thread_population_solution(self):
        # Initialize the populations for each island
        for i in range(NUM_ISLANDS):
            # Initialize the population for the current island
            self.islands.append(PopulationLab2.PopulationLab2(multi_tests_setting_vectors[i]))
        
        # Create and start threads for each island
        threads = []
        for i in range(NUM_ISLANDS):
            thread = threading.Thread(target = self.islands[i].genetic_algorithm, 
                                      args=())
            threads.append(thread)
        
        for thread in threads:
            thread.start()
            print("thread stated =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        for index in self.islands: 
            self.results.append(self.islands[index].best_individual)

        return
    
    def show_results(self):
        print("==============Final Result==================")
        self.print_time()
        # bad_bins = 0
        # self.population.best_individual.gen = list(filter(None, self.population.best_individual.gen))
        # for item in self.population.best_individual.gen:
        #     if sum(item) > self.population.max_weight:
        #         bad_bins += 1
        
        for index in self.results:
            print(f"Best individual {index}:", self.results[index].gen)
            print(f"Best fitness {index}:", self.results[index].score)
        
        # print("BAD bins:", bad_bins)
        # print("num bins:", len(self.population.best_individual.gen))

    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")