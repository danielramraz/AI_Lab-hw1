import random


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

    def rws(self, population: list):
        # for individual in population:
        #     fitness = individual
        return 5

    def sus(self, population: list):
        return 6

    def tournament_ranking(self):
        return 7

