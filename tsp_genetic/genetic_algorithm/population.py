import random


def initialize_population(pop_size, chromosome_length):
    population = []
    for _ in range(pop_size):
        chromosome = list(range(chromosome_length))
        random.shuffle(chromosome)
        population.append(chromosome)
    return population