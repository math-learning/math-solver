class ListUtils:

    # get the posibles combinations where every element
    # of a is paired with one with b
    # ex: a = [1, 2] ; b = [3, 4] returns [[[1,3],[2,4]],[[1,4],[2,3]]]
    # lengths should be equal
    @staticmethod
    def combinations(lista, listb):
        if len(lista) != len(listb):
            return None
        return ListUtils.combinations_rec(lista, listb, [], [])
        
    # Idea a = [1,2, 3] ; b = [4, 5, 6]
    # every element of b is paired with the first element of a
    # [1,4] , [1,5] , [1,6]
    # and then the function is recursively called with the lists without those elements
    # until the solution is found
    @staticmethod
    def combinations_rec(lista, listb, combination, combinations):
        if len(lista) == 1 and len(listb) == 1:
            combination.append([lista[0], listb[0]])
            combinations.append(combination)
            return combinations

        for elem in listb:
            combination_bifurcation = combination[:]
            combination_bifurcation.append([lista[0], elem])
            
            lista_without_first = lista[1:]

            listb_without_elem = list(listb[:])
            listb_without_elem.remove(elem)
            listb_without_elem = tuple(listb_without_elem)

            combinations = ListUtils.combinations_rec(lista_without_first, listb_without_elem, combination_bifurcation, combinations)

        return combinations