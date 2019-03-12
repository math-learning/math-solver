class ExpressionComparator:

    comparators = {
        "FunctionNode": FunctionNodeComparator()
    }

    @staticmethod
    def compare (general_expression, expression):

