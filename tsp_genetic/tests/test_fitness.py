from genetic_algorithm.fitness import route_length, evaluate_population

def test_route_length_simple():
    cities = {
    0: [0, 0],
    1: [3, 4]
    }
    route = [0, 1]
    dist = route_length(route, cities)
    assert round(dist, 2) == 10.0  # 5 (0->1) + 5 (1->0)

def test_evaluate_population():
    cities = {
    0: [0, 0],
    1: [3, 4]
    }
    population = [[0, 1], [1, 0]]
    fitness = evaluate_population(population, cities)
    assert len(fitness) == 2
    assert all(f > 0 for f in fitness)
