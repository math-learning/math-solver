class Equality:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ComparisonPair:
    def __init__(self, structure_child, expression_child):
        self.structure_child = structure_child
        self.expression_child = expression_child

class Expressions:

    # Pair the first, second, ... node of both expressions together.
    def get_equivalent_children_pairs(self, length, structure_children, expression_children):
        comparison_pairs = []
        for i in range(0, length):
            comparison_pairs .append(ComparisonPair(structure_children[i], expression_children[i]))
        return comparison_pairs


    def get_children_pairs(self, structure_children, expression_children):
        return self.get_children_pairs_rec(structure_children, expression_children, [], [])

    # get the possible combinations of expression ren and structure children that can be compared.
    def get_children_pairs_rec(self, structure_children, expression_children, accum, possibles):
        if len(structure_children) == 1 and len(expression_children) == 1:
            accum.append(ComparisonPair(structure_children[0], expression_children[0]))
            possibles.append(accum)
            return possibles

        # TODO: RENAME
        for expression_child in expression_children:
            new_accum = accum[:]
            new_accum.append(ComparisonPair(structure_children[0], expression_child))
            structure_children_without_first = structure_children[1:]
            expression_children_without_child = list(expression_children[:])
            expression_children_without_child.remove(expression_child)
            expression_children_without_child = tuple(expression_children_without_child)
            possibles = self.get_children_pairs_rec(structure_children_without_first, expression_children_without_child, new_accum, possibles)

        return possibles


from sympy import Symbol
from sympy.core.basic import preorder_traversal
from sympy.core.expr import UnevaluatedExpr
from sympy.core.function import Derivative, UndefinedFunction
from sympy.parsing.sympy_parser import parse_expr
from sympy.simplify import simplify


class Expression:

    def __init__(self, formula, evaluate):
        self.sympy_expr = parse_expr(formula, evaluate=False)
        self.evaluate = evaluate

    def is_leaf(self):
        return len(self.sympy_expr.args) == 0
    
    # Search and derivate expressions
    def solve_derivatives(self):
        for exp in preorder_traversal(self.sympy_expr):
            if exp.func == Derivative:
                derivative_applied = self.wrap_expression(exp.doit())
                self.sympy_expr = self.sympy_expr.subs({exp: derivative_applied})
    
    def wrap_expression(self, exp):
        if self.evaluate:
            return UnevaluatedExpr(exp)
        return exp

    def simplify(self):
        self.sympy_expr = simplify(self.sympy_expr)

    def is_user_defined_func(self):
        return isinstance(self.sympy_expr.func, UndefinedFunction)
    
    def to_string(self):
        return str(self.sympy_expr)

    def compare(self, expression):
        return simplify(self.sympy_expr) == simplify(expression.sympy_expr)
    
