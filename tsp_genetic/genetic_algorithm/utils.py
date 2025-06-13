from genetic_algorithm.fitness import route_length


def get_best_solution(population, cities):
    best = None
    best_distance = float("inf")
    for individual in population:
        dist = route_length(individual, cities)
        if dist < best_distance:
            best_distance = dist
            best = individual
    return best, best_distance


def should_terminate(current_generation, best_distance, max_generations=200, tolerance=1e-4):
    return current_generation >= max_generations or best_distance < tolerance
