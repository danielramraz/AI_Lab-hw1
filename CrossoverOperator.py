import random
from Individual import Individual


class CrossoverOperator:

    def __init__(self):
        self.NONE = 0
        self.SINGLE = 1
        self.TWO = 2
        self.UNIFORM = 3

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

        child = Individual(child_gen)
        return child
