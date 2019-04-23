class Equality:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ComparisonPair:
    def __init__(self, structure_child, expression_child):
        self.structure_child = structure_child
        self.expression_child = expression_child

class Expressions:

    # Pair the first, second, ... node of both expressions together.
    def get_equivalent_children_pairs(self, length, structure_children, expression_children):
        comparison_pairs = []
        for i in range(0, length):
            comparison_pairs .append(ComparisonPair(structure_children[i], expression_children[i]))
        return comparison_pairs

    def get_children_pairs(self, structure_children, expression_children):
        return self.get_children_pairs_rec(structure_children, expression_children, [], [])

    # get the possible combinations of expression ren and structure children that can be compared.
    def get_children_pairs_rec(self, structure_children, expression_children, accum, possibles):
        if len(structure_children) == 1 and len(expression_children) == 1:
            accum.append(ComparisonPair(structure_children[0], expression_children[0]))
            possibles.append(accum)
            return possibles

        # TODO: RENAME
        for expression_child in expression_children:
            new_accum = accum[:]
            new_accum.append(ComparisonPair(structure_children[0], expression_child))
            structure_children_without_first = structure_children[1:]
            expression_children_without_child = list(expression_children[:])
            expression_children_without_child.remove(expression_child)
            expression_children_without_child = tuple(expression_children_without_child)
            possibles = self.get_children_pairs_rec(structure_children_without_first, expression_children_without_child, new_accum, possibles)

        return possibles



class TemplateComparator:
    def __init__(self):
        pass
    
    def match(self, template, expression):
        return self.match_rec(template, expression)

    def match_rec(self, template, expression):
        if template.is_leaf() and expression.is_leaf():
            return template.compare(expression)

        if template.is_user_defined_func():
            return template.free_symbols_match(expression)

    #     if template.children_amount() == expression.children_amount():
    #         return self.compare_sympy_expression(structure, expression, equalities)

    #     return self.compare_non_equal_lengths(structure, expression, equalities)

    # def compare_sympy_expression(self, structure, expression, equalities):
    #     if structure.func == expression.func:
    #             if structure.is_commutative:
    #                 # print("is cummulative")
    #                 pairs_to_compare = self.comparator_utils.get_children_pairs(structure.args, expression.args)
    #                 for children_pairs in pairs_to_compare:
    #                     comparison = self.compare_children_combinations(children_pairs, equalities)
    #                     if comparison.structures_match:
    #                         return comparison
    #             else:
    #                 # print("comparing non commutative")
    #                 pairs_to_compare = self.comparator_utils.get_equivalent_children_pairs(len(structure), structure.args, expression.args)
    #                 return self.compare_children_combinations(pairs_to_compare, equalities)
    #     return ComparisonResult(False, [])

    # def compare_children_combinations(self, children_pairs, equalities):
    #     result = ComparisonResult(True, [])
    #     for pair in children_pairs:
    #         children_comparison_result = self.compare_rec(pair.structure_child, pair.expression_child, equalities)
    #         result.structures_match &= children_comparison_result.structures_match
    #         result.equalities += children_comparison_result.equalities
    #     return result


    # def compare_non_equal_lengths(self, structure, expression, equalities):
    #     # if at least one is a user defined function we have to group arguments to see if matches
    #     contains_user_defined_function = self.user_defined_func_comparator.contains_user_defined_function(structure)
    #     if len(structure.args) < len(expression.args) and contains_user_defined_function:
    #         if structure.func.is_commutative:
    #             # TODO: complex logic
    #             print(expression.func(*expression.args))

    #         return ComparisonResult(False, [])
    #     return ComparisonResult(False, [])
