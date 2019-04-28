import sympy
import inspect
from cffi.setuptools_ext import basestring
from sympy import Symbol
from sympy.core.basic import preorder_traversal
from sympy.core.expr import UnevaluatedExpr
from sympy.core.function import Derivative, UndefinedFunction
from sympy.parsing.sympy_parser import parse_expr
from sympy.simplify import simplify

def is_sympy_exp(formula):
    sympy_classes = tuple(x[1] for x in inspect.getmembers(sympy,inspect.isclass))
    return isinstance(formula, sympy_classes)

class Expression:
    
    __evaluate = False

    @classmethod
    def set_evaluate(cls, value):
        cls.__evaluate = value
    
    def __init__(self, formula):
        if isinstance(formula, basestring):
            self.sympy_expr = parse_expr(formula)
        elif is_sympy_exp(formula):
            self.sympy_expr = formula
        else:
            raise(Exception("error while trying to create an Expression, unsuported formula type"))

    def is_leaf(self):
        return len(self.sympy_expr.args) == 0

    # Search and derivate expressions
    def solve_derivatives(self):
        for exp in preorder_traversal(self.sympy_expr):
            # TODO
            exp = Expression(exp)
            if exp.is_derivative():
                derivative_applied = self.wrap_expression(exp.apply_derivative())
                self.sympy_expr = self.sympy_expr.subs({exp.sympy_expr: derivative_applied})
    
    def is_derivative(self):
        return self.is_user_defined_func and self.compare_func(Expression("d()"))

    def apply_derivative(self):
        deriv = Derivative(self.sympy_expr.args[0],self.sympy_expr.args[1])
        return deriv.doit()

    def wrap_expression(self, exp):
        if self.__evaluate:
            return UnevaluatedExpr(exp)
        return exp

    def simplify(self):
        self.sympy_expr = simplify(self.sympy_expr)

    def is_user_defined_func(self):
        return isinstance(self.sympy_expr.func, UndefinedFunction)
    
    def to_string(self):
        return str(self.sympy_expr)

    def is_equivalent_to(self, expression):
        return simplify(self.sympy_expr) == simplify(expression.sympy_expr)

    def contains_user_defined_funct(self):
        for children in self.sympy_expr.preorder_traversal():
            if isinstance(self.sympy_expr.func, UndefinedFunction):
                return True
        return False

    def compare_func(self, expression):
        return self.sympy_expr.func == expression.sympy_expr.func
    
    def free_symbols_match(self, expression):
        for free_symbol in expression.sympy_expr.expr_free_symbols:
            if free_symbol.func == Symbol and not self.sympy_expr.has(free_symbol):
                return False
        return True

    def children_amount(self):
        return len(self.sympy_expr.args)
    
    def get_children(self):
        children = []
        for child in self.sympy_expr.args:
            children.append(Expression(child))
        return children
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Expression):
            return self.sympy_expr == other.sympy_expr
        return False