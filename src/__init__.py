from sympy import *
from sympy.core.function import UndefinedFunction
from sympy.parsing.sympy_parser import parse_expr

a = parse_expr("derivative(x)", evaluate=False)

left = parse_expr("f(x) + 1")
right = parse_expr("1 + f(x)")

input = parse_expr("x + 1")

if input.func == left.func:
    if input.is_commutative:
        print("is commutative")
        # argument combinations
    else:
        print("is not commutative")


def user_defined_function_match(structure, expression):
    print(structure.func)
    for free_symbol in expression.expr_free_symbols:
        if free_symbol.func == Symbol:
            if not structure.has(free_symbol):
                return False
    return True


def compare_user_defined_function(structure, expression, equalities):
    print("comparing user defined function")
    if user_defined_function_match(structure, expression):
        return ComparisonResult(True, equalities + [[structure, expression]])
    else:
        return ComparisonResult(False, [])


def is_user_defined_function(structure):
    return isinstance(structure.func, UndefinedFunction)


def compare_children_combinations(children_pairs, equalities):
    result = ComparisonResult(True, [])
    for pair in children_pairs:
        children_comparison_result = compare_rec(pair.structure_child, pair.expression_child, equalities)
        result.structures_match &= children_comparison_result.structures_match
        result.equalities += children_comparison_result.equalities
    return result


def compare_sympy_expression(structure, expression, equalities):
    if structure.func == expression.func and len(structure.args) == len(expression.args):
        if structure.is_commutative:
            print("is cummulative")
            pairs_to_compare = get_children_pairs(structure.args, expression.args)
            for children_pairs in pairs_to_compare:
                comparison = compare_children_combinations(children_pairs, equalities)
                if comparison.structures_match:
                    return comparison
        else:
            print("comparing non commutative")
            pairs_to_compare = get_equivalent_children_pairs(len(structure), structure.args, expression.args)
            return compare_children_combinations(pairs_to_compare, equalities)

    return ComparisonResult(False, [])

class ComparisonPair:
    def __init__(self, structure_child, expression_child):
        self.structure_child = structure_child
        self.expression_child = expression_child

def get_equivalent_children_pairs(length, structure_children, expression_children):
    comparison_pairs = []
    for i in range(0, length):
        comparison_pairs .append(ComparisonPair(structure_children[i], expression_children[i]))
    return comparison_pairs


def both_nodes_are_leaves(structure, expression):
    return len(structure.args) == len(expression.args) and len(structure.args) == 0


def compare_rec(structure, expression, equalities):
    # compare types
    # number of arguments
    # if passes compare children in case that is commutative then do cross comparisons
    # else handle
    if both_nodes_are_leaves(structure, expression):
        return ComparisonResult(structure == expression, equalities)

    if is_user_defined_function(structure):
        return compare_user_defined_function(structure, expression, equalities)
    else:
        return compare_sympy_expression(structure, expression, equalities)


def get_children_pairs(structure_children, expression_children):
    return get_children_pairs_rec(structure_children, expression_children, [], [])


def get_children_pairs_rec(structure_children, expression_children, accum, possibles):
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
        possibles = get_children_pairs_rec(structure_children_without_first, expression_children_without_child, new_accum, possibles)

    return possibles


def compare(structure, expression):
    return compare_rec(structure, expression, [])


class HistoryItem:
    def __init__(self, expression, theorem_applied):
        self.expression = expression
        self.theorem_applied = theorem_applied


class Theorem:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right


class ComparisonResult:
    def __init__(self, structures_match, equalities):
        self.structures_match = structures_match
        self.equalities = equalities


class TransformationResult:
    def __init__(self, expression, theorem_used):
        self.expression = expression
        self.theorem_used = theorem_used


def replace_structure_expressions(structure, equalities):
    new_expression = structure
    for equality in equalities:
        new_expression = new_expression.subs({equality[0]: equality[1]})
    return new_expression


def transform(expression, theorems, history):
    for theo in theorems:
        comparison = compare(theo.left, expression)
        if comparison.structures_match:
            new_step = replace_structure_expressions(theo.right, comparison.equalities)
            if not new_step in history:
                return TransformationResult(new_step, theo)
    return TransformationResult(expression, None)


def get_solution_if_possible(input, theorems):
    solved = False
    history = []
    current_step = input
    while not solved:
        next_possible_step = transform(current_step, theorems, history)
        if current_step != next_possible_step.expression:
            history.append(HistoryItem(next_possible_step.expression, next_possible_step.theorem_used))
            current_step = next_possible_step.expression
        else:
            break
    return history


input = parse_expr("Derivative(x + x, x)", evaluate=False)
theorems = [
    Theorem("derivada de la suma", parse_expr("Derivative(f(x) + g(x) , x)"),
            parse_expr("Derivative(f(x), x) + Derivative(g(x), x)"))
]
b = get_solution_if_possible(input, theorems)

print("partiendo de: ")
print(input)
for item in b:
    print("aplico " + item.theorem_applied.name + " y obtengo como resultado:")
    print(item.expression)
