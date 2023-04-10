# ----------- File Form Lab -----------
from Individual import Individual
# ----------- Python Package -----------
import random
# ----------- Consts Name  -----------
NONE = 0
SINGLE = 1
TWO = 2
UNIFORM = 3
PMX = 4
CX = 5
BIN_PACKING = 6

# class CrossoverOperator:
#
#     def __init__(self):
#         self.NONE = 0
#         self.SINGLE = 1
#         self.TWO = 2
#         self.UNIFORM = 3
#         self.PMX = 4
#         self.CX = 5
#         self.BIN_PACKING = 6


def crossover_operator(operator, parent1: Individual, parent2: Individual, num_genes: int):

    if operator == NONE:
        child_gen = [parent1.gen[i] if random.random() < 0.5 else parent2.gen[i] for i in range(num_genes)]
#     def __init__(self):
#         self.NONE = 0
#         self.SINGLE = 1
#         self.TWO = 2
#         self.UNIFORM = 3
#         self.PMX = 4
#         self.CX = 5
#         self.BIN_PACKING = 6

#     def crossover_operator(self, operator, parent1: Individual, parent2: Individual, num_genes: int, data: Data,
#                            best_solution: int):  # exploration

#         if operator == self.NONE:
#             child_gen = [parent1.gen[i] if random.random() < 0.5 else parent2.gen[i] for i in range(num_genes)]

#         if operator == self.SINGLE:
#             rand_a = random.randint(0, num_genes)
#             child_gen = [parent1.gen[i] if i < rand_a else parent2.gen[i] for i in range(num_genes)]

#         elif operator == self.TWO:
#             rand_a = random.randint(0, num_genes - 1)
#             rand_b = random.randint(rand_a, num_genes)
#             child_gen = [parent1.gen[i] if i < rand_a or i > rand_b else parent2.gen[i] for i in range(num_genes)]

#         elif operator == self.UNIFORM:
#             child_gen = [parent1.gen[i] if random.choice([0, 1]) else parent2.gen[i] for i in range(num_genes)]

#         elif operator == self.PMX:
#             child_gen = self.pmx_shuffle(parent1, parent2, num_genes)

#         elif operator == self.CX:
#             child_gen = self.cx_shuffle(parent1, parent2, num_genes)

#         elif operator == self.BIN_PACKING:
#             child_gen = self.bin_packing_cross(parent1, parent2, num_genes)

#         return child_gen

#     def bin_packing_cross(self, parent1: Individual, parent2: Individual, num_genes: int):
#         child_gen = []
#         ran = random.random()
#         copy_objects = parent1.objects.copy()
#         size_gen = len(copy_objects)

#         # fill child with empty bins
#         for i in range(size_gen):
#             child_gen.append([])

#         parent1_part = int(len(copy_objects) * ran)
#         parent2_part = len(copy_objects) - parent1_part

#         for i in range(parent1_part):
#             object = random.sample(copy_objects, 1)[0]
#             for bin in range(len(parent1.gen)):
#                 if object in parent1.gen[bin]:
#                     while object + sum(child_gen[bin]) > parent1.max_weight:
#                         bin = random.randint(0, size_gen - 1)
#                     child_gen[bin].append(object)
#                     copy_objects.remove(object)
#                     break

#         for i in range(parent2_part):
#             object = random.sample(copy_objects, 1)[0]
#             for bin in range(len(parent2.gen)):
#                 if object in parent2.gen[bin]:
#                     while object + sum(child_gen[bin]) > parent2.max_weight:
#                         bin = random.randint(0, size_gen - 1)
#                     child_gen[bin].append(object)
#                     copy_objects.remove(object)
#                     break

#         return child_gen

#     def pmx_shuffle(self, parent1: Individual, parent2: Individual, num_genes: int):
#         p1 = parent1.gen
#         p2 = parent2.gen
#         rand_a = random.randint(0, num_genes / 2)

#         for i in range(rand_a):
#             temp_p1 = p1[i]  # set the indexes
#             temp_p2 = p2[i]
#             try:
#                 temp_index1 = p1.index(p2[i])
#                 temp_index2 = p2.index(p1[i])

#                 p1[i] = p1[temp_index1]  # switch the values
#                 p1[temp_index1] = temp_p1

#                 p2[i] = p2[temp_index2]
#                 p2[temp_index2] = temp_p2

#             except:
#                 pass
# >>>>>>> main

    if operator == SINGLE:
        rand_a = random.randint(0, num_genes)
        child_gen = [parent1.gen[i] if i < rand_a else parent2.gen[i] for i in range(num_genes)]

    elif operator == TWO:
        rand_a = random.randint(0, num_genes - 1)
        rand_b = random.randint(rand_a, num_genes)
        child_gen = [parent1.gen[i] if i < rand_a or i > rand_b else parent2.gen[i] for i in range(num_genes)]

    elif operator == UNIFORM:
        child_gen = [parent1.gen[i] if random.choice([0, 1]) else parent2.gen[i] for i in range(num_genes)]

    elif operator == PMX:
        child_gen = pmx_shuffle(parent1, parent2, num_genes)

    elif operator == CX:
        child_gen = cx_shuffle(parent1, parent2, num_genes)

    elif operator == BIN_PACKING:
        child_gen = bin_packing_cross(parent1, parent2)

    return child_gen


def bin_packing_cross(parent1: Individual, parent2: Individual):
    child_gen = []
    ran = random.random()
    copy_objects = parent1.objects.copy()
    size_gen = len(copy_objects)

    # fill child with empty bins
    for i in range(size_gen):
        child_gen.append([])

    parent1_part = int(len(copy_objects) * ran)
    parent2_part = len(copy_objects) - parent1_part

    for i in range(parent1_part):
        object = random.sample(copy_objects, 1)[0]
        for bin in range(len(parent1.gen)):
            if object in parent1.gen[bin]:
                while object + sum(child_gen[bin]) > parent1.max_weight:
                    bin = random.randint(0, size_gen - 1)
                child_gen[bin].append(object)
                copy_objects.remove(object)
                break

    for i in range(parent2_part):
        object = random.sample(copy_objects, 1)[0]
        for bin in range(len(parent2.gen)):
            if object in parent2.gen[bin]:
                while object + sum(child_gen[bin]) > parent2.max_weight:
                    bin = random.randint(0, size_gen - 1)
                child_gen[bin].append(object)
                copy_objects.remove(object)
                break

    return child_gen


def pmx_shuffle(parent1: Individual, parent2: Individual, num_genes: int):
    p1 = parent1.gen
    p2 = parent2.gen
    rand_a = random.randint(0, num_genes / 2)

    for i in range(rand_a):
        temp_p1 = p1[i]  # set the indexes
        temp_p2 = p2[i]
        try:
            temp_index1 = p1.index(p2[i])
            temp_index2 = p2.index(p1[i])

            p1[i] = p1[temp_index1]  # switch the values
            p1[temp_index1] = temp_p1

            p2[i] = p2[temp_index2]
            p2[temp_index2] = temp_p2

        except:
            pass

    rand_a = random.randint(0, num_genes)
    child_gen = [p1[i] if i < rand_a else p2[i] for i in range(num_genes)]

    return child_gen


def cx_shuffle(parent1: Individual, parent2: Individual, num_genes: int):
    p1 = parent1.gen
    p2 = parent2.gen

    cycles = [-1] * len(p1)
    cycle_no = 1
    cycle_start = (i for i, v in enumerate(cycles) if v < 0)

    for pos in cycle_start:

        while cycles[pos] < 0:
            cycles[pos] = cycle_no
            if p2[pos] in p1:
                pos = p1.index(p2[pos])
            else:
                pos = 0
        cycle_no += 1

    child_gen = [p1[i] if n % 2 else p2[i] for i, n in enumerate(cycles)]

    return child_gen
