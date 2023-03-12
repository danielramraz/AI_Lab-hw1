# %%
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from enum import Enum

MUTATION_INDIVIDUALS = 10

class CROSSOVER_OPERATOR (Enum):
    NONE = 0
    SINGLE = 1
    TWO = 2
    UNIFORM = 3


# Define the fitness function
def fitness(individual):                                    # explotation
    target = list("Hello, world!")
    score = 0
    for i in range(len(individual)):
        if individual[i] == target[i]:
            score += 1

    bullsEyeScore = bulls_eye(individual, target, score) #add rienforcement to fitness func
    # bullsEyeScore = 0
    # score = 0
    return (score, bullsEyeScore)


# Define the genetic algorithm
def genetic_algorithm(pop_size, num_genes, fitness_func, max_generations, cross_operator):
    # Initialize the population with random individuals
    population = []
    fitnesses = [(0,0)]
    for i in range(pop_size):
        individual = [chr(random.randint(32, 126)) for j in range(num_genes)]
        population.append(individual)

    # Evolve the population for a fixed number of generations
    for generation in range(max_generations):
        mutation_individuals = MUTATION_INDIVIDUALS
        old_average = averege_fitness(fitnesses[0])
        fitnesses = [fitness_func(individual) for individual in population]         # exploitation
        new_average = averege_fitness(fitnesses[0])

        genTime = time.time()                                                       # information
        print("=========================================")
        print(f"the start time for this gen is {time.asctime(time.gmtime(genTime))}")
        print(f"--------averege for this gen is {new_average}")
                
        show_histogram(fitnesses)
        
        # Select the best individuals for reproduction
        elite_size = int(pop_size * 0.1)                                                # exploitation
        elite_indices = sorted(range(pop_size), key=lambda i: fitnesses[i], reverse=True)[:elite_size]
        elites = [population[i] for i in elite_indices]

        # Generate new individuals by applying crossover and mutation operators
        offspring = []
        while len(offspring) < pop_size - elite_size:
            parent1 = random.choice(elites)
            parent2 = random.choice(elites)
            child = crossover_operator(cross_operator , parent1 , parent2 , num_genes)          # exploration   
            offspring.append(child)

            if (new_average == old_average and mutation_individuals > 0):
                child = mutation(child)
                mutation_individuals -= 1

        population = elites + offspring
        
        print(f"the absolute time for this gen is {time.time() - genTime} sec")
        # print(f"the ticks time for this gen is {int(time.perf_counter())}")


    # Find the individual with the highest fitness
    best_individual = max(population, key=lambda individual: fitness_func(individual))          # exploitation
    best_fitness = fitness_func(best_individual)
    
    return best_individual, best_fitness

def crossover_operator(operator, parent1 , parent2, num_genes):     # exploration
    # print(f"operator {operator} of type {type(operator)}")
    if operator == CROSSOVER_OPERATOR.NONE.value:
        child = random.choice([parent1, parent2])
        
    if operator == CROSSOVER_OPERATOR.SINGLE.value:
        rand_a = random.randint(0, num_genes)
        # print(f"random {rand_a}")
        child = [parent1[i] if i < rand_a else parent2[i] for i in range(num_genes)]

    elif operator == CROSSOVER_OPERATOR.TWO.value:
        rand_a = random.randint(0, num_genes-1)
        rand_b = random.randint(rand_a , num_genes)
        # print(f"random {rand_a} , {rand_b}")
        child = [parent1[i] if i < rand_a or  i > rand_b else parent2[i] for i in range(num_genes)]

    elif operator == CROSSOVER_OPERATOR.UNIFORM.value:
        child = [parent1[i] if random.choice([0,1]) else parent2[i] for i in range(num_genes)]

    return child
   
def bulls_eye(individual, target, score):                   # exploitation
    for i in range(len(individual)):
        if individual[i] == target[i]:
            score += 10
        elif individual[i] in target:
            score += 5
    return score

def averege_fitness(fitness):  # information
    if not fitness:  
        return (0, 0)
    averege = sum(fitness) / len(fitness)
    variance = sum([((x-averege)**2) for x in fitness]) / len(fitness)-1
    sd = variance**0.5
    return (averege, sd)

def show_histogram(array):
    np_array = np.array(array)
    plt.hist(np_array)
    plt.show()
    return

def mutation(individual):                # exploration
    num_genes = len(individual)
    rand_gen = random.randint(0, num_genes-1)
    individual[rand_gen] = chr(random.randint(32, 126))
    return individual
    


def main():
    # Run the genetic algorithm and print the result
    crossover_operator_input = int(input("Enter the number of crossover operator:\nNone = 0 \nSingel = 1\nTwo = 2\nUniform = 3\n"))
    
    total_time = time.time()                                                       # information
    print(f"the start time for this algo is {time.asctime(time.gmtime(total_time))}")

    best_individual, best_fitness = genetic_algorithm(pop_size = 100, 
                                                      num_genes = 13, 
                                                      fitness_func = fitness, 
                                                      max_generations = 100,
                                                      cross_operator = crossover_operator_input)
    
    print(f"the total time for this algo is {time.time() - total_time} sec")
    print(f"the ticks time for this algo is {int(time.perf_counter())}")

    print("Best individual:", ''.join(best_individual))
    print("Best fitness:", best_fitness)
    return

if __name__ == "__main__":
    main()


# %%
