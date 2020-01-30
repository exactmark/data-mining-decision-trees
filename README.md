# data-mining-decision-trees
An implementation of a simple decision tree algorithm from a Big Data course.

##Implementation
DecisionTreeStructures includes classes needed to create a simple decision tree model, while MathFunctions includes functions that are required to create the model (but may also be potentially stand alone).  
DecisionTreeStructures consists of three important classes:  
1. My Dataset class will take a given csv and convert it to a pandas DataFrame.  Pandas allows python users to make some r-style DataFrame queries and is relatively quick.  
2. My Model class will take a given DataFrame and create a decision tree consisting of Nodes.  
3. The Node class makes up the pieces of the actual decision tree.  Each contains a slice of the original pandas DataFrame.  Each node class will call the appropriate functions in MathFunctions to determine the correct data split, then create subnodes as appropriate.  There are currently obvious hooks to improves the implementation, by adding trinary splits or using a different decision method than Gini index.  

MathFunctions consists of a set of relatively agnostic functions.  These depend on knowledge of pandas DataFrames, but nothing else.  These are relatively straightforward--- determine_best_split takes a dataframe and a target, and will send back a tuple of the best split attribute, the appropriate split, and the corresponding gini score.  determine_best_split calls create_binary_subsets to create the possible splits, then get_weighted_gini_score takes a set of lists of the class attribute, as split by the attribute/value pairs.  

The tree visualization uses the ete3 library.

In all cases, I have attempted to keep clean code in mind, including proper function and variable names, as well as sufficient decoupling between the data structures and the functional methods.

##Possible Improvements and Optimizations
The MathFunctions section could be improved.  I created my own function to create binary subsets, and it will return equivalent lists in varying order--- that is ((a,b),(c)) and ((c),(a,b)).  This will lead to much more work being done by determine_best_split.  However, as this dataset is relatively small, the optimization here can wait.  
I am treating all attributes as non-ordinal.  While some attributes have obvious ordering (low,med,high) it is currently being ignored.  This would need to be addressed if I wanted to continue this project further.  However, with this dataset, accuracy seems to be acceptable.

