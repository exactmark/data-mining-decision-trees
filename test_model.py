from unittest import TestCase
from DecisionTreeStructures import *


class TestModel(TestCase):
    def test_instantiate_and_create_model(self):
        new_model = Model(training_path="car.unittest.csv", target_attribute="class")
        # new_model.create_model()
        self.assertIsInstance(new_model.head_node, Node)
        self.assertGreater(len(new_model.head_node.child_edges), 1)

    def skip_test_test_model(self):
        # new_model = Model(training_path="car.unittest.csv", target_attribute="class")
        new_model = Model(training_path="car.training.csv", target_attribute="class")
        self.assertIsInstance(new_model.head_node, Node)
        self.assertGreater(len(new_model.head_node.child_edges), 1)
        testing_data_set = DataSet()
        testing_data_set.load_data_from_file("car.test.csv")
        test_result = new_model.test_model(testing_data_set.data_frame)
        test_result.print()

    def test_create_plot(self):
        # new_model = Model(training_path="car.unittest.csv", target_attribute="class")
        new_model = Model(training_path="car.training.csv", target_attribute="class")
        self.assertIsInstance(new_model.head_node, Node)
        self.assertGreater(len(new_model.head_node.child_edges), 1)
        new_model.create_plot("mytree.pdf")
