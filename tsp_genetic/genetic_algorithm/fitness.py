import math

# Відстань між двома містами
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def route_length(route, cities):
    total = 0
    for i in range(len(route)):
        a = cities[route[i]]
        b = cities[route[(i + 1) % len(route)]]
        total += distance(a, b)
    return total

# Оцінка всіх особин популяції
def evaluate_population(population, cities):
    return [1 / route_length(individual, cities) for individual in population]
