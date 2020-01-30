from unittest import TestCase
from MathFunctions import create_binary_subsets


class TestCreate_permutations(TestCase):
    def test_create_permutations(self):
        startlist = ["a", "b", "c", "d"]
        return_permutations = create_binary_subsets(startlist)
        # print(return_permutations)
        # assert len(return_permutations) == pow(2, len(startlist))
