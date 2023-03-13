import random
import Individual


class ParentOperator:
    def __init__(self):
        self.RWS = 0
        self.SUS = 1
        self.TOURNAMENT_RANKING = 2

    def parent_selection_function(self, parent_selection_input: int, population: list,):
        if parent_selection_input == self.RWS:
            self.rws(population)
        elif parent_selection_input == self.SUS:
            self.sus(population)
        elif parent_selection_input == self.TOURNAMENT_RANKING:
            self.tournament_ranking()

    def rws(self, population: list) -> Individual.Individual:
        sum_score = self.score_sum(population)
        weight_arr = []
        for individual in population:
            weight_arr.append(individual.score[1]/sum_score)

        print(f"weights array {weight_arr}")
        # print(f"choise {random.choices(population, weights = weight_arr, k = 1)}")
        return random.choices(population, weights = weight_arr, k = 1)

    def sus(self, population: list):
        return 6

    def tournament_ranking(self):
        return 7

    def score_sum(self, population):
        sum_score = 0
        for individual in population:
            sum_score += individual.score[1]
        print(f"sum score {sum_score}")
        return sum_score
