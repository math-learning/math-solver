import json

from mathlearning.model.expression import Expression


class ExpressionVariable:
    def __init__(self, tag, expression: Expression):
        self.tag = tag
        self.expression = expression

    def to_json(self):
        return {'tag': self.tag, 'expression': self.expression.to_json()} # TODO: que onda esto de mandarlo a json asi?

    def to_string(self) -> str:
        return json.dumps({'tag': self.tag, 'expression': self.expression.to_string() })

    def __eq__(self, other):
        return self.tag == other.tag and self.expression == other.expression

    def to_print(self):
        return f'{self.tag}: {self.expression.to_expression_string()}'
