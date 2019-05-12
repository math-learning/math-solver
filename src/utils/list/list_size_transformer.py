# TODO: REFACTOR

class ListSizeTransformer:

    def __init__(self, group_case_transformer):
        self.group_case_transformer = group_case_transformer

    # Idea:
    # A = [a,b] ; B = [1,2,3,4]
    # diff = 2
    # Possibles: 
    # 1. join 2 sets of 2 elements of B to reduce its size
    # 2. join 1 set of 3 elements of B to reduce its size
    def transform(self, listone, new_size):
        
        listone_length = len(listone)

        if listone_length < new_size:
            #TODO: handle
            return None
        smaller, larger = new_size, listone_length

        # Each item is an array of numbers representing the amount of items of that length joined
        # for example with a difference in length of 4 and the length of the smaller 2
        # [0,2,0,0] a possible reduction is 0 elements of lenght 1; two elements of length 2; etc..
        grouping_possibilities = self.amount_of_groups_by_group_elements_number(smaller, larger)
        
        combinations = []

        for grouping_case in grouping_possibilities:
            # larger reduced cases are the combinations of for example [1,0,1]
            # combination of indices of elements that form an array that contains 1 list of size 1
            # and another of size 3
            larger_reduced_cases = self.group_case_transformer.transform(grouping_case, listone)
            for single_case in larger_reduced_cases:
                combinations.append(single_case)

        return combinations
        
    
    def amount_of_groups_by_group_elements_number(self, smaller_size, larger_size):
        diff = larger_size - smaller_size
        return self.amount_of_groups_by_group_elements_number_rec(diff + 1, larger_size, smaller_size, [], [])
    
    def amount_of_groups_by_group_elements_number_rec(self, amount_to_group, not_grouped_amount, expected_amount, accum, result):
        
        if amount_to_group == 0:
            return self.get_grouping_info_if_valid(accum, not_grouped_amount, expected_amount)
        
        if (not_grouped_amount < amount_to_group ):
            new_accum = self.add_grouping_info(0, amount_to_group, accum)
            return self.amount_of_groups_by_group_elements_number_rec(amount_to_group - 1, not_grouped_amount, expected_amount, new_accum, result)

        max_amount_of_groups = int (not_grouped_amount / amount_to_group) + 1

        for i in range(0, max_amount_of_groups):
            new_accum = self.add_grouping_info(i, amount_to_group, accum)
            result += self.amount_of_groups_by_group_elements_number_rec(amount_to_group - 1, not_grouped_amount - (i * amount_to_group), expected_amount, new_accum, [])
        
        return result

    def get_grouping_info_if_valid(self, accum, not_grouped_amount, expected_amount):
        sum = 0
        for item in accum:
            sum += item
        if not_grouped_amount != 0 or sum != expected_amount:
            return []
        accum.reverse()
        return [accum]

    def add_grouping_info(self, amount, amount_to_group, accum):
        new_accum = accum[:]
        new_accum.append(amount)
        return new_accum


    

