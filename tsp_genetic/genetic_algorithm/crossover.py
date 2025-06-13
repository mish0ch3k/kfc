import random

def order_crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    hole = parent1[a:b]

    child = [None] * size
    child[a:b] = hole

    pointer = b
    for gene in parent2[b:] + parent2[:b]:
        if gene not in hole:
            if pointer >= size:
                pointer = 0
            child[pointer] = gene
            pointer += 1

    return child

def crossover_population(parents, crossover_rate):
    offspring = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[(i + 1) % len(parents)]
        if random.random() < crossover_rate:
            child1 = order_crossover(parent1, parent2)
            child2 = order_crossover(parent2, parent1)
        else:
            child1, child2 = parent1[:], parent2[:]
        offspring.extend([child1, child2])
    return offspring
