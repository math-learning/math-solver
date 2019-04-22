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


from cffi.setuptools_ext import basestring
from sympy import Symbol
from sympy.core.basic import preorder_traversal
from sympy.core.expr import UnevaluatedExpr
from sympy.core.function import Derivative, UndefinedFunction
from sympy.parsing.sympy_parser import parse_expr
from sympy.simplify import simplify


class TemplateComparator:
    def __init__(self):
        pass
    
    def match(self, template, expression):
        return self.match_rec(template, expression)

    def match_rec(self, template, expression):
        if template.is_leaf() and expression.is_leaf():
            return template.compare(expression)

        if template.is_user_defined_func():
            return template.free_symbols_match(expression)

    #     if template.children_amount() == expression.children_amount():
    #         return self.compare_sympy_expression(structure, expression, equalities)

    #     return self.compare_non_equal_lengths(structure, expression, equalities)

    # def compare_sympy_expression(self, structure, expression, equalities):
    #     if structure.func == expression.func:
    #             if structure.is_commutative:
    #                 # print("is cummulative")
    #                 pairs_to_compare = self.comparator_utils.get_children_pairs(structure.args, expression.args)
    #                 for children_pairs in pairs_to_compare:
    #                     comparison = self.compare_children_combinations(children_pairs, equalities)
    #                     if comparison.structures_match:
    #                         return comparison
    #             else:
    #                 # print("comparing non commutative")
    #                 pairs_to_compare = self.comparator_utils.get_equivalent_children_pairs(len(structure), structure.args, expression.args)
    #                 return self.compare_children_combinations(pairs_to_compare, equalities)
    #     return ComparisonResult(False, [])

    # def compare_children_combinations(self, children_pairs, equalities):
    #     result = ComparisonResult(True, [])
    #     for pair in children_pairs:
    #         children_comparison_result = self.compare_rec(pair.structure_child, pair.expression_child, equalities)
    #         result.structures_match &= children_comparison_result.structures_match
    #         result.equalities += children_comparison_result.equalities
    #     return result


    # def compare_non_equal_lengths(self, structure, expression, equalities):
    #     # if at least one is a user defined function we have to group arguments to see if matches
    #     contains_user_defined_function = self.user_defined_func_comparator.contains_user_defined_function(structure)
    #     if len(structure.args) < len(expression.args) and contains_user_defined_function:
    #         if structure.func.is_commutative:
    #             # TODO: complex logic
    #             print(expression.func(*expression.args))

    #         return ComparisonResult(False, [])
    #     return ComparisonResult(False, [])

import sympy
import inspect

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
            if exp.func == Derivative:
                derivative_applied = self.wrap_expression(exp.doit())
                self.sympy_expr = self.sympy_expr.subs({exp: derivative_applied})
    
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
        return self.sympy_expr.func == expression.func
    
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


# Expression that has at least one user defined function
class TemplateExpression(Expression):

    def match(self, expression):
        pass
