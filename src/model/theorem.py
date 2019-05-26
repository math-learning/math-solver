from src.model.template_match_analyzer import TemplateMatchAnalyzer
from src.model.expression import Expression

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

    def apply_to(self, expression):
        template = self.left

        # Apply to general structure
        analysis = self.analyzer.analyze(template, expression)
        if analysis.expression_match_template:
            return self.transform_right_side(analysis.equalities)
        
        # Apply to children
        else:
            children_transformation = self.apply_to_children(expression)
            if children_transformation != None:
                result = expression
                result.replace(children_transformation.before, children_transformation.after)
                return result

        return None

    def apply_to_children(self, expression):
        template = self.left
        children = expression.get_children()
        already_tried = set()

        # try applying directly to children
        for child in children:
            if str(child) not in already_tried:
                analysis = self.analyzer.analyze(template, child)
                if analysis.expression_match_template:
                    return TheoremApplication(child, self.transform_right_side(analysis.equalities))
                already_tried.add(str(child))
        
        # try applying to groups of children
        for size in range(2, expression.children_amount() + 1):
            children_of_size_n_possibilities = expression.get_child_with_size_possibilities(size)
            for child_of_size_n in children_of_size_n_possibilities:
                if str(child_of_size_n) not in already_tried:
                    analysis = self.analyzer.analyze(template, child_of_size_n)
                    if analysis.expression_match_template:
                        return TheoremApplication(child_of_size_n, self.transform_right_side(analysis.equalities))
                    already_tried.add(str(child_of_size_n))
        return None

    def transform_right_side(self, equalities):
        result = self.right
        for equality in equalities:
            result.replace(equality.template, equality.expression)
        return result