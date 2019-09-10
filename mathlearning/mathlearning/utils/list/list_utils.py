
# DIVIDE 
class ListUtils:

    # get the posibles combinations where every element
    # of a is paired with one with b
    # ex: a = [1, 2] ; b = [3, 4] returns [[[1,3],[2,4]],[[1,4],[2,3]]]
    # lengths should be equal
    @staticmethod
    def pair_combinations(lista, listb):
        if len(lista) != len(listb):
            return None
        return ListUtils.pair_combinations_rec(lista, listb, [], [])
        
    # Idea a = [1,2, 3] ; b = [4, 5, 6]
    # every element of b is paired with the first element of a
    # [1,4] , [1,5] , [1,6]
    # and then the function is recursively called with the lists without those elements
    # until the solution is found
    @staticmethod
    def pair_combinations_rec(listone, listtwo, combination, combinations):
        if len(listone) == 1 and len(listtwo) == 1:
            combination.append([listone[0], listtwo[0]])
            combinations.append(combination)
            return combinations

        for elem in listtwo:
            combination_bifurcation = combination[:]
            combination_bifurcation.append([listone[0], elem])
            
            listone_without_first = listone[1:]

            listtwo_without_elem = list(listtwo[:])
            listtwo_without_elem.remove(elem)
            listtwo_without_elem = tuple(listtwo_without_elem)

            combinations = ListUtils.pair_combinations_rec(listone_without_first, listtwo_without_elem, combination_bifurcation, combinations)

        return combinations
