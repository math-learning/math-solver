import unittest

from sympy import Add, Derivative, Pow, Mul, cos

from mathlearning.model.expression import Expression


class TestExpression(unittest.TestCase):

    def test_is_leaf(self):
        leaf = Expression("x")
        self.assertTrue(leaf.is_leaf())

    def test_solve_derivatives(self):
        exp = Expression("\\frac{d(x)}{dx}")
        exp = exp.solve_derivatives()
        self.assertEqual(exp.to_expression_string(), '1')

    def test_compare(self):
        exp_one = Expression("x + x")
        exp_two = Expression("2 * x")

        self.assertTrue(exp_one.is_equivalent_to(exp_two))

    def test_some(self):
        exp_one = Expression("x + x")
        exp_two = Expression("x + x")

        self.assertTrue(exp_one == exp_two)

    def test_get_children(self):
        exp = Expression("x + x^2")
        children = exp.get_children()
        self.assertEqual(2, len(children))

        self.assertTrue(Expression("x") in children)
        self.assertTrue(Expression("x^2") in children)

    def test_get_children_add_three_elements(self):
        exp = Expression("x + x^2 + x^3")
        children = exp.get_children()
        self.assertEqual(3, len(children))

        self.assertTrue(Expression("x") in children)
        self.assertTrue(Expression("x^2") in children)
        self.assertTrue(Expression("x^3") in children)

    def test_get_children_derivative(self):
        exp = Expression("x^3 + \\frac{d(x)}{dx} + \\frac{d(x^2)}{dx}")
        children = exp.get_children()
        self.assertEqual(3, len(children))
        self.assertTrue(Expression("\\frac{d(x^2)}{dx}") in children)
        self.assertTrue(Expression("\\frac{d(x)}{dx}") in children)
        self.assertTrue(Expression("x^3") in children)

    def test_get_operators_by_level(self):
        exp = Expression("x + Derivative(x + x**2, x)", is_latex=False)
        operators = exp.get_operators_by_level()
        expected = {
            0: [Add],
            1: [Derivative],
            2: [Add],
            3: [Pow]
        }
        self.assertEquals(expected, operators)

    def test_get_operators_by_level_complex(self):
        exp = Expression("cos(x+Derivative(e**x,x))  + Derivative(x + x**(2*x+3), x)", is_latex=False)
        operators = exp.get_operators_by_level()
        expected = {
            0: [Add],
            1: [cos, Derivative],
            2: [Add, Add],
            3: [Derivative, Pow],
            4: [Pow, Add],
            5: [Mul]
        }
        self.assertEquals(expected, operators)

    def test_get_operators_by_level_one_level(self):
        exp = Expression("x + 2", is_latex=False)
        operators = exp.get_operators_by_level()
        expected = {
            0: [Add]
        }
        self.assertEquals(expected, operators)


    def test_all_operators_and_levels_match(self):
        expression = Expression("x + Derivative(x +  x**2, x)", is_latex=False)
        sub_expression = Expression("Derivative(x +  x**2, x)", is_latex=False)
        self.assertTrue(expression.operators_and_levels_match(sub_expression))

    def test_all_operators_and_levels_match_long_expression(self):
        expression = Expression("Derivative(x +  x**2, x) + Derivative(x +  x**2, x) + Derivative(x +  x**2, x)", is_latex=False)
        sub_expression = Expression("Derivative(x +  x**2, x)", is_latex=False)
        self.assertTrue(expression.operators_and_levels_match(sub_expression))

    def test_all_operators_and_levels_match_non_contained(self):
        expression = Expression("x + Derivative(x +  x**2, x)", is_latex=False)
        sub_expression = Expression("Derivative(x**2)", is_latex=False)
        self.assertFalse(expression.operators_and_levels_match(sub_expression))

    def test_get_depth_with_user_defined_func(self):
        expression = Expression("Derivative(f(x) +  g(x), x)", is_latex=False)
        self.assertEquals(3, expression.get_depth())

    def test_get_simplifications(self):
        exp  = Expression('x**2*cos(x) + 2*x*sin(x) + x*Derivative(exp(x), x) + exp(x)', is_latex=False)
        exp.get_simplifications()

    def test_apply_integral(self):
        expression = Expression('Integral(x+x**2,x)', is_latex=False)
        result = expression.apply_integral()
        self.assertEquals(result, Expression('x**2/2 + x**3/3', is_latex=False))


    def test_integrate_is_integral(self):
        expression = Expression('Integral(x+x**2,x)', is_latex=False)
        self.assertTrue(expression.is_integral())

    def test_integrate_is_integral_false(self):
        expression = Expression('Derivative(x+x**2,x)', is_latex=False)
        self.assertFalse(expression.is_integral())

    def test_integrate_solving_possibilities(self):
        expression = Expression('Integral(x,x) + Integral(x**2,x) - Integral(cos(x),x)', is_latex=False)
        result = expression.integrals_solving_possibilities()
        self.assertEquals(len(result), 3)
        self.assertTrue(Expression('x**2/2 + Integral(x**2,x) - Integral(cos(x),x)', is_latex=False) in result)
        self.assertTrue(Expression('Integral(x,x) + x**3/3 - Integral(cos(x),x)', is_latex=False) in result)
        self.assertTrue(Expression('Integral(x,x) + Integral(x**2,x) - sin(x)', is_latex=False) in result)
