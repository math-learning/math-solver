class ExpressionVariable:
    def __init__(self, tag, expression: 'Expression'):
        self.tag = tag
        self.expression = expression

    def to_json(self):
        return {'tag': self.tag, 'expression': self.expression} # TODO: que onda esto de mandarlo a json asi?
