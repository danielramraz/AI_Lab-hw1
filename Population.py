from Data import Data
import StringIndividual
import NqueensIndividual
import BinPackingIndividual

class Population:

    data: Data
    population: list

    def __init__(self):
        self.data = Data()
        problem = int(input("Select a problem:\nString = 0\nN-Queens = 1\nBinPacking = 2\n"))
        for index in self.data.pop_size:
            if self.data.problem == 0:
                individual = StringIndividual(self.data)
            if self.data.problem == 1:
                individual = NqueensIndividual(self.data)
            if self.data.problem == 2:
                individual = BinPackingIndividual(self.data)
        self.population = []

