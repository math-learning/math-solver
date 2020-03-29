from mathlearning.model.theorem import Theorem
from mathlearning.services.step_service import StepService
from mathlearning.services.theorems_service import TheoremsService
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
            'expression': self.expression.to_latex_with_derivatives(),
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


class ResultService:

    def __init__(self):
        self.step_service = StepService()
        self.theorems_service = TheoremsService()

    def get_derivative_result(self, expression: Expression) -> Expression:
        return expression.solve_derivatives()

    def solution_tree(self, expression: Expression, theorems: List[Theorem]) -> SolutionTreeNode:
        logger.info("get solution tree for: " + expression.to_string())
        return self.solution_tree_for(expression, theorems, None)

    def solution_tree_for(self, expression: Expression, theorems: List[Theorem], applied_theorem: Theorem   ):
        simplified_expression = expression.simplify()
        tree = SolutionTreeNode(expression, applied_theorem, self.subtrees(expression, theorems))
        if simplified_expression != expression:
            tree.branches.append(
                SolutionTreeNode(simplified_expression,
                                 Theorem('simplificacion', None, None, []),
                                 self.subtrees(simplified_expression, theorems))
            )
        tree.apply_derivatives_to_leaves()
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
        return subtrees

    def appy_derivatives(self, tree: SolutionTreeNode) -> SolutionTreeNode:
        tree.apply_derivatives_to_leaves()

