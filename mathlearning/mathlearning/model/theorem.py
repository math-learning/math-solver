from mathlearning.model.template_match_analyzer import TemplateMatchAnalyzer
from mathlearning.model.expression import Expression
from mathlearning.utils.logger import Logger


logger = Logger.getLogger()

class TheoremApplication:
    def __init__(self,before, after):
        self.before = before
        self.after = after

class Theorem:
    def __init__(self, name, left, right, conditions):
        self.name = name
        self.left = Expression(left)
        self.right = Expression(right)
        self.conditions = conditions
        self.analyzer = TemplateMatchAnalyzer()

    def to_json(self):
        return {'name': self.name, 'right': str(self.right), 'left': str(self.left)}

    def apply_reverse_to(self, expression):
        from_side = self.right
        to_side = self.left
        return self._apply_to(expression, from_side, to_side)
        
    def apply_to(self, expression):
        from_side = self.left
        to_side = self.right
        return self._apply_to(expression, from_side, to_side)

    def _apply_to(self, expression, from_side, to_side):
        application_possibilities = []

        template = from_side

        # Apply to general structure
        logger.info("Trying to apply: " + self.name + " to the general structure: " + str(expression))
        analysis = self.analyzer.analyze(template,self.conditions, expression)
        if analysis.expression_match_template:
            application_possibilities.append(self.transform_side(to_side, analysis.equalities))
        
        # Apply to children
        
        logger.info("Trying to apply: " + self.name + " to expression CHILDREN: " + str(expression))
        children_transformations = self.apply_to_children(expression, from_side, to_side)
        for child_transformation in children_transformations:
            result = expression.get_copy()
            result.replace(child_transformation.before, child_transformation.after)
            application_possibilities.append(result)
            
        return application_possibilities

    def apply_to_children(self, expression, from_side, to_side):
        #TODO: apply to children of children
        application_possibilities = []

        template = from_side
        children = expression.get_children()
        already_tried = set()

        # try applying directly to children
        logger.info("Trying to apply: " + self.name + " directly to children: " + str(expression))
        for child in children:
            if str(child) not in already_tried:
                logger.info("Trying to apply: "  + self.name + " directly to child: " + str(child))
                analysis = self.analyzer.analyze(template,self.conditions, child)
                if analysis.expression_match_template:
                    application_possibilities.append(TheoremApplication(child, self.transform_side(to_side, analysis.equalities)))
                already_tried.add(str(child))
        
        # try applying to groups of children
        logger.info("Trying to apply: " + self.name + " to a group children: " + str(expression))
        for size in range(2, expression.children_amount() + 1):
            children_of_size_n_possibilities = expression.get_child_with_size_possibilities(size)
            for child_of_size_n in children_of_size_n_possibilities:
                if str(child_of_size_n) not in already_tried:
                    logger.info("Trying to apply: " + self.name + "to: " + str(child_of_size_n))
                    analysis = self.analyzer.analyze(template,self.conditions, child_of_size_n)
                    if analysis.expression_match_template:
                        application_possibilities.append(TheoremApplication(child_of_size_n, self.transform_side(to_side, analysis.equalities)))
                    already_tried.add(str(child_of_size_n))
        return application_possibilities

    def transform_right_side(self, equalities):
        result = self.right.get_copy()
        for equality in equalities:
            result.replace(equality.template, equality.expression)
        return result

    def transform_side(self, side, equalities):
        result = side.get_copy()
        for equality in equalities:
            result.replace(equality.template, equality.expression)
        return result