# ----------- Python Package -----------
import random
import numpy as np
# ----------- Consts Name  -----------
NONE = 0
RWS = 1
SUS = 2
TOURNAMENT_RANKING = 3


def parent_selection_function(parent_selection_input: int, population: list, elites: list):
    if parent_selection_input == NONE:
        return [random.choice(elites), random.choice(elites)]
    elif parent_selection_input == RWS:
        return rws(population)
    elif parent_selection_input == SUS:
        return sus(population)
    elif parent_selection_input == TOURNAMENT_RANKING:
        return tournament_ranking(population)

    return


def rws(population: list):
    sum_score = score_sum(population)
    fitness = winsorize(population)
    weight_arr = []
    for index in range(len(fitness)):
        weight_arr.append(abs(fitness[index] / sum_score))

    return random.choices(population, weights=weight_arr, k=2)


def sus(population: list):
    sum_score = score_sum(population)
    fitness = winsorize(population)

    for index, individual in enumerate(population):
        if index > 0:
            fitness[index] += fitness[index - 1]

    parents = []
    number_of_parents = 2
    slice_size = int(sum_score / len(population))
    first_spine_pointer = int(random.uniform(0, slice_size))
    delta = sum_score / number_of_parents

    for i in range(number_of_parents):
        fit = first_spine_pointer + i * delta
        current, j = 0, 0
        while current < fit and j < len(population):
            current += population[j].score
            j += 1
        if j == len(population):
            parents.append(population[j-1])
        else:
            parents.append(population[j])

    return parents


def tournament_ranking(population: list):

    number_of_competitors = 30
    number_of_parents = 2
    k_fitness = []

    k_individual = random.choices(population, k=number_of_competitors)
    for individual in k_individual:
        k_fitness.append(individual.score)

    k_sorted = sorted(range(number_of_competitors), key=lambda i: k_fitness[i], reverse=True)[:number_of_parents]
    parents = [k_individual[i] for i in k_sorted]

    return parents


def score_sum(population: list):
    sum_score = 0
    for individual in population:
        sum_score += individual.score
    return sum_score


def winsorize(population: list, percentile=5):
    fitneses = []
    for individual in population:
        fitneses.append(individual.score_share)

    lower_bound = np.percentile(fitneses, percentile)
    upper_bound = np.percentile(fitneses, 100 - percentile)
    fitneses = np.where(fitneses < lower_bound, lower_bound, fitneses)
    fitneses = np.where(fitneses > upper_bound, upper_bound, fitneses)
    mean = np.mean(fitneses)
    std = np.std(fitneses)
    try:
        fitneses = (fitneses - mean) / std
    except:
        fitneses = 0

    return fitneses
