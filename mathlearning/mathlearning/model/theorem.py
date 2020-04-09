from mathlearning.model.template_match_analyzer import TemplateMatchAnalyzer
from mathlearning.model.expression import Expression
from mathlearning.utils.logger import Logger
from typing import List
from mathlearning.model.template_match_analyzer import Equality
import sympy
from typing import Union

logger = Logger.getLogger()

class TheoremApplication:
    def __init__(self, before, after):
        self.before = before
        self.after = after


class Theorem:
    # left and right could be expressions or str
    def __init__(self, name: str, left: Union['Expression', str], right: Union['Expression', str], conditions: dict):
        self.name = name
        if left is not None and right is not None:
            self.left = Expression(left)
            self.right = Expression(right)
        else:
            self.left = Expression(sympy.nan)
            self.right = Expression(sympy.nan)

        self.conditions = conditions
        self.analyzer = TemplateMatchAnalyzer()

    def to_json(self) -> dict:
        left = ''
        right = ''
        if self.left is not None:
            left = self.left.to_latex_with_derivatives()
        if self.right is not None:
            right = self.right.to_latex_with_derivatives()
        return {'name': self.name, 'right': right, 'left': left}

    # Returns the application possibilities (could be more than 1)
    def apply_reverse_to(self, expression: Expression) -> List[Expression]:
        from_side = self.right
        to_side = self.left
        return self._apply_to(expression, from_side, to_side)

    def operators_and_levels_match(self, expression: Expression):
        return expression.operators_and_levels_match(self.left)


    # Returns the application possibilities (could be more than 1)
    def apply_to(self, expression: Expression) -> List[Expression]:
        from_side = self.left
        to_side = self.right
        return self._apply_to(expression, from_side, to_side)

    def _apply_to(self, expression: Expression, from_side: Expression, to_side: Expression) -> List[Expression]:
        application_possibilities = []

        if not expression.operators_and_levels_match(from_side):
            return []
        template = from_side

        # Apply to general structure
        logger.info("Trying to apply: " + self.name +
                    " to the general structure: " + str(expression))
        analysis = self.analyzer.analyze(template, self.conditions, expression)
        if analysis.expression_match_template:
            application_possibilities.append(
                self.transform_side(to_side, analysis.equalities))

        # Apply to children

        logger.info("Trying to apply: " + self.name +
                    " to expression CHILDREN: " + str(expression))
        children_transformations = self.apply_to_children(
            expression, from_side, to_side)
        for child_transformation in children_transformations:
            result = expression.get_copy()
            result.replace(child_transformation.before,
                           child_transformation.after)
            application_possibilities.append(result)

        return application_possibilities

    def apply_to_children(self, expression: Expression, from_side: Expression, to_side: Expression) -> List[Expression]:
        # TODO: apply to children of children
        application_possibilities = []

        template = from_side
        children = expression.get_children()
        already_tried = set()

        # try applying directly to children
        # for example in x + y
        # try applying to x
        # try applying to y
        logger.info("Trying to apply: " + self.name +
                    " directly to children: " + str(expression))
        for child in children:
            if str(child) not in already_tried:
                logger.info("Trying to apply: " + self.name +
                            " directly to child: " + str(child))
                analysis = self.analyzer.analyze(
                    template, self.conditions, child)
                if analysis.expression_match_template:
                    application_possibilities.append(TheoremApplication(
                        child, self.transform_side(to_side, analysis.equalities)))
                # children of children
                children_of_children_result = self.apply_to_children(child, from_side, to_side)
                application_possibilities += children_of_children_result
                already_tried.add(str(child))

        # try applying to groups of children
        # for example in x + y + z
        # try with: x + y ; x + z : y + z
        logger.info("Trying to apply: " + self.name +
                    " to a group children: " + str(expression))
        for size in range(2, expression.children_amount() + 1):
            children_of_size_n_possibilities = expression.get_child_with_size_possibilities(
                size)
            for child_of_size_n in children_of_size_n_possibilities:
                if str(child_of_size_n) not in already_tried:
                    logger.info("Trying to apply: " + self.name +
                                "to: " + str(child_of_size_n))
                    analysis = self.analyzer.analyze(
                        template, self.conditions, child_of_size_n)
                    if analysis.expression_match_template:
                        application_possibilities.append(TheoremApplication(
                            child_of_size_n, self.transform_side(to_side, analysis.equalities)))
                    already_tried.add(str(child_of_size_n))
        return application_possibilities

    def transform_right_side(self, equalities: List[Equality]) -> Expression:
        result = self.right.get_copy()
        for equality in equalities:
            result.replace(equality.template, equality.expression)
        return result

    def transform_side(self, side: Expression, equalities: List[Equality]) -> Expression:
        result = side.get_copy()
        for equality in equalities:
            result.replace(equality.template, equality.expression)
        return result


    def __str__(self):
        return self.name + ' - ' + self.left.to_string() + " = " + self.right.to_string()
