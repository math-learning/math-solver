import inspect
import sympy
from sympy import Symbol
from sympy.parsing.latex import parse_latex
from sympy.core.basic import preorder_traversal
from sympy.core.function import Derivative, UndefinedFunction
from sympy.parsing.sympy_parser import parse_expr
from sympy.simplify import simplify
from mathlearning.utils.list.list_size_transformer import ListSizeTransformer
from mathlearning.utils.list.commutative_group_transformer import CommutativeGroupTransformer
from mathlearning.utils.list.non_commutative_group_transformer import NonCommutativeGroupTransformer
from mathlearning.utils.latex_utils import clean_latex
from typing import Union, List

from mathlearning.utils.sympy_utils import SympyUtils

sympy_classes = tuple(x[1] for x in inspect.getmembers(sympy, inspect.isclass))

def is_sympy_exp(formula):
    return isinstance(formula, sympy_classes)

class Expression:

    def __init__(self, formula: Union['Expression', str], is_latex=True):
        self.commutative_group_transformer = CommutativeGroupTransformer()
        self.non_commutative_group_transformer = NonCommutativeGroupTransformer()
        self.commutative_list_size_transformer = ListSizeTransformer(CommutativeGroupTransformer())
        self.non_commutative_list_size_transformer = ListSizeTransformer(NonCommutativeGroupTransformer())
        if isinstance(formula, str) and is_latex:
            clean_formula = clean_latex(formula)
            self.sympy_expr = parse_latex(clean_formula)
            self.sympy_expr = self.sympy_expr.subs(simplify(parse_expr("e")), parse_expr("exp(1)"))
        elif is_sympy_exp(formula):
            self.sympy_expr = formula
        elif isinstance(formula, str):
            self.sympy_expr = parse_expr(formula)
        else:
            raise (Exception("error while trying to create an Expression, unsuported formula type" + str(formula)))

    def is_leaf(self) -> bool:
        return len(self.sympy_expr.args) == 0

    def is_commutative(self) -> bool:
        return self.sympy_expr.is_commutative

    def is_constant(self) -> bool:
        free_symbols = self.sympy_expr.expr_free_symbols
        for symbol in free_symbols:
            if isinstance(symbol, Symbol):
                return False
        return True

    def get_copy(self) -> 'Expression':
        return Expression(parse_expr(str(self.sympy_expr)))

    # Search and derivate expressions
    def solve_derivatives(self) -> 'Expression':
        derivatives_solved = self.get_copy()
        for exp in preorder_traversal(self.sympy_expr):
            # TODO
            exp = Expression(exp)
            if exp.is_derivative():
                derivative_applied = exp.apply_derivative()
                derivatives_solved.replace(exp, derivative_applied)
        return derivatives_solved

    def replace_derivatives_for_json(self):
        replacements = []
        for exp in preorder_traversal(self.sympy_expr):
            # TODO
            expression = Expression(exp)
            if expression.is_derivative():
                content = Expression(exp.args[0]).to_latex()
                variable = Expression(exp.args[1][0]).to_latex()

                replacement = '\\frac{d(%s)}{d%s}' % (content, variable)
                replacements.append({"derivative": expression.to_latex(), "replacement": replacement})
        return replacements


    # possibilities of solving just 1 derivative
    def derivatives_solving_possibilities(self) -> List['Expression']:

        derivatives = []
        for exp in preorder_traversal(self.sympy_expr):
            exp = Expression(exp)
            if exp.is_derivative():
                derivatives.append(exp)

        possibilities = []
        for derivative in derivatives:
            derivative_solved = self.get_copy()
            derivative_solved.replace(derivative, derivative.apply_derivative())
            possibilities.append(derivative_solved)
        return possibilities

    def is_derivative(self) -> bool:
        return isinstance(self.sympy_expr, Derivative)

    def apply_derivative(self) -> 'Expression':
        deriv = Derivative(self.sympy_expr.args[0], self.sympy_expr.args[1])
        return Expression(deriv.doit())

    def simplify(self) -> 'Expression':
        copy = self.get_copy()
        return Expression(simplify(copy.sympy_expr))

    def is_user_defined_func(self) -> bool:
        return isinstance(self.sympy_expr.func, UndefinedFunction) and not self.is_derivative()

    def to_string(self) -> str:
        return str(self.sympy_expr)

    def to_latex(self) -> str:
        return sympy.latex(self.sympy_expr)


    def to_latex_with_derivatives(self) -> str:
        replacements = self.replace_derivatives_for_json()
        latex_exp = sympy.latex(self.sympy_expr)
        for replacement in replacements:
            latex_exp = latex_exp.replace(replacement['derivative'], replacement['replacement'])
        return latex_exp

    def is_equivalent_to(self, expression: 'Expression') -> bool:
        if str(simplify(self.sympy_expr)) == str(simplify(expression.sympy_expr)) or \
                self == expression:
            return True
        self_simplifications = self.get_simplifications()
        expression_simplifications = expression.get_simplifications()
        for self_simplification in self_simplifications:
            for expression_simplification in expression_simplifications:
                simplifications_match = str(self_simplification.sympy_expr) == str(expression_simplification.sympy_expr)
                if simplifications_match:
                    return True
        return False

    def contains_user_defined_funct(self) -> bool:
        if self.is_user_defined_func():
            return True
        if len(self.get_children()) == 0:
            return False
        result = False
        for child in self.get_children():
            result = result or child.contains_user_defined_funct()
        return result

    def compare_func(self, expression: 'Expression') -> bool:
        return self.sympy_expr.func == expression.sympy_expr.func

    def has_all_free_symbols(self, free_symbols) -> bool:
        for free_symbol in free_symbols:
            if free_symbol.func == Symbol and not self.sympy_expr.has(free_symbol) and str(free_symbol) != "e":
                return False
        return True

    def free_symbols_match(self, expression: 'Expression') -> bool:
        result = self.has_all_free_symbols(expression.sympy_expr.expr_free_symbols)
        result &= expression.has_all_free_symbols(self.sympy_expr.expr_free_symbols)
        return result

    def children_amount(self) -> int:
        # TODO: handle this cases derivatives
        if self.is_derivative():
            return 1
        return len(self.get_children())

    def get_children(self) -> List['Expression']:
        children = []
        if self.is_derivative():
            children.append(Expression(self.sympy_expr.args[0]))
            return children
        for child in self.sympy_expr.args:
            expression_child = Expression(child)
            if self.is_commutative() and self.compare_func(expression_child):
                children.extend(expression_child.get_children())
            else:
                children.append(expression_child)
        return children

    # todo remove side effect
    def replace(self, to_replace: 'Expression', replacement: 'Expression'):
        to_replace_sympy = to_replace.sympy_expr
        replacement_sympy = simplify(replacement.sympy_expr)
        new_sympy_expr = self.sympy_expr.subs({to_replace_sympy: replacement_sympy})
        if new_sympy_expr == self.sympy_expr:
            to_replace_sympy = simplify(to_replace.sympy_expr)
            self.sympy_expr = self.sympy_expr.subs({to_replace_sympy: replacement_sympy})
        else:
            self.sympy_expr = new_sympy_expr

    # Refactor
    def get_child_with_size_possibilities(self, size) -> List['Expression']:
        if self.is_commutative():
            transformer = self.commutative_group_transformer
        else:
            transformer = self.non_commutative_list_size_transformer
        possibilities = []
        combinations = transformer.combinations_of_n_elements(self.get_children(), size)

        for combination in combinations:
            sympy_elements = []
            for element in combination.elements:
                sympy_elements.append(element.sympy_expr)
            children_sympy = self.sympy_expr.func(*sympy_elements)
            possibilities.append(Expression(children_sympy))
        return possibilities

    def get_children_with_size(self, size) -> List[List['Expression']]:
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
                    children_sympy = self.sympy_expr.func(*item)
                    children_transformation.append(Expression(children_sympy))
            results.append(children_transformation)
        return results

    def get_simplifications(self) -> List['Expression']:
        simplifications = [
            Expression(sympy.expand(self.sympy_expr)),
            Expression(sympy.cancel(self.sympy_expr)),
            Expression(sympy.simplify(self.sympy_expr)),
            Expression(sympy.factor(self.sympy_expr))
        ]
        return simplifications

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Expression):
            return self.to_string() == other.to_string()
        return False

    def __str__(self):
        return str(self.sympy_expr)

    # TODO: refactor
    def get_operators_by_level(self):
        operators = {}
        to_check = [{
            'expression': self,
            'level': 0
        }]
        while len(to_check) > 0:
            current = to_check.pop()
            current_level = current['level']
            current_expression =  current['expression']
            operator = current['expression'].sympy_expr.func

            if not isinstance(operator, UndefinedFunction) and not current_expression.is_constant() \
                    and not operator.is_symbol:

                if current_level not in operators:
                    operators[current_level] = []

                if SympyUtils.is_division(current_expression.sympy_expr):
                    operators[current_level].append('Division')

                operators[current_level].append(operator)
                to_check += list(
                    map(
                        lambda expression: {'expression': expression, 'level': current_level + 1},
                        current['expression'].get_children()
                    )
                )

        return operators

    # TODO: refactor
    # Compares if all the operators or a sub_expression are contained and in the right level order
    def operators_and_levels_match(self, sub_expression: 'Expression'):
        self_operators = self.get_operators_by_level()
        sub_expression_operators = sub_expression.get_operators_by_level()

        if len(sub_expression_operators) == 0:
            return True

        # expression  x + x**(2+x) -- 0: [Add] ; 1: [Pow] ; 2: [Add]
        # sub_expression  x**(2+x) -- 0: [Pow] ; 1: [Add]
        # self_level is used  to find the starting point where the first Pow of sub_expression is.
        # in this example the only possible values are 0 and 1  since if we select 2 as the starting level
        # we have to match the 1: [Add] sub_expression level with an non existent level.
        for self_level in range(0, len(self_operators) - len(sub_expression_operators) + 1):
            first_sub_expression_operator = sub_expression_operators[0][0]
            if first_sub_expression_operator in self_operators[self_level]:
                all_match = True
                # check if the rest of the levels match
                for self_level_to_check in range(self_level, self_level + len(sub_expression_operators)):
                    sub_level_to_check = self_level_to_check - self_level
                    sub_level_operators = sub_expression_operators[sub_level_to_check]
                    for sub_level_operator in sub_level_operators:
                        if sub_level_operator not in self_operators[self_level_to_check]:
                            all_match = False
                if all_match:
                    return True
        return False

    # TODO: refactor
    def get_subtrees_with_root_func_by_level(self, expression: 'Expression'):
        subtrees = []
        func = expression.sympy_expr.func
        to_check = [{
            'expression': self,
            'level': 0
        }]
        while len(to_check) > 0:
            current = to_check.pop()
            current_level = current['level']
            if current['expression'].sympy_expr.func == func:
                subtrees.append(current)
            to_check += list(
                map(
                    lambda expression: {'expression': expression, 'level': current_level + 1},
                    current['expression'].get_children()
                )
            )
        return subtrees

    # TODO: refactor
    def get_depth(self):
        if self is None:
            return 0

        to_check = [{
            'expression': self,
            'depth': 1
        }]

        max = 0
        while len(to_check) > 0:
            current = to_check.pop()
            if current['depth'] > max:
                max = current['depth']
            if not current['expression'].is_user_defined_func():
                to_check += list(
                    map(
                        lambda expression: {'expression': expression, 'depth': current['depth'] + 1},
                        current['expression'].get_children()
                    )
                )
        return max

    def can_group_children(self):
        if self.sympy_expr.func in [sympy.Add, sympy.Mul]:
            return True
        return False
