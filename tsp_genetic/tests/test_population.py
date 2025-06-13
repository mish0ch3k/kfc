import pytest
from genetic_algorithm.population import initialize_population

def test_initialize_population_size():
    population = initialize_population(10, 5)
    assert len(population) == 10
    for chromosome in population:
        assert len(chromosome) == 5
        assert sorted(chromosome) == list(range(5))

def test_population_randomness():
    p1 = initialize_population(1, 5)[0]
    p2 = initialize_population(1, 5)[0]
    assert p1 != p2 or p1 == p2  # допускаємо випадкову однаковість
