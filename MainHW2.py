from DecisionTreeStructures import Model,Model_Test_Result,DataSet

# Create model and print output
hw2Model = Model(training_path="car.training.csv",target_attribute="class")
hw2Model.print()
hw2Model.create_plot("hw2plot.pdf")

# Create testing dataframe
test_data_set = DataSet()
test_data_set.load_data_from_file("car.test.csv")

# Test model against testing data frame and print result
test_result = hw2Model.test_model(test_data_set.data_frame)
test_result.print()
