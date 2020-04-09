from mathlearning.model.solution_tree_node import SolutionTreeNode
from mathlearning.model.theorem import Theorem
from mathlearning.services.step_service import StepService
from mathlearning.services.theorems_service import TheoremsService
from mathlearning.utils.logger import Logger
from mathlearning.model.expression import Expression
from typing import List

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
        simplified_expression = expression.simplify()
        tree = SolutionTreeNode(expression, applied_theorem, self.subtrees(expression, theorems))
        if simplified_expression != expression:
            tree.branches.append(
                SolutionTreeNode(simplified_expression,
                                 Theorem('simplificacion', None, None, []),
                                 self.subtrees(simplified_expression, theorems))
            )
        return tree

    def subtrees(self, expression: Expression, theorems: List[Theorem]) -> List[SolutionTreeNode]:
        logger.info('subtrees of ' + expression.to_string())
        theorems_that_apply = self.theorems_service.get_theorems_that_can_be_applied_to(expression, theorems)
        subtrees = []
        for theorem in theorems_that_apply:
            result = theorem.apply_to(expression)
            for case in result:
                if not expression.is_equivalent_to(case):
                    subtrees.append(SolutionTreeNode(case, theorem, self.subtrees(case, theorems)))

        derivatives_solving_possibilities = expression.derivatives_solving_possibilities()
        for derivatives_solving_possibility in derivatives_solving_possibilities:
            if not derivatives_solving_possibility.is_equivalent_to(expression):
                branch = SolutionTreeNode(derivatives_solving_possibility,
                                          Theorem('resolver derivadas', None, None, []),
                                          self.subtrees(derivatives_solving_possibility))
                subtrees.append(branch)

        return subtrees

    def resolve(self,
                problem_input: Expression,
                solution_tree: SolutionTreeNode,
                exercise_type: str,
                step_list: List[Expression],
                current_expression: Expression,
                theorems: List[Theorem]):
        return solution_tree.validate_new_expression(step_list[-1], current_expression)