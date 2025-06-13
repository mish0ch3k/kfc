from genetic_algorithm.utils import get_best_solution, should_terminate

def test_get_best_solution():
    cities = {
        "0": [0, 0],
        "1": [3, 4],
        "2": [0, 3]
    }
    population = [[0, 1, 2], [2, 1, 0]]
    best, dist = get_best_solution(population, cities)
    assert isinstance(best, list)
    assert dist > 0

def test_should_terminate():
    assert should_terminate(200, 0.001, max_generations=200)
    assert not should_terminate(50, 1000)
