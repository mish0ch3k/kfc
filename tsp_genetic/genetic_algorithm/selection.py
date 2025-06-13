import random

def tournament_selection(population, fitness_scores, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        participants = random.sample(list(zip(population, fitness_scores)), tournament_size)
        winner = max(participants, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected

def roulette_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    selected = []
    for _ in range(len(population)):
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual, fitness in zip(population, fitness_scores):
            current += fitness
            if current >= pick:
                selected.append(individual)
                break
    return selected

def select_parents(population, fitness_scores, method="tournament"):
    if method == "roulette":
        return roulette_selection(population, fitness_scores)
    else:
        return tournament_selection(population, fitness_scores)
