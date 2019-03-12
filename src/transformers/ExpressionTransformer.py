from src.model.TransformationResult import TransformationResult


class ExpressionTransformer:

    def transform(self, structure, equalities):
        new_expression = structure
        for equality in equalities:
            new_expression = new_expression.subs({equality[0]: equality[1]})
        return new_expression