import random
from Individual import Individual


class CrossoverOperator:

    def __init__(self):
        self.NONE = 0
        self.SINGLE = 1
        self.TWO = 2
        self.UNIFORM = 3
        self.PMX = 4
        self.CX = 5

    def crossover_operator(self, operator, parent1: Individual, parent2: Individual, num_genes: int):  # exploration
        # print(f"operator {operator} of type {type(operator)}")
        if operator == self.NONE:
            child_gen = random.choice([parent1.gen, parent2.gen])

        if operator == self.SINGLE:
            rand_a = random.randint(0, num_genes)
            child_gen = [parent1.gen[i] if i < rand_a else parent2.gen[i] for i in range(num_genes)]

        elif operator == self.TWO:
            rand_a = random.randint(0, num_genes - 1)
            rand_b = random.randint(rand_a, num_genes)
            child_gen = [parent1.gen[i] if i < rand_a or i > rand_b else parent2.gen[i] for i in range(num_genes)]

        elif operator == self.UNIFORM:
            child_gen = [parent1.gen[i] if random.choice([0, 1]) else parent2.gen[i] for i in range(num_genes)]

        elif operator == self.PMX:
            child_gen = self.pmx_shuffle(parent1, parent2, num_genes)

        elif operator == self.CX:
            child_gen = self.cx_shuffle(parent1, parent2, num_genes)

        child = Individual(child_gen)
        return child

    def cx_shuffle(self, parent1: Individual, parent2: Individual, num_genes: int):
        p1 = parent1.gen
        p2 = parent2.gen

        gen_groups = []


        # for i in range(num_genes):
        #     gen_groups.append([])
        #     for j in range(num_genes): 
        #         gen_groups[i].append(j)

        return 
    
    def pmx_shuffle(self, parent1: Individual, parent2: Individual, num_genes: int):
        p1 = parent1.gen
        p2 = parent2.gen
        # print(f"parents befor pmx shuffle are:\n{p1}\n{p2}")
        rand_a = random.randint(0, num_genes/2)

        for i in range(rand_a):
            temp_p1 = p1[i]                     #set the indexes
            temp_p2 = p2[i]
            try:
                temp_index1 = p1.index(p2[i])
                temp_index2 = p2.index(p1[i])

                p1[i] = p1[temp_index1]             #switch the values
                p1[temp_index1] = temp_p1

                p2[i] = p2[temp_index2]
                p2[temp_index2] = temp_p2
                
            except:
                print("there are missing index in one of the genes")

        # print(f"parents after pmx shuffle are:\n{p1}\n{p2}")

        rand_a = random.randint(0, num_genes)
        child_gen = [p1[i] if i < rand_a else p2[i] for i in range(num_genes)]

        return child_gen
