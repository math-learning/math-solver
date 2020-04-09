from mathlearning.model.theorem import Theorem
from mathlearning.utils.logger import Logger
from mathlearning.model.expression import Expression
from typing import List

logger = Logger.getLogger()


class SolutionTreeNode:
    def __init__(self, expression: Expression, theorem_applied: Theorem, branches: List):
        self.expression = expression
        self.theorem_applied = theorem_applied
        self.branches = branches

    def explain_solution(self, profundidad):
        theorem = "None"
        if self.theorem_applied is not None:
            theorem = self.theorem_applied.name
        print(profundidad, ". Expression: " + self.expression.to_string(), ". Teorema aplicado: " + theorem)

        for branch in self.branches:
            branch.explain_solution(profundidad + 1)

    def apply_derivatives_to_leaves(self):
        logger.info("Trying to  apply derivatives to leaves")
        if len(self.branches) == 0:
            branches = []
            derivatives_solving_possibilities = self.expression.derivatives_solving_possibilities()
            for possibility in derivatives_solving_possibilities:
                if not possibility.is_equivalent_to(self.expression):
                    branch = SolutionTreeNode(possibility, Theorem('resolver derivadas', None, None, []),[])
                    branch.apply_derivatives_to_leaves()
                    branches.append(branch)
            self.branches = branches
        else:
            for branch in self.branches:
                branch.apply_derivatives_to_leaves()

    def to_latex(self):
        self.expression = self.expression.to_latex()
        for branch in self.branches:
            branch.to_latex()

    def to_json(self):
        branches = []
        for branch in self.branches:
            branches.append(branch.to_json())

        if self.theorem_applied is not None:
            theorem = self.theorem_applied.to_json()
        else:
            theorem = {'name': 'none'}

        return {
            'expression': self.expression.to_string(),
            'theorem_applied': theorem,
            'branches': branches
        }

    def get_theorem_names(self):
        names = self.get_theorem_names_rec(set())
        names.discard('none')
        return names

    def get_theorem_names_rec(self, accum):
        if self.theorem_applied is not None:
            accum.add(self.theorem_applied.name)
        children_names = set()
        for branch in self.branches:
            children_names |= branch.get_theorem_names_rec(set())
        accum |= children_names
        return accum

    def __str__(self):
        return self.expression.to_string() + str(self.theorem_applied)

    def validate_new_expression(self, current_expression, new_expression):
        subtree_possibilities = self.get_sub_tree_with_root(current_expression)
        for subtree in subtree_possibilities:
            if subtree.contains(new_expression):
                if subtree.is_a_result(new_expression):
                    return 'resolved'
                return 'valid'
        return 'invalid'

    def get_hints(self, current_expression):
        possible_subrees = self.get_sub_tree_with_root(current_expression)
        hints = []
        for subtree in possible_subrees:
            for children in subtree.get_children():
                hints.append(children.theorem_applied)
        return hints

    def get_sub_tree_with_root(self, current_expression):
        if self.expression.is_equivalent_to(current_expression):
            return [self]
        if len(self.branches) == 0:
            return []
        accum = []
        for branch in self.branches:
            accum += branch.get_sub_tree_with_root(current_expression)
        return accum

    def contains(self, expression):
        to_check = [self]
        while len(to_check) > 0:
            current = to_check.pop()
            if current.expression.is_equivalent_to(expression):
                return True
            for branch in current.branches:
                to_check.append(branch)
        return False

    def is_pre_simplification_step(self):
        if len(self.branches) == 1:
            branch = self.branches[0]
            if branch.theorem_applied.name == 'simplificacion' and len(branch.branches) == 0:
                return True
        return False

    def is_a_result(self, expression):
        to_check = [self]
        leaves_and_pre_simplification = []
        while len(to_check) > 0:
            current = to_check.pop()
            if current.is_pre_simplification_step():
                return leaves_and_pre_simplification.append(current)
            elif len(current.branches) > 0:
                for branch in current.branches:
                    to_check.append(branch)
            else:
                leaves_and_pre_simplification.append(current)

        for leave in leaves_and_pre_simplification:
            if leave.expression.is_equivalent_to(expression):
                return True

        return False
