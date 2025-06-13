from genetic_algorithm.selection import select_parents
from genetic_algorithm.population import initialize_population
from genetic_algorithm.fitness import evaluate_population

def test_selection_methods():
    cities = {
        str(i): [i, 0] for i in range(5)
    }
    population = initialize_population(10, 5)
    fitness = evaluate_population(population, cities)

    selected_tournament = select_parents(population, fitness, method="tournament")
    selected_roulette = select_parents(population, fitness, method="roulette")

    assert len(selected_tournament) == len(population)
    assert len(selected_roulette) == len(population)
    for ind in selected_tournament + selected_roulette:
        assert sorted(ind) == list(range(5))
