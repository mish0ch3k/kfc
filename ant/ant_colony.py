import numpy as np
import matplotlib.pyplot as plt
import random
import csv

ALPHA = 1.0
BETA = 5.0
EVAPORATION = 0.5
Q = 100.0


def generate_cities(n):
    return np.random.rand(n, 2) * 100


def distance_matrix(cities):
    n = len(cities)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = np.linalg.norm(cities[i] - cities[j])
    return matrix


def initialize_pheromones(n):
    return np.ones((n, n))


def construct_route(pheromone, dist_matrix):
    n = len(pheromone)
    route = [random.randint(0, n - 1)]
    visited = set(route)
    for _ in range(n - 1):
        i = route[-1]
        probabilities = []
        for j in range(n):
            if j not in visited:
                tau = pheromone[i][j] ** ALPHA
                eta = (1 / dist_matrix[i][j]) ** BETA
                probabilities.append((j, tau * eta))
        total = sum(p for _, p in probabilities)
        r = random.random()
        cum_prob = 0
        for city, prob in probabilities:
            cum_prob += prob / total
            if r <= cum_prob:
                route.append(city)
                visited.add(city)
                break
    return route


def route_length(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))


def update_pheromones(pheromone, routes, lengths):
    pheromone *= (1 - EVAPORATION)
    for route, length in zip(routes, lengths):
        for i in range(len(route)):
            a, b = route[i], route[(i + 1) % len(route)]
            pheromone[a][b] += Q / length
            pheromone[b][a] += Q / length
    return pheromone


def plot_route(route, cities, title="Найкращий маршрут"):
    x = [cities[i][0] for i in route] + [cities[route[0]][0]]
    y = [cities[i][1] for i in route] + [cities[route[0]][1]]
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-')
    for i, city in enumerate(route):
        plt.text(cities[city][0], cities[city][1], str(city), fontsize=9)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


def ant_colony_optimization(num_cities, num_ants, num_iterations):
    cities = generate_cities(num_cities)
    dist_matrix = distance_matrix(cities)
    pheromone = initialize_pheromones(num_cities)
    best_route = None
    best_length = float('inf')
    history = []

    for iteration in range(num_iterations):
        routes = []
        lengths = []
        for _ in range(num_ants):
            route = construct_route(pheromone, dist_matrix)
            length = route_length(route, dist_matrix)
            routes.append(route)
            lengths.append(length)
            if length < best_length:
                best_route = route
                best_length = length
        avg_length = sum(lengths) / len(lengths)
        history.append((iteration + 1, best_length, avg_length))
        pheromone = update_pheromones(pheromone, routes, lengths)

    return best_route, best_length, cities, history


def save_statistics(history, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ітерація', 'Найкраща довжина', 'Середня довжина'])
        writer.writerows(history)


if __name__ == '__main__':
    best_route, best_length, cities, stats = ant_colony_optimization(20, 30, 100)
    plot_route(best_route, cities)
    save_statistics(stats, 'statistics.csv')
