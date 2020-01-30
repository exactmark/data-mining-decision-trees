from unittest import TestCase
from DecisionTreeStructures import DataSet


class TestDataSet(TestCase):
    def test_load_car_data_from_file(self):
        new_dataset = DataSet()
        new_dataset.load_data_from_file("car.unittest.csv")
        assert "class" in new_dataset.columnmap
        assert len(new_dataset.data_frame[new_dataset.data_frame.buying == "vhigh"])==3,"Data frame did not read data"
        # print(new_dataset.data_frame[(new_dataset.data_frame.buying == "vhigh") & (new_dataset.data_frame.maint=="low")])
        # print(new_dataset.data_frame[(new_dataset.data_frame.buying == "vhigh") & (new_dataset.data_frame.maint=="low")])

    def test_add_node_column(self):
        new_dataset = DataSet()
        new_dataset.load_data_from_file("car.unittest.csv")
        # print(new_dataset.data_frame[new_dataset.data_frame.buying == "vhigh"])

