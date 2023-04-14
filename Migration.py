# ----------- Python Package -----------
import random
# ----------- Consts Name  -----------
CONSTRAINT_1 = 0
CONSTRAINT_2 = 1


def migration(population: list, target_population: list, viability_fuc_num):

    immigrant = immigrant_selection(population, number_of_competitors = 2)
    legal_transfer = viability_fuc(viability_fuc_num, immigrant, target_population)

    # Perform migration if legal
    if legal_transfer:
        population.remove(immigrant)
        target_population.append(immigrant)

    return population, target_population


# Selection of the immigrant according to size-2 tournament method
def immigrant_selection(population: list, number_of_competitors):
    number_of_immigrants = 1
    k_fitness = []
    k_individual = random.choices(population, k=number_of_competitors)
    for individual in k_individual:
        k_fitness.append(individual.score_share)

    k_sorted = sorted(range(number_of_immigrants), key=lambda i: k_fitness[i], reverse=True)[:number_of_immigrants]
    immigrant = k_sorted[0]

    return immigrant


# Checking if it is legal to transfer the immigrant to the target population by viability function
def viability_fuc(viability_fuc_num, immigrant, target_population):
    citizen = random.choices(target_population, k=1)[0]
    if viability_fuc_num == CONSTRAINT_1:
        if citizen.score_share ** 2 + immigrant.score_share** 2 <= 3:
            return True

    elif viability_fuc_num == CONSTRAINT_2:
        if (citizen.score_share-5) ** 2 + (immigrant.score_share-5) ** 2 <= 2:
            return True

    return False




