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
    def combinations_rec(listone, listtwo, combination, combinations):
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

            combinations = ListUtils.combinations_rec(listone_without_first, listtwo_without_elem, combination_bifurcation, combinations)

        return combinations

    @staticmethod
    def combinations_diferent_sizes(listone, listtwo):
        if len(listone) > len(listtwo):
            larger = listone
            smaller = listtwo
        else:
            larger = listtwo
            smaller = listone

        return ListUtils.combinations_diferent_sizes_rec(larger, smaller)

    # Idea:
    # A = [a,b] ; B = [1,2,3,4]
    # diff = 2
    # Possibles: 
    # 1. join 2 sets of 2 elements of B to reduce its size
    # 2. join 1 set of 3 elements of B to reduce its size

    @staticmethod
    def combinations_diferent_sizes_rec(larger, smaller, possibilities):
        diff = len(larger) - len(smaller)
        
        # Each item is an array of numbers representing the amount of items of that length joined
        # for example with a difference in length of 4 and the length of the smaller 2
        # [0,2,0,0] a possible reduction is 0 elements of lenght 1; two elements of length 2; etc..
        join_possibilities = possibilities
        
            
    # TODO: logic
    @staticmethod
    def get_list_of_joins(smaller_size, larger_size):
        pass
    

    # TODO: refactor
    @staticmethod
    def compute_rec(amount_joined, rest_size, expected_amount, accum, total):
        if amount_joined == 0:
            sum = 0
            for item in accum:
                sum += item
            if rest_size == 0 and sum == expected_amount:
                return [accum]
            return []
        
        if (rest_size < amount_joined ):
            accum_copy = accum[:]
            accum_copy.append(0)
            return ListUtils.compute_rec(amount_joined - 1, rest_size, expected_amount, accum_copy, total)

        max_amount_of_joins = int (rest_size / amount_joined)
        for i in range(0, max_amount_of_joins + 1):
            accum_copy = accum[:]
            accum_copy.append(i)
            
            total += ListUtils.compute_rec(amount_joined - 1, rest_size - (i * amount_joined), expected_amount, accum_copy, [])
        
        return total