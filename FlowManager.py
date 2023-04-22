# ----------- File For Genetic Algorithm -----------
from Individual import Individual
from Migration import Migration
import Population
import Population
# ----------- Python Package -----------
import time
import threading
# ----------- Consts Name  ----------
NUM_ISLANDS = 2

single_test_setting_vector = [2, 0, 0, 0,
                              6, 1, 2,
                              0, 0, 0]
# setting_vector => 
# problem[0] num_genes[1] fitness_function[2] mutation_selection[3] 
# cross_operator[4] mutation_control_selection[5] parent_selection[6] 
# niche_algorithm[7] age_factor[8] viability_fuc_num[9]
multi_tests_setting_vectors = [[3, 2, 0, 4, 7, 1, 2, 0, 0, 1], 
                               [3, 2, 0, 4, 7, 1, 2, 0, 0, 2]]


class FlowManager:
    
    population: Population
    islands: list
    results: list 
    migration: Migration

    def __init__(self):
        self.total_time = time.time()
        self.results = []
        self.islands = []
        self.migration = Migration(NUM_ISLANDS)
        return

    def user_run(self):
        self.runing_config = int(input("singel run with user inputs = 0\nislands methode (multi theard) run with cartesian problem = 1\n"))
        
        if self.runing_config == 0:
            self.run_single_population_solution()
        elif self.runing_config == 1:
            self.run_multi_thread_population_solution()
        
        self.show_results()
        self.run_again()
        return
    
    def run_single_population_solution(self):
        # ----------- single run by user -----------
        self.population = Population.Population()

        # ----------- test Program single thread -----------
        # self.population = Population.Population(single_test_setting_vector)
        
        self.population.genetic_algorithm()
        self.results.append(self.population.best_individual)
        return
    
    def run_multi_thread_population_solution(self):
        # Initialize the populations for each island
        for i in range(NUM_ISLANDS):
            # Initialize the population for the current island
            self.islands.append(Population.Population(multi_tests_setting_vectors[i]))
        
        # Create and start threads for each island
        threads = []
        for i in range(NUM_ISLANDS):
            thread = threading.Thread(target = self.islands[i].genetic_algorithm, 
                                      args=(self.migration, i))
            threads.append(thread)
        
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        for index in range(len(self.islands)): 
            self.results.append(self.islands[index].best_individual)

        return
    
    def show_results(self):
        print("==============Final Result==================")
        self.print_time()
        
        for index in range(len(self.results)):
            print(f"Best individual {index}:", self.results[index].gen)
            print(f"Best fitness {index}:", self.results[index].score)

        if (self.runing_config == 0 and self.population.data.problem == 2):
            self.extra_print_solution_bin_packing()
        return
        
    def extra_print_solution_bin_packing(self):
        bad_bins = 0
        self.population.best_individual.gen = list(filter(None, self.population.best_individual.gen))
        for item in self.population.best_individual.gen:
            if sum(item) > self.population.max_weight:
                bad_bins += 1
        print("BAD bins:", bad_bins)
        print("num bins:", len(self.population.best_individual.gen))

        return
    
    def print_time(self):
        print(f"the total time for this algo is {time.time() - self.total_time} sec")
        print(f"the ticks time for this algo is {int(time.perf_counter())}")

    def run_again(self):
        run_again = int(input("Do you want to run again? yes = 1, n = 0\n"))
        
        if run_again == 1:
            self.user_run()
        
        return
