import unittest
import numpy as np
from ant_colony import generate_cities, distance_matrix, initialize_pheromones,construct_route, route_length, update_pheromones

class TestAntColony(unittest.TestCase):
    def setUp(self):
        self.cities = generate_cities(5)
        self.dist_matrix = distance_matrix(self.cities)
        self.pheromone = initialize_pheromones(5)

    def test_distance_matrix_symmetry(self):
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                self.assertAlmostEqual(self.dist_matrix[i][j], self.dist_matrix[j][i])

    def test_construct_route_validity(self):
        route = construct_route(self.pheromone, self.dist_matrix)
        self.assertEqual(len(route), len(set(route)))
        self.assertEqual(len(route), len(self.cities))

    def test_route_length_positive(self):
        route = construct_route(self.pheromone, self.dist_matrix)
        length = route_length(route, self.dist_matrix)
        self.assertGreater(length, 0)

    def test_pheromone_update_changes_values(self):
        routes = [construct_route(self.pheromone, self.dist_matrix) for _ in range(3)]
        lengths = [route_length(route, self.dist_matrix) for route in routes]
        old = self.pheromone.copy()
        new = update_pheromones(old.copy(), routes, lengths)
        self.assertTrue((new != old).any())

if __name__ == '__main__':
    unittest.main()
