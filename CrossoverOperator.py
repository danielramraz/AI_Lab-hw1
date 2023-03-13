import random


class CrossoverOperator:

    def __init__(self):
        self.NONE = 0
        self.SINGLE = 1
        self.TWO = 2
        self.UNIFORM = 3

    def crossover_operator(self, operator, parent1, parent2, num_genes: int):  # exploration
        # print(f"operator {operator} of type {type(operator)}")
        if operator == self.NONE:
            child = random.choice([parent1, parent2])

        if operator == self.SINGLE:
            rand_a = random.randint(0, num_genes)
            # print(f"random {rand_a}")
            child = [parent1[i] if i < rand_a else parent2[i] for i in range(num_genes)]

        elif operator == self.TWO:
            rand_a = random.randint(0, num_genes - 1)
            rand_b = random.randint(rand_a, num_genes)
            # print(f"random {rand_a} , {rand_b}")
            child = [parent1[i] if i < rand_a or i > rand_b else parent2[i] for i in range(num_genes)]

        elif operator == self.UNIFORM:
            child = [parent1[i] if random.choice([0, 1]) else parent2[i] for i in range(num_genes)]

        return child
