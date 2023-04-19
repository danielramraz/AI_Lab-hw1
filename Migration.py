# ----------- Python Package -----------
import random
# ----------- Consts Name  -----------
NONE_FUNCTION = 0
FUNCTION_1 = 1
FUNCTION_2 = 2

class Migration:
    immigrant_per_island =[]

    def __init__(self, num_island):
        for i in range(num_island):
            self.immigrant_per_island.append([])

    # Selection of the immigrant according to size-2 tournament method
    def immigrant_selection(self,
                            population: list, 
                            number_of_competitors, 
                            population_index):
        
        number_of_immigrants = 1
        k_fitness = []
        k_individual = random.choices(population, k=number_of_competitors)
        for individual in k_individual:
            k_fitness.append(individual.score)

        k_sorted = sorted(range(number_of_immigrants), key=lambda i: k_fitness[i], reverse=True)[:number_of_immigrants]
        immigrants = [k_individual[i] for i in k_sorted]

        self.immigrant_per_island[population_index] = immigrants
        return

    # Checking if it is legal to transfer the immigrant to the target population by viability function
    def insert_imigranent_to_pop(self, 
                                 viability_fuc_num, 
                                 target_population, 
                                 population_index):
        
        citizen = random.choices(target_population, k=1)[0]

        if viability_fuc_num == FUNCTION_1:
            for immigrant in self.immigrant_per_island[(population_index+1) % 2]:
                if citizen.score ** 2 + immigrant.score** 2 <= 3:
                        target_population.append(immigrant)
                        # print("migration F1 used")

        elif viability_fuc_num == FUNCTION_2:
            for immigrant in self.immigrant_per_island[(population_index+1) % 2]:
                if (citizen.score-5) ** 2 + (immigrant.score-5) ** 2 <= 2:
                    target_population.append(immigrant)
                    # print("migration F2 used")
        
        elif viability_fuc_num == NONE_FUNCTION:
            for immigrant in self.immigrant_per_island[(population_index+1) % 2]:
                target_population.append(immigrant)

        return target_population




