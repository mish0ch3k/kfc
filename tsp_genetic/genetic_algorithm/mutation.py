import random

# Інверсія ділянки маршруту
def reverse_mutation(individual):
    a, b = sorted(random.sample(range(len(individual)), 2))
    individual[a:b] = reversed(individual[a:b])
    return individual

# Мутація всієї популяції
def mutate_population(population, mutation_rate):
    mutated = []
    for individual in population:
        if random.random() < mutation_rate:
            individual = reverse_mutation(individual[:])
        mutated.append(individual)
    return mutated
