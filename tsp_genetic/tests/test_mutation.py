from genetic_algorithm.mutation import reverse_mutation
import random

def test_reverse_mutation_validity():
    original = list(range(10))
    mutated = reverse_mutation(original[:])
    assert sorted(mutated) == list(range(10))
    assert len(mutated) == len(original)
