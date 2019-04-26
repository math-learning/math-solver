from server.src.utils.list_utils import ListUtils


class Equality:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ComparisonPair:
    def __init__(self, structure_child, expression_child):
        self.structure_child = structure_child
        self.expression_child = expression_child


class TemplateExpression:

    def __init__(self, formula):
        self.expression = Expression(formula)

    def match(self):
        



class TemplateComparator:
    def __init__(self):
        pass
    
    def match(self, template, expression):
        return self.match_rec(template, expression)

    def match_rec(self, template, expression):
        if not template.contains_user_defined_funct() and not expression.contains_user_defined_funct():
            return template.compare(expression)

        if template.is_user_defined_func():
            return template.free_symbols_match(expression)
        
        if template.children_amount() == expression.children_amount():
            return self.compare_exp_with_user_def_func_eq_sizes(template, expression)
        
        return self.compare_exp_with_user_def_func_diff_sizes(template, expression)


    def compare_exp_with_user_def_func_eq_sizes(template, expression):
        if structure.func == expression.func:
                 if structure.is_commutative:
                     # print("is cummulative")
                     pairs_to_compare = ListUtils.get
                     .get_children_pairs(structure.args, expression.args)
                     for children_pairs in pairs_to_compare:
                         comparison = self.compare_children_combinations(children_pairs, equalities)
                         if comparison.structures_match:
                             return comparison
                 else:
                     # print("comparing non commutative")
                     pairs_to_compare = self.comparator_utils.get_equivalent_children_pairs(len(structure), structure.args, expression.args)
                     return self.compare_children_combinations(pairs_to_compare, equalities)
         return ComparisonResult(False, [])

     def compare_sympy_expression(self, structure, expression, equalities):
         if structure.func == expression.func:
                 if structure.is_commutative:
                     # print("is cummulative")
                     pairs_to_compare = self.comparator_utils.get_children_pairs(structure.args, expression.args)
                     for children_pairs in pairs_to_compare:
                         comparison = self.compare_children_combinations(children_pairs, equalities)
                         if comparison.structures_match:
                             return comparison
                 else:
                     # print("comparing non commutative")
                     pairs_to_compare = self.comparator_utils.get_equivalent_children_pairs(len(structure), structure.args, expression.args)
                     return self.compare_children_combinations(pairs_to_compare, equalities)
         return ComparisonResult(False, [])

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
