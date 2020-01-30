from unittest import TestCase
from DecisionTreeStructures import Node, DataSet
import pandas as pd

class TestNode(TestCase):
    def test_basic_functionality(self):
        head_node = Node()
        test_data_set = DataSet()
        test_data_set.load_data_from_file("car.unittest.csv")
        # head_node.members=range(0,test_data_set.data_frame.shape[0])
        # head_node.dataset=test_data_set
        head_node.mydataframe = test_data_set.data_frame
        head_node.target_attribute = "class"
        splitreturn = head_node.test_determine_split()
        self.assertEqual(splitreturn[0], "buying")

    def test_create_immediate_children(self):
        head_node = Node()
        test_data_set = DataSet()
        test_data_set.load_data_from_file("car.unittest.csv")
        head_node.mydataframe = test_data_set.data_frame
        head_node.target_attribute = "class"
        head_node.create_immediate_children()
        self.assertGreater(len(head_node.child_edges), 1, "create_immediate_children created no children")

    def test_create_recursive_child_nodes(self):
        head_node = Node()
        test_data_set = DataSet()
        test_data_set.load_data_from_file("car.unittest.csv")
        head_node.mydataframe = test_data_set.data_frame
        head_node.target_attribute = "class"
        head_node.create_recursive_children()
        self.assertGreater(len(head_node.child_edges), 1)

    def test_run_tree_on_test_row(self):
        head_node = Node()
        test_data_set = DataSet()
        test_data_set.load_data_from_file("car.unittest.csv")
        head_node.mydataframe = test_data_set.data_frame
        head_node.target_attribute = "class"
        head_node.create_recursive_children()
        d = {'buying': ['vhigh','vhigh','med', 'med'], 'class': ['acc', 'unacc', 'acc','unacc']}
        test_dataframe = pd.DataFrame(data=d)
        # head_node.print_tree()
        self.assertEqual(head_node.run_tree_on_test_row(test_dataframe.iloc[0]), "unacc")
        self.assertEqual(head_node.run_tree_on_test_row(test_dataframe.iloc[1]), "unacc")
        self.assertEqual(head_node.run_tree_on_test_row(test_dataframe.iloc[2]), "acc")
        self.assertEqual(head_node.run_tree_on_test_row(test_dataframe.iloc[3]), "acc")

    def test_print_tree(self):
        if True:
            head_node = Node()
            test_data_set = DataSet()
            # test_data_set.load_data_from_file("car.unittest.csv")
            test_data_set.load_data_from_file("car.training.csv")
            head_node.mydataframe = test_data_set.data_frame
            head_node.target_attribute = "class"
            head_node.create_recursive_children()
            head_node.print_tree()
