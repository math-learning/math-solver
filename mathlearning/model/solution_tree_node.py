from mathlearning.model.theorem import Theorem
from mathlearning.utils.logger import Logger
from mathlearning.model.expression import Expression
from typing import List

logger = Logger.getLogger()

class SolutionTreeNode:
    def __init__(self, expression: Expression, theorem_applied_name: str, branches: List):
        self.expression = expression
        self.theorem_applied_name = theorem_applied_name
        self.branches = branches

    def explain_solution(self, depth):
        theorem = "None"
        if self.theorem_applied_name is not None:
            theorem = self.theorem_applied_name
        print(depth, ". Expression: " + self.expression.to_string(), ". Teorema aplicado: " + theorem)

        for branch in self.branches:
            branch.explain_solution(depth + 1)

    def to_latex(self):
        self.expression = self.expression.to_latex()
        for branch in self.branches:
            branch.to_latex()

    def to_json(self):
        branches = []
        for branch in self.branches:
            branches.append(branch.to_json())

        if self.theorem_applied_name is not None:
            theorem = self.theorem_applied_name
        else:
            theorem = 'none'

        return {
            'expression': self.expression.to_string(),
            'theorem_applied_name': theorem,
            'branches': branches
        }

    def get_theorem_names(self):
        names = self.get_theorem_names_rec(set())
        names.discard('none')
        return names

    def get_theorem_names_rec(self, accum):
        accum.add(self.theorem_applied_name)
        children_names = set()
        for branch in self.branches:
            children_names |= branch.get_theorem_names_rec(set())
        accum |= children_names
        return accum

    def __str__(self):
        return self.expression.to_string() + self.theorem_applied_name

    def new_expression_is_valid(self, previous_step, new_expression):
        # TODO: fix going backwards bug
        return self.contains(new_expression)

    def validate_new_expression(self, new_expression, previous_step):
        hints = []
        is_valid = self.new_expression_is_valid(previous_step, new_expression)

        if not is_valid:
            hints = self.get_hints(previous_step)
            return 'invalid', hints
        if self.is_a_result(new_expression):
            return 'resolved', hints

        hints = self.get_hints(new_expression)
        return 'valid', hints

    def get_hints(self, current_expression) -> List[str]:
        current_expression_subtrees = self.get_sub_trees_with_root(current_expression)
        hints = set()
        for current_expression_subtree in current_expression_subtrees:
            for children in current_expression_subtree.branches:
                hints.add(children.theorem_applied_name)

        return list(hints)

    def get_sub_trees_with_root(self, current_expression):
        if self.expression.is_equivalent_to(current_expression):
            return [self]
        if len(self.branches) == 0:
            return []
        accum = []
        for branch in self.branches:
            accum += branch.get_sub_trees_with_root(current_expression)
        return accum

    def contains(self, expression):
        to_check = [self]
        already_checked = set()
        while len(to_check) > 0:
            current = to_check.pop()
            if current.expression.to_string() not in already_checked:
                if current.expression.is_equivalent_to(expression) and \
                        current.expression.compare_variables(expression.variables):
                    return True

                current_replaced = current.expression.replace_variables()
                expression_replaced = expression.replace_variables()

                if current_replaced.is_equivalent_to(expression_replaced):
                    return True

                for branch in current.branches:
                    to_check.append(branch)
            already_checked.add(current.expression.to_string())
        return False

    def is_pre_simplification_step(self):
        if len(self.branches) == 1:
            branch = self.branches[0]
            if branch.theorem_applied_name == 'simplificacion' and len(branch.branches) == 0:
                return True
        return False

    def is_a_result(self, expression):
        to_check = [self]
        is_contained = False
        while len(to_check) > 0:
            current = to_check.pop()
            if current.expression.is_equivalent_to(expression):
                is_contained = True
                if not len(current.branches) == 0 and not current.is_pre_simplification_step():
                    return False
            for branch in current.branches:
                to_check.append(branch)

        return is_contained

    def get_amount_of_nodes(self):
        accum = [self]
        count = 0
        while len(accum) > 0:
            count += 1
            current = accum.pop()
            accum += current.branches
        return count

    # for debugging purposes
    def print_tree(self, level=0):
        ret = "\t" * level + 'Theorem: ' + self.theorem_applied_name + "\n"
        ret += "\t" * level + self.expression.to_expression_string() + "\n"
        if len(self.expression.variables) > 0:
            for variable in self.expression.variables:
                ret += "\t" * level + variable.to_print() + "\n"
        for branch in self.branches:
            ret += branch.print_tree(level + 1)
        return ret
