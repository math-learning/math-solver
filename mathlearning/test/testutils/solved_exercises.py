from mathlearning.model.expression import Expression
from mathlearning.model.expression_variable import ExpressionVariable


class SolvedExercise:
    def __init__(self, name: str, steps: list, result: str, non_result_steps: list,
                 result_non_latex: str = None, steps_non_latex: list = None):
        self.name = name
        self.steps = steps
        self.result = result
        self.result_non_latex = result_non_latex
        self.steps_non_latex = steps_non_latex
        self.non_result_steps = non_result_steps

    def get_results_as_expressions(self):
        return list(
            map(
                lambda step: Expression(step['expression'], step['variables'], is_latex=False),
                self.steps_non_latex
            )
        )
    @staticmethod
    def as_expressions(list_to_convert, is_latex=True):
        return list(
            map(
                lambda expression_string: Expression(expression_string['expression'], is_latex=is_latex),
                list_to_convert
            )
        )



class SolvedExercises:

    @staticmethod
    def derivative_e_plus_sin() -> SolvedExercise:
        name = "e + sen"
        steps = [
            {'expression': '\\frac{d(e^x.\\ x)}{dx}\\ +\\ \\frac{d(sen(x)* x^2)}{dx}', 'variables': []},
            {'expression': '\\frac{d(e^x)}{dx}* x\\ +\\ \\frac{d(x)}{dx}* e^x\\ +\\ \\frac{d(\\sin(x)* x^2)}{dx}', 'variables': []},
            {'expression': 'e^x* x\\ +\\ \\frac{d(x)}{dx}* e^x\\ +\\ \\frac{d(\\sin(x)* x^2)}{dx}', 'variables': []},
            {'expression': 'e^x* x\\ +\\ e^x\\ +\\ \\frac{d(\\sin(x)* x^2)}{dx}', 'variables': []},
            {'expression': 'e^x* x\\ +\\ e^x\\ +\\ \\frac{d(\\sin(x))}{dx}* x^2+\\sin(x)* \\frac{d(x^2)}{dx}', 'variables': []},
            {'expression': 'e^x* x\\ +\\ e^x\\ +\\ \\frac{d(\\sin(x))}{dx}* x^2+\\sin(x)* 2\\ * x', 'variables': []},
            {'expression': 'e^x* x\\ +\\ e^x\\ +\\ \\cos(x)* x^2+\\sin(x)* 2\\ * x', 'variables': []},
            {'expression': 'e^x* (1\\ +x)+\\ \\cos(x)* x^2+\\sin(x)* 2\\ * x', 'variables': []}
        ]

        non_result_steps = steps[:len(steps) - 2]

        result = {'expression': 'e^x* (1\\ +x)+\\ \\cos(x)* x^2+\\sin(x)* 2\\ * x', 'variables': []}

        steps_non_latex = [
            {'expression': 'Derivative(x*exp(x), x) + Derivative(x**2*sin(x), x)', 'variables': []},
            {'expression': 'x*Derivative(exp(x), x) + exp(x)*Derivative(x, x) + Derivative(x**2*sin(x), x)', 'variables': []},
            {'expression': 'x*exp(x) + exp(x)*Derivative(x, x) + Derivative(x**2*sin(x), x)', 'variables': []},
            {'expression': 'x*exp(x) + exp(x) + Derivative(x**2*sin(x), x)', 'variables': []},
            {'expression': 'x*exp(x) + exp(x) + x**2 * Derivative(sin(x), x) + sin(x) * Derivative(x**2, x)', 'variables': []},
            {'expression': 'x*exp(x) + exp(x) + x**2 * Derivative(sin(x), x) + sin(x) * 2 * x', 'variables': []},
            {'expression': 'x**2*cos(x) + x*2*sin(x) + (x + 1)*exp(x)', 'variables': []}
        ]

        result_non_latex = {'expression': 'x**2*cos(x) + x*(2*sin(x)) + (x + 1)*exp(x)', 'variables': []}

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def derivative_sin_divided_by_cos() -> SolvedExercise:
        name = "sen / cos"
        steps = [
            {'expression': '\\frac{d(\\frac{sen(x)}{\\cos(x)})} {dx}', 'variables': []},
            {'expression': '\\frac{\\frac{d(sen(x))}{dx}* \\cos(x)\\ -\\ sen(x)\\ * \\ \\frac{d(\\cos(x))}{dx}}{\\cos ^2(x)}', 'variables': []},
            {'expression': '\\frac{\\cos^2(x)\\ +\\ sen^2(x)\\ }{\\cos ^2(x)}', 'variables': []},
            {'expression': '\\frac{1}{\\cos^2(x)}', 'variables': []}
        ]
        result = {'expression': '\\frac{1}{\\cos^2(x)}', 'variables': []}

        non_result_steps = steps[:len(steps) - 2]

        steps_non_latex = [
            {'expression': 'Derivative(sin(x)/cos(x), x)', 'variables': []},
            {'expression': '(-sin(x)*Derivative(cos(x), x) + cos(x)*Derivative(sin(x), x))/cos(x)**2', 'variables': []},
            {'expression': '(sin(x)**2 + cos(x)**2)/cos(x)**2', 'variables': []},
            {'expression': '1/(cos(x)**2)', 'variables': []}
        ]

        result_non_latex = {'expression': '1/(cos(x)**2)', 'variables': []}

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def sum_derivative_x2_derivative_sum_x_cos() -> SolvedExercise:
        name = "deriv x**2 + dervi suma x + cos"

        steps = [
            {'expression': '\\frac{d(x^2)}{dx}+\\frac{d(x\\ +\\cos(x))}{dx}', 'variables': []},
            {'expression': '\\frac{d(x^2)}{dx}+\\frac{d(x)}{dx}+\\frac{d(\\cos(x))}{dx}', 'variables': []},
            {'expression': '2* x+\\frac{d(x)}{dx}+\\frac{d(\\cos(x))}{dx}', 'variables': []},
            {'expression': '2* x+1+\\frac{d(\\cos(x))}{dx}', 'variables': []},
            {'expression': '2* x+1-\\sin(x)', 'variables': []}
        ]
        result = {'expression': '2  * x+1-\\sin(x)', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        result_non_latex = {'expression': '2*x + 1 - sin(x)', 'variables': []}
        steps_non_latex = [
            {'expression': 'Derivative(x**2, x) + Derivative(x + cos(x), x)', 'variables': []},
            {'expression': 'Derivative(x, x) + Derivative(x**2, x) + Derivative(cos(x), x)', 'variables': []},
            {'expression': '2*x + Derivative(x, x) + Derivative(cos(x), x)', 'variables': []},
            {'expression': '2*x + 1 + Derivative(cos(x), x)', 'variables': []},
            {'expression': '2*x + 1 - sin(x)', 'variables': []}
        ]

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)


    @staticmethod
    def derivative_mult_of_three_elem() -> SolvedExercise:
        name = "multiplication of 3 elem"

        steps = [
            {'expression': 'x^2\\sin(x)\\frac{d(\\cos(x))}{dx}+\\cos(x)\\frac{d(x^2\\sin(x))}{dx}', 'variables': []},
            {'expression': 'x^2\\sin(x)\\ (-\\sin(x))+\\cos(x)\\frac{d(x^2\\sin(x))}{dx}', 'variables': []},
            {'expression': '-\\ x^2\\sin ^2(x)\\ +\\cos(x)\\frac{d(x^2\\sin(x))}{dx}', 'variables': []},
            {'expression': '- x^{2} \\sin^{2}{(x )} + (x^{2} \\frac{d}{d x} \\sin{(x )} + \\sin(x) \\frac{d}{d x} x^{2}) \\cos{(x )}', 'variables': []},
            {'expression': '- x^{2} \\sin^{2}{(x )} + (x^{2} \\frac{d}{d x} \\sin{(x )} + 2 x \\sin{(x )}) \\cos{(x )}', 'variables': []},
            {'expression': '- x^{2} \\sin^{2}{(x )} + (x^{2} \\cos{(x )} + 2 x \\sin{(x )}) \\cos{(x )}', 'variables': []}
        ]

        result = {'expression': '- x^{2} \\sin^{2}{(x )} + (x^{2} \\cos{(x )} + 2 x \\sin{(x )}) \\cos{(x )}', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
            {'expression': 'x**2*(sin(x)*Derivative(cos(x), x)) + cos(x)*Derivative(x**2*sin(x), x)', 'variables': []},
            {'expression': 'x**2*((-sin(x))*sin(x)) + cos(x)*Derivative(x**2*sin(x), x)', 'variables': []},
            {'expression': '-x**2*sin(x)**2 + cos(x)*Derivative(x**2*sin(x), x)', 'variables': []},
            {'expression': '-x**2*sin(x)**2 + (x**2*Derivative(sin(x), x) + sin(x)*Derivative(x**2, x))*cos(x)', 'variables': []},
            {'expression': '-x**2*sin(x)**2 + (x**2*Derivative(sin(x), x) + sin(x)* 2 * x)*cos(x)', 'variables': []},
            {'expression': '-x**2*sin(x)**2 + (x**2*cos(x) + sin(x)* 2 * x)*cos(x)', 'variables': []}
        ]

        result_non_latex = {'expression': "x**2*(- sin(x)**2) + (x**2*cos(x) + sin(x)* 2 * x)*cos(x)", 'variables': []}

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)


    # INTEGRAL EXERCISES ---------------------------------------------------------------------

    @staticmethod
    def integral_add_x_cosx() -> SolvedExercise:
        name = "sum of two integrals"

        steps = [
            {'expression': '\\int x + \\cos(x) dx', 'variables': []},
            {'expression': '(\\int x dx) + (\\int \\cos(x) dx)', 'variables': []},
            {'expression': 'x^2 / 2 + \\int (\\cos(x)) dx', 'variables': []},
            {'expression': 'x^2 / 2 + \\sin(x)', 'variables': []}
        ]

        result = {'expression': 'x^2 / 2 + sin(x)', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
            {'expression': 'Integral(x+ cos(x),x)', 'variables': []},
            {'expression': 'Integral(x,x) + Integral(cos(x),x)', 'variables': []},
            {'expression': 'x**2 / 2 + Integral(cos(x),x)', 'variables': []},
            {'expression': 'x**2 / 2 + sin(x)', 'variables': []}
        ]

        result_non_latex = {'expression': 'x**2 / 2 + sin(x)', 'variables': []}
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)


    @staticmethod
    def integral_substitution_division_of_polynomials():
        #   TODO
        name = "substitution"

        steps = [
            {'expression': '\\int ( x^2 / (\\sqrt[3]{1+2x}) ) dx', 'variables': []}, # 1+2x = t^3 => x = ( t^3 - 1 ) / 2 ; 2dx = 3t^2 dt dx = (3t^2 dt)/2
            {'expression': '\\int ( \\frac{ (( t^3 - 1 ) / 2)^2}{t} * (3*t^2)/2 ) dt', 'variables': []},
            {'expression': '(3/2) * \\int ( (t^6-2t^3+1)/4 *t ) dt', 'variables': []},
            {'expression': '3/8 * (\\int (t^7 - 2t^4 + t) dt)', 'variables': []},
            {'expression': '3/8 * (\\int (t^7) dt - \\int( 2t^4 + t) dt)', 'variables': []},
            {'expression': '3/8 * (\\int (t^7) dt - \\int( 2t^4) dt + \\int (t) dt)', 'variables': []},
            {'expression': '3/8 * (\\int (t^7) dt - \\int( 2t^4) dt + t^2/2)', 'variables': []},
            {'expression': '3/8 * (\\int (t^7) dt - 2t^5/5 + t^2/2)', 'variables': []},
            {'expression': '3/8 * (t^8/8 - 2t^5/5 + t^2/2)', 'variables': []}, # t = \\sqrt[3]{1 +2x}
            {'expression': '3/8 * ((\\sqrt[3]{1 +2x})^8/8 - 2(\\sqrt[3]{1 +2x})^5/5 + (\\sqrt[3]{1 +2x})^2/2)', 'variables': []},
            {'expression': '3/64 * (\\sqrt[3]{1 +2x})^8 - 6/40 * (\\sqrt[3]{1 +2x})^5 + 3/16 *(\\sqrt[3]{1 +2x})^2', 'variables': []},
            {'expression': '3/64 * (\\sqrt[3]{1 +2x})^8 - 3/20 * (\\sqrt[3]{1 +2x})^5 + 3/16 *(\\sqrt[3]{1 +2x})^2', 'variables': []}
        ]

        result = {'expression': '3/64 * (\\sqrt[3]{1 +2x})^8 - 3/20 * (\\sqrt[3]{1 +2x})^5 + 3/16 *(\\sqrt[3]{1 +2x})^2', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [

        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def integral_substitution_sin_with_polynomials() -> SolvedExercise:
        # TODO check why the result is different
        name = "sin with polynomials"

        steps = [
            {'expression': '\\int(\\sin(3*x + 5))dx', 'variables': []},# u = 3x+5 du=3dx
            {'expression': '\\int(\\sin(3*x + 5))dx', 'variables': [
                ExpressionVariable('u(x)', Expression('3x+5')).to_json()
            ]},  # u = 3x+5 du=3dx
            {'expression': '1/3 * \\int(\\sin(3x+5)) * 3 dx', 'variables': []},
            {'expression': '1/3 * \\int(\\sin(u)) * du', 'variables': []},
            {'expression': '- 1/3 * \\cos(u)', 'variables': []},
            {'expression': '- 1/3 * \\cos(3x+5)', 'variables': []}
        ]

        result = {'expression': '- 1/3 * \\cos(3x+5)', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def integral_substitution_multiplication() -> SolvedExercise:
        name = "substitution multiplication"

        steps = [
            {'expression': '\\int(2 * x \\sqrt[2]{1+x^2}) dx', 'variables': []},  # u = 1+x^2 du=2x dx
            {'expression': '\\int(\\sqrt[2]{u}) du', 'variables': []},
            {'expression': '2/3 * u^{3/2}', 'variables': []},
            {'expression': '2/3 * (1+x^2)^{3/2}', 'variables': []}
        ]

        result = {'expression': '2/3 * (1+x^2)^{3/2}', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def integral_parts_mult_x_cosx():
        name = "parts rule mult cosx and x"

        # TODO: check again the steps
        steps = [
            {'expression': '\\int (x * \\cos(x)) dx', 'variables': []},
            {'expression': '\\int (u(x) * \\frac{d(v(x))}{dx}) dx',
             'variables': [
                 ExpressionVariable('u(x)', Expression('x')).to_json(),
                 ExpressionVariable('v(x)', Expression('\\sin(x)')).to_json()
             ]
             },
            {'expression': 'u(x) * v(x) - \\int (\\frac{d(u(x))}{dx} * v(x)) dx',
             'variables': [
                 ExpressionVariable('u(x)', Expression('x')).to_json(),
                 ExpressionVariable('v(x)', Expression('\\sin(x)')).to_json()
             ]
             },
            {'expression': 'x * \\sin(x) - \\int (\\frac{d(x)}{dx} * \\sin(x)) dx', 'variables': []},
            {'expression': 'x * \\sin(x) - \\int (1 * \\sin(x)) dx', 'variables': []},
            {'expression': 'x * \\sin(x) - \\int (\\sin(x)) dx', 'variables': []},
            {'expression': 'x*\\sin(x) + \\cos(x)', 'variables': []}
        ]

        result = {'expression': 'x*\\sin(x) + \\cos(x)', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [

        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    # https://www.intmath.com/methods-integration/7-integration-by-parts.php
    @staticmethod
    def integral_parts_example_one():
        name = "parts example one"

        steps = [
            {'expression': '\\int( x * \\sin(2*x)) dx', 'variables': []},  # u = x  dv = sin(2x) dx ; v -cos(2x)/2
            {'expression': '\\int (u(x) * \\frac{d(v(x))}{dx}) dx', 'variables': [
                ExpressionVariable('u(x)', Expression('x')).to_json(),
                ExpressionVariable('v(x)', Expression('-cos(2x)/2')).to_json()
            ]}, # TODO think if this step should be included
            {'expression': 'u(x) * v(x) - \\int (\\frac{d(u(x))}{dx} * v(x)) dx', 'variables': [
                ExpressionVariable('u(x)', Expression('x')).to_json(),
                ExpressionVariable('v(x)', Expression('-cos(2x)/2')).to_json()
            ]},
            {'expression': 'x * (- \\cos(2x)/2) - \\int (\\frac{d(x)}{dx} * (-\\cos(2x)/2) ) dx', 'variables': []},
            {'expression': 'x * (- \\cos(2x)/2) - \\int ( 1 * (-\\cos(2x)/2) ) dx', 'variables': []},
            {'expression': 'x * (- \\cos(2x)/2) - \\int ((-\\cos(2x)/2) ) dx', 'variables': []},
            {'expression': 'x * (- \\cos(2x)/2) + 1/2 * \\int (\\cos(2x) ) dx', 'variables': []},
            {'expression': 'x * (- \\cos(2x)/2) + 1/2 * \\sin(2x)/2', 'variables': []}
        ]

        result = {'expression': 'x * (- \\cos(2x)/2) + 1/2 * \\sin(2x)/2', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def integral_parts_example_two():
        name = "parts example two"

        steps = [
            {'expression': '\\int ( x * \\sqrt[2]{x+1} ) dx', 'variables': []},
            {'expression': '\\int (u(x) * \\frac{d(v(x))}{dx}) dx', 'variables': [
                ExpressionVariable('u(x)', Expression('x')).to_json(),
                ExpressionVariable('v(x)', Expression('(2/3 * (x+1)^{3/2})')).to_json()
            ]},  # TODO think if this step should be included
            {'expression': 'u(x) * v(x) - \\int (\\frac{d(u(x))}{dx} * v(x)) dx', 'variables': [
                ExpressionVariable('u(x)', Expression('x')).to_json(),
                ExpressionVariable('v(x)', Expression('(2/3 * (x+1)^{3/2})')).to_json()
            ]},
            {'expression': 'x * (2/3 * (x+1)^{3/2}) - \\int (2/3 * (x+1)^{3/2}) dx', 'variables': []},
            {'expression': 'x * (2/3 * (x+1)^{3/2}) - 2/3 * \\int ((x+1)^{3/2}) dx', 'variables': []},
            # {'expression': 'x * (2/3 * (x+1)^{3/2}) - 2/3 * 2/5 * (x+1)^{5/2}', 'variables': []},
            {'expression': 'x * (2/3 * (x+1)^{3/2}) - 4/15 * (x+1)^{5/2}', 'variables': []}
        ]

        result = {'expression': 'x * (2/3 * (x+1)^{3/2}) - 4/15 * (x+1)^{5/2}', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def integral_parts_example_six():
        name = "parts example six"

        steps = [
            {'expression': '\\int (\\ln(x)) dx', 'variables': []},
            {'expression': '\\int (u(x) * \\frac{d(v(x))}{dx}) dx', 'variables': [
                {'tag': 'u(x)', 'expression': {'expression': '\\ln(x)', 'variables': []}},
                {'tag': 'v(x)', 'expression': {'expression': 'x', 'variables': []}}
            ]},  # TODO think if this step should be included
            {'expression': 'u(x) * v(x) - \\int (\\frac{d(u(x))}{dx} * v(x)) dx', 'variables': [
                {'tag': 'u(x)', 'expression': {'expression': '\\ln(x)', 'variables': []}},
                {'tag': 'v(x)', 'expression': {'expression': 'x', 'variables': []}}
            ]},
            {'expression': '\\ln(x) * x - \\int (\\frac{d(\\ln(x))}{dx} * x ) dx', 'variables': []},
            # {'expression': '\\ln(x) * x - \\int (\\frac{1}{x} * x ) dx', 'variables': []},
            {'expression': '\\ln(x) * x - \\int (1) dx', 'variables': []},
            {'expression': '\\ln(x) * x - x', 'variables': []}
        ]

        result = {'expression': '\\ln(x) * x - x', 'variables': []}

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)
