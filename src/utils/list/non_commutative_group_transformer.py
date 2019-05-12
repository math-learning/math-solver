class NonCommutativeSubCombination:
    def __init__(self, left_rest, elements, right_rest):
        self.left_rest = left_rest
        self.elements = elements
        self.right_rest = right_rest

#TODO: REFACTOR

# combine index i only with i + 1 or i - 1
class NonCommutativeGroupTransformer:

    def transform(self, grouping_case, elements):
        pass

    def transform_rec(self, grouping_case, current_index, quantity, not_gruped_elements_list, accum, total):
        
        if len(join_case) < current_index + 1:
            return [accum]

        if quantity == 0:
            new_index = current_index + 1
            new_quantity = 0
            if len(join_case) > current_index + 1:
                new_quantity = join_case[current_index + 1] 
            return self.transform_rec(join_case, new_index, new_quantity, not_gruped_elements, accum, total)

        amount_joined = current_index + 1

        for not_grouped_elements in not_gruped_elements_list
            combinations = self.combinations_of_n_elements(not_gruped_elements, amount_joined)
        
        # TODO: complex logic
            

    def combinations_of_n_elements(self, elements, n, accum, total):
        if n > len(elements):
            return None
        
        result = []
        for i in range(0, len(elements) - n + 1):

            left_elements = elements[:i]
            sub_elements = elements[i:i+n]    
            right_elements = [i+n:]
            
            result.append(NonCommutativeSubCombination(left_elements, sub_elements, right_elements))
        
        return result

