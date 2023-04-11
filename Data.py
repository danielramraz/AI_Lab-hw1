
class Data:
    def __init__(self):
        problem = 0 # int(input("Select a problem:\nString = 0\nN-Queens = 1\nBinPacking = 2\n"))
        self.num_genes = 13 # int(input("enter the size of the gen:\nFor String enter 13\nFor N-Queens enter 8\nFor BinPacking enter 0\n"))
        fitness_function = 0 # int(input("Enter the fitness function:\noriginal = 0 \nString bulls eye = 1\nBitwise bulls eye = 2\n"))
        mutation_selection = 1 # int(input("Enter them mutation:\nBinPacking None = 0 \nString mutation= 1\nN-Queens invertion shuffle = 2\nN-Queens Just shuffle = 3\n"))
        crossover_operator = 3 # int(input("Enter the number of crossover operator:\nNone = 0 \nSingel = 1\nTwo = 2\nUniform = 3\nN-Queens PMX = 4\nN-Queens CX = 5\nBIN_PACKING = 6\n"))
        self.mutation_control_selection = 3 # int(input("Enter mutation control method:\NONE = 0 \nConst mutation= 1\nDecrease linearly = 2\nNon Linear logistic decay = 3\n"))
        parent_selection = 2 # int(input("Enter the parent selection oprator:\nNone = 0 \nRWS = 1 \nSUS = 2\nTOURNAMENT RANKING = 3\n"))
        niche_algorithm = 1  # int(input("Enter the niche algorithm:\n (Share Fitness = 0) \nClustering = 1 \n"))
        age_factor = 0  # float(input("Enter the age factor:\n"))

        self.problem = problem
        self.fitness_function = fitness_function
        self.mutation = mutation_selection
        self.cross_operator = crossover_operator
        self.parent_selection = parent_selection
        self.niche_algorithm = niche_algorithm
        self.age_factor = age_factor
        self.pop_size = 100
        # self.num_genes = 8
        self.max_generations = 100
        self.max_age = 101