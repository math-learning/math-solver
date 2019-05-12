from src.utils.list.index_combinations_strategy import SubCombination

#TODO: REFACTOR

# combine index i only with i + 1 or i - 1
class OnlyContinuousIndexCombinationStrategy:

    def combinations_of_n_elements(self, elements, n):
        result = []
        for i in range(0, len(elements) - n + 1):
            sub_elements = []
            for j in range(i, i + n):
                sub_elements.append(elements[j])
            rest = []
            for elem in elements:
                if elem not in sub_elements:
                    rest.append(elem)
            subcombination = SubCombination(sub_elements, rest)
            result.append( subcombination)
        return result