from src.comparators.ComparatorUtils import ComparatorUtils
from src.comparators.ComparisonResult import ComparisonResult
from src.comparators.SympyComparator import SympyComparator
from src.comparators.UserDefinedFunctionComparator import UserDefinedFunctionComparator
from src.model.HistoryItem import HistoryItem
from src.services.DerivativesService import DerivativeApplier
from src.model.TransformationResult import TransformationResult
from src.transformers.ExpressionTransformer import ExpressionTransformer
from sympy import simplify


class ComparatorService:

    def __init__(self):
        self.sympy_comparator = SympyComparator()
        self.expression_transformer = ExpressionTransformer()
        self.comparator_utils = ComparatorUtils()
        self.user_defined_func_comparator = UserDefinedFunctionComparator()
        self.derivatives_applier = DerivativeApplier()

    def get_solution_if_possible(self, input, theorems):
        solved = False
        history = []
        current_step = input
        while not solved:
            next_possible_step = self.get_possible_new_step(current_step, theorems, history)
            if current_step != next_possible_step.expression:
                history.append(HistoryItem(next_possible_step.expression, next_possible_step.theorem_used))
                current_step = next_possible_step.expression
            else:
                for arg in current_step.args:
                    children_history = self.get_solution_if_possible(arg, theorems)
                    for history_item in children_history:
                        equalities = [[arg,history_item.expression]]
                        new_step = self.expression_transformer.transform(current_step, equalities)
                        history.append(HistoryItem(new_step, history_item.theorem_applied))
                    if len(history) != 0:
                        current_step = history[-1].expression
                break
        return history

    def compare_equality(self, old_expression, new_expression, theorems):
        # Try with theorems
        for theo in theorems:
            comparison = self.compare(theo.left, old_expression)
            if comparison.structures_match:
                new_step = self.expression_transformer.transform(theo.right, comparison.equalities)
                if new_step == simplify(new_expression):
                    return True

        if new_expression != old_expression:
            # Try applying derivatives:
            new_step = self.derivatives_applier.apply_derivatives(old_expression)
            if new_step == simplify(new_expression):
                return True
            
            # Try simplifying
            if simplify(new_expression) == simplify(old_expression):
                return True

        return False

    def get_possible_new_step(self, expression, theorems, history):
        for theo in theorems:
            comparison = self.compare(theo.left, expression)
            if comparison.structures_match:
                new_step = self.expression_transformer.transform(theo.right, comparison.equalities)
                if new_step not in history:
                    return TransformationResult(new_step, theo)
        return TransformationResult(expression, None)

    def compare(self, structure, expression):
        return self.compare_rec(structure, expression, [])

    def compare_rec(self, structure, expression, equalities):
        if self.comparator_utils.both_nodes_are_leaves(structure, expression):
            return ComparisonResult(structure == expression, equalities)

        if self.user_defined_func_comparator.is_user_defined_function(structure):
            return self.user_defined_func_comparator.compare(structure, expression, equalities)

        if len(structure.args) == len(expression.args):
            return self.compare_sympy_expression(structure, expression, equalities)

        return self.compare_non_equal_lengths(structure, expression, equalities)

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

    def compare_children_combinations(self, children_pairs, equalities):
        result = ComparisonResult(True, [])
        for pair in children_pairs:
            children_comparison_result = self.compare_rec(pair.structure_child, pair.expression_child, equalities)
            result.structures_match &= children_comparison_result.structures_match
            result.equalities += children_comparison_result.equalities
        return result


    def compare_non_equal_lengths(self, structure, expression, equalities):
        # if at least one is a user defined function we have to group arguments to see if matches
        contains_user_defined_function = self.user_defined_func_comparator.contains_user_defined_function(structure)
        if len(structure.args) < len(expression.args) and contains_user_defined_function:
            if structure.func.is_commutative:
                # TODO: complex logic
                print(expression.func(*expression.args))

            return ComparisonResult(False, [])
        return ComparisonResult(False, [])










