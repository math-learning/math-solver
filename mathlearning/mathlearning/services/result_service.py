from mathlearning.model.solution_tree_node import SolutionTreeNode
from mathlearning.model.theorem import Theorem
from mathlearning.services.step_service import StepService
from mathlearning.services.theorems_service import TheoremsService
from mathlearning.utils.logger import Logger
from mathlearning.model.expression import Expression
from typing import List, Tuple

logger = Logger.getLogger()


class ResultService:

    def __init__(self):
        self.step_service = StepService()
        self.theorems_service = TheoremsService()

    def get_derivative_result(self, expression: Expression) -> Expression:
        return expression.solve_derivatives()

    def solution_tree(self, expression: Expression, theorems: List[Theorem]) -> SolutionTreeNode:
        logger.info("get solution tree for: " + expression.to_string())
        return self.solution_tree_for(expression, theorems, None)

    def solution_tree_for(self, expression: Expression, theorems: List[Theorem], applied_theorem: Theorem):

        already_seen = set()
        subtrees = self.subtrees(expression, theorems, already_seen)
        already_seen |= subtrees[1]
        tree = SolutionTreeNode(expression, applied_theorem, subtrees[0])

        # TODO: check if this si necessary
        simplified_expression = expression.simplify()
        if simplified_expression.sympy_expr != expression.sympy_expr:
            if simplified_expression.to_string() in already_seen:
                tree.branches.append(
                    SolutionTreeNode(simplified_expression,
                                     Theorem('simplificacion', None, None, []),
                                     [])
                )
            else:
                tree.branches.append(
                    SolutionTreeNode(simplified_expression,
                                     Theorem('simplificacion', None, None, []),
                                     self.subtrees(simplified_expression, theorems, already_seen)[0])
                )
        return tree

    # Returns the subtrees of a specific expression, if a expression is already in the tree the subtree is not going
    # to be added again.
    def subtrees(self, expression: Expression, theorems: List[Theorem], already_seen: set) -> Tuple[List[SolutionTreeNode], set]:
        possible_theorems = self.theorems_service.possible_theorems_for(expression, theorems)
        subtrees = []
        already_seen.add(expression.to_string())
        for theorem in possible_theorems:
            result = theorem.apply_to(expression)
            for case in result:
                if not expression.is_equivalent_to(case):
                    if case.to_string() in already_seen:
                        subtrees.append(SolutionTreeNode(case, theorem, []))
                    else:
                        subtrees_result = self.subtrees(case, theorems, already_seen)
                        subtrees.append(SolutionTreeNode(case, theorem, subtrees_result[0]))
                        already_seen |= subtrees_result[1]

        # Try solving derivatives
        derivatives_solving_possibilities = expression.derivatives_solving_possibilities()
        for derivatives_solving_possibility in derivatives_solving_possibilities:
            if not derivatives_solving_possibility.is_equivalent_to(expression):
                if derivatives_solving_possibility.to_string() in already_seen:
                    branch = SolutionTreeNode(derivatives_solving_possibility,
                                              Theorem('resolver derivadas', None, None, []),
                                              [])
                else:
                    subtrees_result = self.subtrees(derivatives_solving_possibility, theorems, already_seen)
                    branch = SolutionTreeNode(derivatives_solving_possibility,
                                              Theorem('resolver derivadas', None, None, []),
                                              subtrees_result[0])
                    already_seen |= subtrees_result[1]

                subtrees.append(branch)

        # Try solving integrals
        # TODO: fix duplicated code
        integral_solving_posibbilities = expression.integrals_solving_possibilities()
        for integral_solving_possibility in integral_solving_posibbilities:
            if not integral_solving_possibility.is_equivalent_to(expression):
                if integral_solving_possibility.to_string() in already_seen:
                    branch = SolutionTreeNode(integral_solving_possibility,
                                              Theorem('resolver integrales', None, None, []),
                                              [])
                else:
                    subtrees_result = self.subtrees(integral_solving_possibility, theorems, already_seen)
                    branch = SolutionTreeNode(integral_solving_possibility,
                                              Theorem('resolver integrales', None, None, []),
                                              subtrees_result[0])
                    already_seen |= subtrees_result[1]

                subtrees.append(branch)

        return subtrees, already_seen

    def resolve(self,
                problem_input: Expression,
                solution_tree: SolutionTreeNode,
                exercise_type: str,
                step_list: List[Expression],
                current_expression: Expression,
                theorems: List[Theorem]):
        if len(step_list) == 0:
            previous_step = problem_input
        else:
            previous_step = step_list[-1]
        result, hints = solution_tree.validate_new_expression(current_expression, previous_step)
        hints = list(map(lambda hint_theorem: {'title': hint_theorem.name}, hints))
        return result, hints
