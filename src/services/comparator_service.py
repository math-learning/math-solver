from sympy import simplify

from src.comparators.comparator_utils import ComparatorUtils
from src.comparators.comparison_result import ComparisonResult
from src.comparators.user_defined_function_comparator import UserDefinedFunctionComparator
from src.model.theorem import Theorem
from src.model.history_item import HistoryItem
from src.model.transformation_result import TransformationResult
from src.services.derivative_service import DerivativeApplier
from src.transformers.expression_transformer import ExpressionTransformer
from src.utils.logger import Logger


class ComparatorService:

    def __init__(self):
        self.expression_transformer = ExpressionTransformer()
        self.comparator_utils = ComparatorUtils()
        self.user_defined_func_comparator = UserDefinedFunctionComparator()
        self.derivatives_applier = DerivativeApplier()
        self.logger = Logger.getLogger()

    def get_solution_if_possible(self, input_data, theorems):
        self.logger.info("Trying to solve the problem of input {} using the following theorems {}".format(input_data, theorems))
        solved = False
        history = []
        current_step = input_data
        while not solved:
            # Try to apply theorems to the expression
            next_possible_step = self.get_possible_new_step(current_step, theorems, history)
            if current_step != next_possible_step.expression:
                self.logger.info("Applying theorem to the general structure. Applying {} to {} getting {}".format(next_possible_step.theorem_used.name, current_step, next_possible_step.expression))
                history.append(HistoryItem(next_possible_step.expression, next_possible_step.theorem_used))
                current_step = next_possible_step.expression
            else:
                # Try to apply theorems to children nodes
                expression_changed = False
                for arg in current_step.args:
                    children_history = self.get_solution_if_possible(arg, theorems)
                    for history_item in children_history:
                        equalities = [[arg,history_item.expression]]
                        new_step = self.expression_transformer.transform(current_step, equalities)
                        self.logger.info("Applying theorem to the children nodes. Applying {} to {} getting {}".format(history_item.theorem_applied.name, current_step, new_step))
                        history.append(HistoryItem(new_step, history_item.theorem_applied))
                    if len(history) != 0:
                        current_step = history[-1].expression
                        expression_changed = True

                # Try applying derivatives
                if not expression_changed:
                    new_step = self.derivatives_applier.apply_derivatives(current_step)
                    if new_step != current_step:
                        expression_changed = True
                        self.logger.info("Applying theorem to the children nodes. Applying {} to {} getting {}".format("Aplicacion de derivadas", current_step, new_step))
                        history.append(HistoryItem(new_step, Theorem("Aplicacion de derivadas", "-", "-")))
                        current_step = new_step
                
                # Try with simplifications
                if not expression_changed:
                    new_step = simplify(current_step)
                    if new_step != current_step:
                        expression_changed = True
                        self.logger.info("Applying theorem to the children nodes. Applying {} to {} getting {}".format("Simplificaciones", current_step, new_step))
                        history.append(HistoryItem(new_step, Theorem("Simplificacion", "-", "-")))
                        current_step = new_step
                
                if not expression_changed:
                    solved = True

        return history

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
