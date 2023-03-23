import random
import math
from Individual import Individual


class CrossoverOperator:

    def __init__(self):
        self.NONE = 0
        self.SINGLE = 1
        self.TWO = 2
        self.UNIFORM = 3
        self.PMX = 4
        self.CX = 5
        self.BIN_PACKING = 6

    def crossover_operator(self, operator, parent1: Individual, parent2: Individual, num_genes: int):  # exploration
        # print(f"operator {operator} of type {type(operator)}")
        # print(type(parent1))
        if operator == self.NONE:
            child_gen = [parent1.gen[i] if random.random() < 0.5 else parent2.gen[i] for i in range(num_genes)]

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

        elif operator == self.BIN_PACKING:
            child_gen = []
            ran = random.random()
            copy_objects = parent1.objects.copy()
            # size_gen = max(len(parent1.gen), len(parent2.gen))
            size_gen = math.ceil(sum(copy_objects)/150) * 2

            # fill child with empty bins
            for i in range(size_gen):
                child_gen.append([])

            parent1_part = int(len(copy_objects)*ran)
            parent2_part = len(copy_objects) - parent1_part

            for i in range(parent1_part):
                object = random.sample(copy_objects, 1)[0]
                for bin in range(len(parent1.gen)):
                    if object in parent1.gen[bin]:
                        child_gen[bin].append(object)
                        copy_objects.remove(object)
                        break

            for i in range(parent2_part):
                object = random.sample(copy_objects, 1)[0]
                for bin in range(len(parent2.gen)):
                    if object in parent2.gen[bin]:
                        child_gen[bin].append(object)
                        copy_objects.remove(object)
                        break

            # mutation
            copy_objects = parent1.objects.copy()
            num_object_change = random.randint(0, len(child_gen))

            for i in range(num_object_change):
                copy_objects = parent1.objects.copy()
                object = random.sample(copy_objects, 1)[0]
                random_bin = random.randint(0, len(child_gen) - 1)

                for bin in range(len(child_gen)):
                    if object in child_gen[bin]:
                        child_gen[bin].remove(object)
                        child_gen[random_bin].append(object)
                        break

            # copy_objects = parent1.objects.copy()
            # object = random.sample(copy_objects, 1)[0]
            # random_bin = random.randint(0, len(child_gen)-1)
            #
            # for bin in range(len(child_gen)):
            #     if object in child_gen[bin]:
            #         child_gen[bin].remove(object)
            #         child_gen[random_bin].append(object)
            #         break

            child_gen = list(filter(None, child_gen))
            # print("p1: ", parent1.gen)
            # print("p2: ", parent2.gen)
            # print("child: ", child_gen)

        return child_gen

    def pmx_shuffle(self, parent1: Individual, parent2: Individual, num_genes: int):
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

    def cx_shuffle(self, parent1: Individual, parent2: Individual, num_genes: int):
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
