from ParentOperator import ParentOperator


class Data:
    def __init__(self):
        problem = int(input("Select a problem:\nString = 0\nN-Queens = 1\nBinPacking = 2\n"))
        crossover_operator = int(input("Enter the number of crossover operator:\nNone = 0 \nSingel = 1\nTwo = 2\nUniform = 3\n"))
        parent_selection = int(input("Enter the parent selection oprator:\nRWS = 0 \nSUS = 1\nTOURNAMENT RANKING = 2\nPMX = 3\nCX = 4\n"))
        mutation_selection = int(input("Enter them mutation:\nNone = 0 \nString mutation= 1\n= 2\nPMX = 3\nCX = 4\n")) #לעדכן לפי דניאל
        age_factor = int(input("Enter the age factor:\n"))
        fitness_function = int(input("Enter the fitness function:\noriginal = 0 \nbulls eye = 1\n"))

        self.problem = problem
        self.fitness_function = fitness_function
        self.mutation = mutation_selection
        self.cross_operator = crossover_operator
        self.parent_selection = parent_selection
        self.age_factor = age_factor
        self.pop_size = 100
        self.num_genes = 13
        self.max_generations = 100
        self.max_age = 10
