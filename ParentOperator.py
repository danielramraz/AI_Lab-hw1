import random
from Individual import Individual
import Population
import numpy as np

class ParentOperator:
    def __init__(self):
        self.NONE = 0
        self.RWS = 1
        self.SUS = 2
        self.TOURNAMENT_RANKING = 3

    def parent_selection_function(self, 
                                  parent_selection_input: int, 
                                  population: list, 
                                  elites: list):
        
        if parent_selection_input == self.NONE:
            return [random.choice(elites), random.choice(elites)]
        elif parent_selection_input == self.RWS:
            return self.rws(population)
        elif parent_selection_input == self.SUS:
            return self.sus(population)
        elif parent_selection_input == self.TOURNAMENT_RANKING:
            return self.tournament_ranking(population)
        
        return
    
    def rws(self, population: list):
        sum_score = self.score_sum(population)
        fitness = self.winsorize(population)
        weight_arr = []
        for index in range(len(fitness)):
            weight_arr.append(abs(fitness[index]/sum_score))

        return random.choices(population, weights=weight_arr, k=2)

    def sus(self, population: list):
        sum_score = self.score_sum(population)
        fitness = self.winsorize(population)

        for index, individual in enumerate(population):
            if index > 0:
                fitness[index] += fitness[index-1]

        parents = []
        number_of_parents = 2
        slice_size = int(sum_score/len(population))
        first_spine_pointer = int(random.uniform(0, slice_size))
        delta = sum_score / number_of_parents

        for i in range(number_of_parents):
            fit = first_spine_pointer + i * delta
            current, j = 0, 0
            while current < fit:
                current += population[j].score
                j += 1
            parents.append(population[j])

        return parents

    def tournament_ranking(self, population: list):

        number_of_competitors = 30
        number_of_parents = 2
        k_fitness = []

        k_individual = random.choices(population, k=number_of_competitors)
        for individual in k_individual:
            k_fitness.append(individual.score)

        k_sorted = sorted(range(number_of_competitors), key=lambda i: k_fitness[i], reverse=True)[:number_of_parents]
        parents = [k_individual[i] for i in k_sorted]

        return parents

    def score_sum(self, population: list):
        sum_score = 0
        for individual in population:
            sum_score += individual.score
        return sum_score

    def winsorize(self, population: list, percentile=5):
        fitneses = []
        for individual in population:
                fitneses.append(individual.score)

        lower_bound = np.percentile(fitneses, percentile)
        upper_bound = np.percentile(fitneses, 100 - percentile)
        fitneses = np.where(fitneses < lower_bound, lower_bound, fitneses)
        fitneses = np.where(fitneses > upper_bound, upper_bound, fitneses)
        mean = np.mean(fitneses)
        std = np.std(fitneses)
        try:
            fitneses = (fitneses - mean) / std
        except:
            fitneses = 0
            
        return fitneses


