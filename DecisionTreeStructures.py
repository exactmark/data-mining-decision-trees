import pandas as pd
import datetime
import MathFunctions


class DataSet:

    def __init__(self):
        self.data_frame = None

    def load_data_from_file(self, filePath):
        if str(filePath).startswith("car."):
            self.columnmap = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"]
            self.data_frame = pd.read_csv(filePath, header=None, names=self.columnmap)
        else:
            # else assume a generic file
            self.data_frame = pd.read_csv(filePath)
            self.columnmap = self.data_frame.columns


class Node:
    class child_edge():
        def __init__(self):
            self.split_portion = None
            self.node_ptr = None

    def __init__(self, *args, **kwargs):
        self.decision_method = "gini"
        # Str version of ordinal decision type (include,lessthan,greaterthan?
        self.decision = ""
        # Column to use for decision
        self.decision_attribute = None
        # Set of child_nodes
        self.child_edges = []
        # ideally a pointer to the parent node
        self.parent_node = kwargs.get('parent_node',None)
        self.mydataframe = None
        self.target_attribute = None
        self.depth = 0
        self.score = 0
        self.leaf_class = None

    def test_determine_split(self):
        assert self.target_attribute in self.mydataframe.columns, self.target_attribute + " was not in column map"
        split_column, split_values, trash = MathFunctions.determine_best_split(self.mydataframe, self.target_attribute)
        return (split_column, split_values)

    def create_immediate_children(self):
        assert self.mydataframe is not None, "create_child_nodes called with no dataframe"
        assert self.target_attribute is not None, "create child nodes called with no target_attribute"

        # TODO keeping track of columns still available to be split on subsequent nodes would allow us to feed the column list into
        # TODO determine best split.  This would cut back on checks therein (depending on how expensive pandas.unique is)
        split_column, split_values, score = MathFunctions.determine_best_split(self.mydataframe, self.target_attribute)

        # if no available split, then this is a leaf.
        if not split_column:
            target_classes = self.mydataframe[self.target_attribute].unique()
            assert len(target_classes) == 1
            self.leaf_class = target_classes[0]

        # otherwise, make more nodes
        else:
            self.score = score
            self.decision_attribute = split_column
            for single_split in split_values:
                new_child = Node(parent_node=self)
                new_child.depth = self.depth + 1
                new_child.target_attribute = self.target_attribute
                child_dataframe = self.mydataframe.loc[self.mydataframe[split_column].isin(single_split)]
                new_child.mydataframe = child_dataframe
                new_child_edge = self.child_edge()
                new_child_edge.node_ptr = new_child
                new_child_edge.split_portion = single_split
                self.child_edges.append(new_child_edge)

    def create_recursive_children(self):
        assert self.mydataframe is not None, "create_child_nodes called with no dataframe"
        assert self.target_attribute is not None, "create child nodes called with no target_attribute"
        self.create_immediate_children()
        for single_edge in self.child_edges:
            single_edge.node_ptr.create_recursive_children()

    def print_tree(self):
        def print_depth_formatter(node):
            for x in range(0, node.depth):
                print("--|-", end="")

        if self.decision_attribute:
            print_depth_formatter(self)
            print("Decision: " + self.decision_attribute + ", " + self.decision_method + "=" + str(
                self.score) + ", " + str(self.get_len_contained_rows()) + " records")
            for single_edge in self.child_edges:
                print_depth_formatter(self)
                print("--", end="")
                print("Attribute: " + " or ".join(single_edge.split_portion))
                single_edge.node_ptr.print_tree()
        else:
            print_depth_formatter(self)
            print("--", end="")
            print("Class: " + self.leaf_class + ", " + str(self.get_len_contained_rows()) + " records")

    def get_len_contained_rows(self):
        return self.mydataframe.shape[0]

    def run_tree_on_test_row(self, test_series):
        if self.leaf_class:
            return self.leaf_class
        assert test_series[
            self.decision_attribute], "Node decision point " + self.decision_attribute + " not in test frame"
        for single_edge in self.child_edges:
            # print(test_frame[self.decision_attribute])
            if test_series[self.decision_attribute] in single_edge.split_portion:
                return single_edge.node_ptr.run_tree_on_test_row(test_series)
        assert True == False, "Unable to find tree/node"

    def create_equivalent_ete_tree(self):
        import ete3 as ete
        t = ete.Tree()
        self.add_ete_self_and_children(t)
        return t

    def add_ete_self_and_children(self,prototree):
        node_name = ""
        if self.leaf_class:
            node_name=self._get_node_branch_decision()+", class:" + self.leaf_class
        else:
            node_name=self._get_node_branch_decision()

        this_node=prototree.add_child(name=node_name)
        if not self.leaf_class:
            weight=(0.5-self.score)*50
            # print("score %f weight %f"%(self.score,weight))
            this_node.add_features(weight=weight)
        for single_edge in self.child_edges:
            single_edge.node_ptr.add_ete_self_and_children(this_node)

    def _get_node_branch_decision(self):
        branch_decision=""
        if self.parent_node:
            self_decision=self.parent_node.decision_attribute
            myportion=[]
            for single_edge in self.parent_node.child_edges:
                if single_edge.node_ptr == self:
                    myportion=single_edge.split_portion
            branch_decision=self_decision+"= "+" or ".join(myportion)


        return branch_decision


class Model_Test_Result:
    def __init__(self):
        self.tested_rows = 0
        self.true_positive = 0
        self.true_negative = 0
        self.false_positive = 0
        self.false_negative = 0

    def print(self):
        print("Tested rows: %i" % self.tested_rows)
        accuracy = (self.true_positive + self.true_negative) / self.tested_rows
        print("Accuracy: %1.2f" % accuracy)
        print("True positive: %1.2f" % (self.true_positive / self.tested_rows))
        print("True negative: %1.2f" % (self.true_negative / self.tested_rows))
        print("False positive: %1.2f" % (self.false_positive / self.tested_rows))
        print("False negative: %1.2f" % (self.false_negative / self.tested_rows))


class Model:
    def __init__(self, *args, **kwargs):
        self.head_node = None
        self.data_set = kwargs.get('data_set', None)
        self.training_path = kwargs.get('training_path', None)
        if self.training_path:
            self.data_set = DataSet()
            self.data_set.load_data_from_file(self.training_path)
        self.target_attribute = kwargs.get('target_attribute', None)
        if self.data_set and self.target_attribute:
            self._create_model()
        self.testing_result = Model_Test_Result()

    def _create_model(self, method='gini', data_set=None, **kwargs):
        if data_set:
            self.data_set = data_set
        assert self.data_set, "create model called without dataset"
        self.head_node = Node()
        self.head_node.mydataframe = self.data_set.data_frame
        self.head_node.target_attribute = self.target_attribute
        self.head_node.create_recursive_children()

    def test_model(self, test_data_frame):
        assert self.head_node,"Test model called without model creation"
        self.testing_result = Model_Test_Result()

        for x in range(0, test_data_frame.shape[0]):
            actual_pos = test_data_frame.iloc[x][self.target_attribute] == "acc"
            predict_pos = self.head_node.run_tree_on_test_row(test_data_frame.iloc[x]) == "acc"
            if actual_pos and predict_pos:
                self.testing_result.true_positive += 1
            elif not actual_pos and not predict_pos:
                self.testing_result.true_negative += 1
            elif predict_pos:
                self.testing_result.false_positive += 1
            else:
                self.testing_result.false_negative += 1
            self.testing_result.tested_rows += 1

        return self.testing_result

    def create_plot(self,target_outputfile):
        from ete3 import Tree,TreeStyle,NodeStyle,faces,AttrFace,CircleFace,TextFace
        t=Tree()

        def layout(node):
            if node.is_leaf():
                N = AttrFace("name",  fgcolor="black")
                faces.add_face_to_node(N, node, 0)
            if "weight" in node.features:
                # Creates a sphere face whose size is proportional to node's
                # feature 1/gini index
                circle_face = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
                circle_face.hz_align=2
                circle_face.opacity = 0.3
                text_face = TextFace(text=node.name)
                faces.add_face_to_node(circle_face, node, 0, position="float")
                faces.add_face_to_node(text_face, node, 0, position="float")

        # Create an empty TreeStyle
        ts = TreeStyle()

        # Set our custom layout function
        ts.layout_fn = layout
        ts.scale = 140
        # # Draw a tree
        # ts.mode = "c"
        # We will add node names manually
        ts.show_leaf_name = False
        ts.branch_vertical_margin = 30
        ts.show_scale=False

        t= self.head_node.create_equivalent_ete_tree()

        t.render(target_outputfile, w=183, units="mm",tree_style=ts)

    def print(self):
        self.head_node.print_tree()