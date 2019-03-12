from unittest import TestCase

from src.model.Expression import Expression
from src.model.ExpressionComparator import ExpressionComparator


class TestExpressionComparator(TestCase):
    def test_compare(self):
        general_expression = Expression("diff(f(x) + g(x), x)")
        specific_expression = Expression("diff(x + 2,x)")
        result = ExpressionComparator.compare(general_expression, specific_expression)
        self.assertTrue(result)
