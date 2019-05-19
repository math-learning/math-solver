import inspect

import sympy
from cffi.setuptools_ext import basestring
from sympy import Symbol
from sympy.core.basic import preorder_traversal
from sympy.core.expr import UnevaluatedExpr
from sympy.core.function import Derivative, UndefinedFunction
from sympy.parsing.sympy_parser import parse_expr
from sympy.simplify import simplify
from src.utils.list.list_size_transformer import ListSizeTransformer
from src.utils.list.commutative_group_transformer import CommutativeGroupTransformer
from src.utils.list.non_commutative_group_transformer import NonCommutativeGroupTransformer

def is_sympy_exp(formula):
    sympy_classes = tuple(x[1] for x in inspect.getmembers(sympy,inspect.isclass))
    return isinstance(formula, sympy_classes)

class Expression:
    
    __evaluate = False

    @classmethod
    def set_evaluate(cls, value):
        cls.__evaluate = value
    
    def __init__(self, formula):
        self.commutative_group_transformer = CommutativeGroupTransformer()
        self.non_commutative_group_transformer = NonCommutativeGroupTransformer()
        self.commutative_list_size_transformer = ListSizeTransformer(CommutativeGroupTransformer())
        self.non_commutative_list_size_transformer = ListSizeTransformer(NonCommutativeGroupTransformer())
        if isinstance(formula, basestring):
            self.sympy_expr = parse_expr(formula)
        elif is_sympy_exp(formula):
            self.sympy_expr = formula
        else:
            raise(Exception("error while trying to create an Expression, unsuported formula type"))

    def is_leaf(self):
        return len(self.sympy_expr.args) == 0

    def is_commutative(self):
        return self.sympy_expr.is_commutative

    # Search and derivate expressions
    def solve_derivatives(self):
        for exp in preorder_traversal(self.sympy_expr):
            # TODO
            exp = Expression(exp)
            if exp.is_derivative():
                derivative_applied = exp.apply_derivative()
                self.replace(exp, derivative_applied)
    
    def is_derivative(self):
        return isinstance(self.sympy_expr.func, UndefinedFunction) and self.compare_func(Expression("d()"))

    def apply_derivative(self):
        deriv = Derivative(self.sympy_expr.args[0],self.sympy_expr.args[1])
        return Expression(deriv.doit())

    def wrap_expression(self, exp):
        if self.__evaluate:
            return UnevaluatedExpr(exp)
        return exp

    def simplify(self):
        self.sympy_expr = simplify(self.sympy_expr)

    def is_user_defined_func(self):
        return isinstance(self.sympy_expr.func, UndefinedFunction) and not self.is_derivative() 
    
    def to_string(self):
        return str(self.sympy_expr)

    def is_equivalent_to(self, expression):
        return simplify(self.sympy_expr) == simplify(expression.sympy_expr)

    def contains_user_defined_funct(self):
        if self.is_user_defined_func():
            return True

        if len(self.get_children()) == 0:
            return False

        result = False

        for child in self.get_children():
            result = result or child.contains_user_defined_funct()
        return result

    def compare_func(self, expression):
        return self.sympy_expr.func == expression.sympy_expr.func
    
    def free_symbols_match(self, expression):
        for free_symbol in expression.sympy_expr.expr_free_symbols:
            if free_symbol.func == Symbol and not self.sympy_expr.has(free_symbol):
                return False
        return True

    def children_amount(self):
        # TODO: handle this cases derivatives
        if self.is_derivative():
            return 1
        return len(self.sympy_expr.args)
    
    def get_children(self):
        children = []
        if self.is_derivative():
            children.append(Expression(self.sympy_expr.args[0]))
            return children
        for child in self.sympy_expr.args:
            children.append(Expression(child))
        return children

    def replace(self, to_replace, replacement):
        to_replace_sympy = to_replace.sympy_expr
        replacement_sympy = replacement.sympy_expr
        self.sympy_expr = self.sympy_expr.subs({to_replace_sympy: replacement_sympy})
    
    def get_child_with_size_possibilities(self, size):
        if self.is_commutative():
            transformer = self.commutative_group_transformer
        else:
            transformer = self.non_commutative_list_size_transformer
        possibilities = []
        combinations = transformer.combinations_of_n_elements(self.get_children(), size)

        for combination in combinations:
            possibilities.append(combination.elements)
        return possibilities

    def get_children_with_size(self, size):
        # TODO refactor
        if self.is_commutative():
            transformer = self.commutative_list_size_transformer
        else:
            transformer = self.non_commutative_list_size_transformer
        transformations = transformer.transform(list(self.sympy_expr.args), size)
        results = []
        for transformation in transformations:
            children_transformation = []
            for item in transformation:
                if len(item) == 1:
                    children_transformation.append(Expression(item[0]))
                elif len(item) > 1:
                    children_sympy = self.sympy_expr.func(*item,evaluate=self.__evaluate) 
                    children_transformation.append(Expression(children_sympy))
            results.append(children_transformation)
        return results

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Expression):
            return self.sympy_expr == other.sympy_expr
        return False
    
    def __str__(self):
        return "Expression with sympy_expr: " + str(self.sympy_expr)