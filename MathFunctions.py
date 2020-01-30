def create_binary_subsets(values_to_split):
    return_perms = []
    expectedperms = pow(2, len(values_to_split)) - 1
    binlength = len(bin(expectedperms)[2:])
    for a in range(0, expectedperms + 1):
        leftside = []
        rightside = []
        binstring = bin(a)[2:]
        while len(binstring) < binlength:
            binstring = "0" + binstring
        this_character_index = 0
        for this_character in binstring:
            if this_character == "0":
                leftside.append(values_to_split[this_character_index])
            else:
                rightside.append(values_to_split[this_character_index])
            this_character_index += 1
        if len(leftside) == 0 or len(rightside) == 0:
            pass
        else:
            return_perms.append((leftside, rightside))
    #     TODO this function is kinda gross and returns ((a,b),(c,d)) and ((c,d),(a,b)) as separate entries.
    return return_perms


def get_gini_score_of_single_list(target_list):
    assert len(set(target_list)) < 3
    assert len(target_list) > 0
    class_one_tally = 0
    class_two_tally = 0
    for single_item in target_list:
        if single_item == target_list[0]:
            class_one_tally += 1
        else:
            class_two_tally += 1
    list_size = len(target_list)
    gini_score = 1 - pow((class_one_tally / list_size), 2) - pow((class_two_tally / list_size), 2)
    return gini_score


def get_weighted_gini_score(target_lists):
    assert len(target_lists) > 1, "target list should have more than one sublist"
    combined_score = 0
    total_count = 0
    for single_list in target_lists:
        total_count += len(single_list)
    for single_list in target_lists:
        weighted_score = len(single_list) / total_count * get_gini_score_of_single_list(single_list)
        combined_score += weighted_score
    return combined_score


class split_possibility():
    def __init__(self, split_attr, subsets):
        self.split_attr = split_attr
        self.score = None
        self.subsets = subsets

def determine_best_split(dataframe, target, split_criteria='gini', possible_split_attributes=None):
    no_split_return = [None, None, None]
    # determine what rows can still be split.
    if not possible_split_attributes:
        possible_split_attributes = []
        for single_attr in dataframe.columns:
            possible_split_attributes.append(single_attr)
    if target in possible_split_attributes:
        possible_split_attributes.remove(target)
    for single_attribute in possible_split_attributes:
        if len(dataframe[single_attribute].unique()) == 0:
            possible_split_attributes.remove(single_attribute)

    # if no splits possible, return
    if len(possible_split_attributes) == 0:
        return no_split_return
    if len(dataframe[target].unique()) == 1:
        return no_split_return

    test_iterations = []
    for single_attr in possible_split_attributes:
        unique_vals = dataframe[single_attr].unique()
        if len(unique_vals) > 1:
            for single_combination in create_binary_subsets(unique_vals):
                test_iterations.append(split_possibility(single_attr, single_combination))

    if len(test_iterations) == 0:
        return no_split_return

    # Below actually does the split--- split method could be changed when implementing entropy/etc.
    best_score = {"score": 1, "test_result": None}
    test_results = []
    for single_test in test_iterations:
        targetlists = []

        for single_subset in single_test.subsets:
            targetlists.append(dataframe.loc[dataframe[single_test.split_attr].isin(single_subset)][target].values)

        single_test.score = get_weighted_gini_score(targetlists)
        test_results.append(single_test)
        if single_test.score < best_score["score"]:
            best_score["score"] = single_test.score
            best_score["test_result"] = single_test

    if best_score["score"] == 1:
        return no_split_return
    else:
        return [best_score["test_result"].split_attr, best_score["test_result"].subsets,
                best_score["test_result"].score]
