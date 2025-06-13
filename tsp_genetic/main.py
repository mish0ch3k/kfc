from genetic_algorithm.population import initialize_population
from genetic_algorithm.fitness import evaluate_population
from genetic_algorithm.selection import select_parents
from genetic_algorithm.crossover import crossover_population
from genetic_algorithm.mutation import mutate_population
from genetic_algorithm.utils import get_best_solution, should_terminate
from visual.plot_routes import plot_route
import matplotlib.pyplot as plt
import json
import time

POPULATION_SIZE = 100
GENERATIONS = 200
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2


def load_cities(filepath="data/cities.json"):
    with open(filepath, 'r') as f:
        data = json.load(f)
        return {int(k): v for k, v in data.items()}



def main():
    cities = load_cities()
    population = initialize_population(POPULATION_SIZE, len(cities))

    for generation in range(GENERATIONS):
        fitness_scores = evaluate_population(population, cities)
        parents = select_parents(population, fitness_scores)
        offspring = crossover_population(parents, CROSSOVER_RATE)
        mutated = mutate_population(offspring, MUTATION_RATE)
        population = mutated

        best = get_best_solution(population, cities)
        print(f"Generation {generation + 1}: Best distance = {best[1]:.2f}")

        if should_terminate(generation, best[1]):
            break

    best_route, best_distance = get_best_solution(population, cities)
    print("Best found solution:", best_route)
    print("Distance:", best_distance)
    plot_route(best_route, cities)
    

if __name__ == "__main__":
    main()
    