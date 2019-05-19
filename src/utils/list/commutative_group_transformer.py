# TODO: refactor

class CommutativeGroupTransformer:
    
    def transform(self, grouping_case, elements):
        if len(grouping_case) <= 0:
            return None
        return self.transform_rec(grouping_case, 0, grouping_case[0], elements, [], [])

    # TODO: refactor
    def transform_rec(self, join_case, current_index, quantity, not_gruped_elements, accum, total):

        if len(join_case) < current_index + 1:
            return [accum]

        if quantity == 0:
            new_index = current_index + 1
            new_quantity = 0
            if len(join_case) > current_index + 1:
                new_quantity = join_case[current_index + 1] 
            return self.transform_rec(join_case, new_index, new_quantity, not_gruped_elements, accum, total)

        amount_joined = current_index + 1

        combinations = self.combinations_of_n_elements(not_gruped_elements, amount_joined)

        for combination in combinations:
            accum_copy = accum[:]
            accum_copy.append(combination.elements)
            total += self.transform_rec(join_case, current_index, quantity - 1, combination.rest, accum_copy, [])
        
        return total


    # returns a list of SubCombination
    def combinations_of_n_elements(self, elements, n):
        return self.combinations_of_n_elements_rec(elements, elements,n,[],[])

    # TODO: REFACTOR!
    def combinations_of_n_elements_rec(self, elements, all_elements, n, accum, total):
        if n == 0:
            rest = []
            for elem in all_elements:
                if elem not in accum:
                    rest.append(elem)
            combination = SubCombination(accum, rest) 
            return [combination]

        for i in range(0, len(elements)):
            accum_copy = accum[:]
            elements_copy = elements[:]
            element = elements[i]
            for j in range(0, i + 1):
                elements_copy.remove(elements[j])
            accum_copy.append(element)
            total += self.combinations_of_n_elements_rec(elements_copy, all_elements, n-1, accum_copy, [])

        return total

class SubCombination:
    def __init__(self, elements, rest):
        self.elements = elements
        self.rest = rest
