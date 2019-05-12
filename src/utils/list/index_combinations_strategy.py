# TODO: refactor

class IndexCombinationStrategy:
    
    # returns a list of SubCombination
    def combinations_of_n_elements(self, elements, n):
        return self.combinations_of_n_elements_rec(elements, elements,n,[],[])

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
