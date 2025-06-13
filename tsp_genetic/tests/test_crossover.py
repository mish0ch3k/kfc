from genetic_algorithm.crossover import order_crossover
import random

def test_order_crossover_validity():
    parent1 = list(range(10))
    parent2 = parent1[::-1]
    child = order_crossover(parent1, parent2)
    assert sorted(child) == list(range(10))
    assert len(set(child)) == 10
