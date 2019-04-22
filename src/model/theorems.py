from src.model.expressions import Expression

class Theorem:
    def __init__(self, name, left, right):
        self.name = name
        self.left = Expression(left)
        self.right = Expression(right)

    def to_json(self):
        return {'name': self.name, 'right': str(self.right), 'left': str(self.left)}

    def apply_to(self, expression):
        match_template = self.compare_rec(self.left, expression)
        return expression

    def compare_rec(self, template, expression):
        if template.is_leaf() and expression.is_leaf():
            return template.compare(expression)

        if template.is_user_defined_func():
            return template.free_symbols_match(expression)

        # if len(template.args) == len(expression.args):
        #     return self.compare_rec()

        # return self.compare_non_equal_lengths(structure, expression, equalities)