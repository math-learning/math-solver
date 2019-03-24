from sympy import *
from sympy.parsing.sympy_parser import parse_expr

from src.model.Theorem import Theorem
from src.services.ComparatorService import ComparatorService
from src.services.DerivativesService import DerivativeApplyItem, DerivativeApplier
from src.utils.PrintUtils import PrintUtils


def main():
    input = parse_expr("Derivative(x + x * x, x)", evaluate=False)

    theorems = [
        Theorem("derivada de la suma", parse_expr("Derivative(f(x) + g(x) , x)"),
                parse_expr("Derivative(f(x), x) + Derivative(g(x), x)")),

        Theorem("derivada del producto", parse_expr("Derivative(f(x) * g(x) , x)"),
                parse_expr("Derivative(f(x), x) * g(x) + Derivative(g(x), x) * f(x)")),

        Theorem("derivada de la division", parse_expr("Derivative(f(x) / g(x) , x)"),
                parse_expr("Derivative(( f(x), x) * g(x) - Derivative(g(x), x) * f(x)) / ( g(x)** 2)")),
    ]

    comparator = ComparatorService()

    b = comparator.get_solution_if_possible(input, theorems)

    printer = PrintUtils()

    printer.solution(input, b)

    #derivativeApplier = DerivativeApplier()
    # der = derivativeApplier.apply_derivatives(b[-1].expression)
    # derivativeApplier.printDerivatives(der)

    # for item in apply_derivatives(a):
    #     print("Before: ")
    #     print(item.before)
    #     print("After: ")
    #     print(item.after)

main()