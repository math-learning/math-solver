class NonCommutativeSubCombination:
    def __init__(self, left_rest, elements, right_rest):
        self.left_rest = left_rest
        self.elements = elements
        self.right_rest = right_rest


# TODO: REFACTOR

# combine index i only with i + 1 or i - 1
class NonCommutativeGroupTransformer:

    def transform(self, grouping_case, elements):
        return self.transform_rec(grouping_case, 0, grouping_case[0], [elements], [], [])

    def transform_rec(self, grouping_case, current_index, quantity, not_grouped_elements_list, accum, total):

        if len(grouping_case) < current_index + 1:
            return [accum]

        if quantity == 0:
            new_index = current_index + 1
            new_quantity = 0
            if len(grouping_case) > current_index + 1:
                new_quantity = grouping_case[current_index + 1]
            return self.transform_rec(grouping_case, new_index, new_quantity, not_grouped_elements_list, accum, total)

        amount_joined = current_index + 1

        for not_grouped_elements in not_grouped_elements_list:
            combinations = self.combinations_of_n_elements(not_grouped_elements, amount_joined)
            if combinations != None:
                for combination in combinations:
                    not_grouped_elements_list_copy = not_grouped_elements_list[:]
                    not_grouped_elements_list_copy.remove(not_grouped_elements)

                    if len(combination.left_rest) != 0:
                        not_grouped_elements_list_copy.append(combination.left_rest)
                    if len(combination.right_rest) != 0:
                        not_grouped_elements_list_copy.append(combination.right_rest)

                    accum_copy = accum[:]
                    accum_copy.append(combination.elements)

                    a_result = self.transform_rec(grouping_case, current_index, quantity - 1,
                                                  not_grouped_elements_list_copy, accum_copy, [])
                    if a_result != None:
                        total += a_result

        return total

        # TODO: complex logic

    def combinations_of_n_elements(self, elements, n):
        if n > len(elements):
            return None

        result = []
        for i in range(0, len(elements) - n + 1):
            left_elements = elements[:i]
            sub_elements = elements[i:i + n]
            right_elements = elements[i + n:]

            result.append(NonCommutativeSubCombination(left_elements, sub_elements, right_elements))

        return result
