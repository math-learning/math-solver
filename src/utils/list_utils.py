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

        return ListUtils.combinations_diferent_sizes_rec(larger, smaller, [])

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
        join_possibilities = ListUtils.get_list_of_joins(len(smaller), len(larger))
        
        for join_case in join_possibilities:
            
            for quantity in join_case:
                amount_joined = join_case.index(quantity) + 1

                for i in range(0, quantity):
                    combinations = ListUtils.combinations_of_n_elem(larger, amount_joined)


                    


    # TODO: refactor
    @staticmethod
    def calculate_rec(join_case, current_index, quantity, rest, accum, total):

        if len(join_case) < current_index + 1:
            return [accum]

        if quantity == 0:
            new_index = current_index + 1
            new_quantity = 0
            if len(join_case) > current_index + 1:
                new_quantity = join_case[current_index + 1] 
            return ListUtils.calculate_rec(join_case, new_index, new_quantity, rest, accum, total)

        amount_joined = current_index + 1

        combinations = ListUtils.combinations_of_n_elem(rest, amount_joined)
        for combination in combinations:
            accum_copy = accum[:]
            accum_copy.append(combination.elements)
            total += ListUtils.calculate_rec(join_case, current_index, quantity - 1, combination.rest, accum_copy, [])
        
        return total

    @staticmethod
    def combinations_of_n_elem(elements, n):
        return ListUtils.combinations_of_n_elem_rec(elements, elements,n,[],[])

    @staticmethod
    def combinations_of_n_elem_rec(elements, all_elements, n, accum, total):
        
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
            total += ListUtils.combinations_of_n_elem_rec(elements_copy, all_elements, n-1, accum_copy, [])

        return total

        

            
    # TODO: logic
    @staticmethod
    def get_list_of_joins(smaller_size, larger_size):
        diff = larger_size - smaller_size
        return ListUtils.list_of_joins_rec(diff + 1, larger_size, smaller_size, [], [])
    

    # TODO: refactor
    @staticmethod
    def list_of_joins_rec(amount_joined, rest_size, expected_amount, accum, total):
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
            return ListUtils.list_of_joins_rec(amount_joined - 1, rest_size, expected_amount, accum_copy, total)

        max_amount_of_joins = int (rest_size / amount_joined)
        for i in range(0, max_amount_of_joins + 1):
            accum_copy = accum[:]
            accum_copy.append(i)
            
            total += ListUtils.list_of_joins_rec(amount_joined - 1, rest_size - (i * amount_joined), expected_amount, accum_copy, [])
        
        return total

class SubCombination:
        def __init__(self, elements, rest):
            self.elements = elements
            self.rest = rest