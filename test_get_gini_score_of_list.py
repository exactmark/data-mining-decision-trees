from unittest import TestCase
from MathFunctions import get_gini_score_of_single_list, get_weighted_gini_score


class TestGet_gini_score_of_list(TestCase):
    def test_gini_score_simple_list(self):
        test_cases = [[[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], 0.5],
                      [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0.0],
                      [[0, 0, 0, 0, 0, 1, 1], 0.408],
                      [[0, 0, 0, 0, 1], 0.32]]
        for arg, expected in test_cases:
            assert round(get_gini_score_of_single_list(arg), 3) == round(expected, 3), "expected %f but got %f" % (
                expected, get_gini_score_of_single_list(arg))

    def test_gini_score_handles_strings(self):
        test_cases = [[[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], 0.5],
                      [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0.0],
                      [[0, 0, 0, 0, 0, 1, 1], 0.408],
                      [["a", "a", "a", "a", "b"], 0.32]]
        for arg, expected in test_cases:
            assert round(get_gini_score_of_single_list(arg), 3) == round(expected, 3), "expected %f but got %f" % (
                expected, get_gini_score_of_single_list(arg))

    def test_get_weighted_gini_score_with_simple_input(self):
        test_cases = [[[[0, 0, 0, 0, 0, 1, 1], [0, 1, 1, 1, 1]], 0.371]]
        for arg, expected in test_cases:
            weighted = get_weighted_gini_score(arg)
            assert round(weighted, 3) == round(expected, 3), "expected %f but got %f" % (expected, weighted)
