from unittest import TestCase
from DecisionTreeStructures import DataSet
from MathFunctions import determine_best_split
import pandas as pd


class TestDetermine_best_split(TestCase):
    def test_determine_best_split(self):
        test_data_set = DataSet()
        test_data_set.load_data_from_file("car.unittest.csv")
        det_best_split_result = determine_best_split(test_data_set.data_frame, "class")
        det_best_split_expected = ['buying', (['vhigh'], ['med']), 0.0]
        self.assertEqual(det_best_split_result, det_best_split_expected)

    def test_determine_best_split_no_target_difference(self):
        d = {'col1': [1, 2, 2], 'col2': [3, 3, 3]}
        test_dataframe = pd.DataFrame(data=d)
        det_best_split_result = determine_best_split(test_dataframe, "col2")
        det_best_split_expected = [None, None, None]
        self.assertEqual(det_best_split_result, det_best_split_expected)

    def test_determine_best_split_homogenous_splitter(self):
        d = {'col1': [2, 2, 2], 'col2': [1, 3, 3]}
        test_dataframe = pd.DataFrame(data=d)
        det_best_split_result = determine_best_split(test_dataframe, "col2")
        det_best_split_expected = [None, None, None]
        self.assertEqual(det_best_split_result, det_best_split_expected)

    def test_determine_best_split_multiple_homogenous_splitters(self):
        d = {'col1': [2, 2, 2], 'col1a': [2, 2, 2], 'col2': [1, 3, 3]}
        test_dataframe = pd.DataFrame(data=d)
        det_best_split_result = determine_best_split(test_dataframe, "col2")
        det_best_split_expected = [None, None, None]
        self.assertEqual(det_best_split_result, det_best_split_expected)
