from mathlearning.model.expression import Expression


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
                lambda expression_string: Expression(expression_string, is_latex=False),
                self.steps_non_latex
            )
        )

    def as_expressions(self, list_to_convert, is_latex):
        return list(
            map(
                lambda expression_string: Expression(expression_string, is_latex=is_latex),
                list_to_convert
            )
        )



class SolvedExercises:

    @staticmethod
    def derivative_e_plus_sin() -> SolvedExercise:
        name = "e + sen"
        steps = [
            "\\frac{d\\left(e^x.\\ x\\right)}{dx}\\ +\\ \\frac{d\\left(sen\\left(x\\right)\\cdot x^2\\right)}{dx}",
            "\\frac{d\\left(e^x\\right)}{dx}\\cdot x\\ +\\ \\frac{d\\left(x\\right)}{dx}\\cdot e^x\\ +\\ \\frac{d\\left(\\sin \\left(x\\right)\\cdot x^2\\right)}{dx}",
            "e^x\\cdot x\\ +\\ \\frac{d\\left(x\\right)}{dx}\\cdot e^x\\ +\\ \\frac{d\\left(\\sin \\left(x\\right)\\cdot x^2\\right)}{dx}",
            "e^x\\cdot x\\ +\\ e^x\\ +\\ \\frac{d\\left(\\sin \\left(x\\right)\\cdot x^2\\right)}{dx}",
            "e^x\\cdot x\\ +\\ e^x\\ +\\ \\frac{d\\left(\\sin \\left(x\\right)\\right)}{dx}\\cdot x^2+\\sin \\left(x\\right)\\cdot \\frac{d\\left(x^2\\right)}{dx}",
            "e^x\\cdot x\\ +\\ e^x\\ +\\ \\frac{d\\left(\\sin \\left(x\\right)\\right)}{dx}\\cdot x^2+\\sin \\left(x\\right)\\cdot 2\\ \\cdot x",
            "e^x\\cdot x\\ +\\ e^x\\ +\\ \\cos \\left(x\\right)\\cdot x^2+\\sin \\left(x\\right)\\cdot 2\\ \\cdot x",
            "e^x\\cdot \\left(1\\ +x\\right)+\\ \\cos \\left(x\\right)\\cdot x^2+\\sin \\left(x\\right)\\cdot 2\\ \\cdot x"
        ]

        non_result_steps = steps[:len(steps) - 2]

        result = "e^x\\cdot \\left(1\\ +x\\right)+\\ \\cos \\left(x\\right)\\cdot x^2+\\sin \\left(x\\right)\\cdot 2\\ \\cdot x"

        steps_non_latex = [
            "Derivative(x*exp(x), x) + Derivative(x**2*sin(x), x)",
            "x*Derivative(exp(x), x) + exp(x)*Derivative(x, x) + Derivative(x**2*sin(x), x)",
            "x*exp(x) + exp(x)*Derivative(x, x) + Derivative(x**2*sin(x), x)",
            "x*exp(x) + exp(x) + Derivative(x**2*sin(x), x)",
            "x*exp(x) + exp(x) + x**2 * Derivative(sin(x), x) + sin(x) * Derivative(x**2, x)",
            "x*exp(x) + exp(x) + x**2 * Derivative(sin(x), x) + sin(x) * 2 * x",
            "x**2*cos(x) + x*2*sin(x) + (x + 1)*exp(x)"
        ]

        result_non_latex = "x**2*cos(x) + x*(2*sin(x)) + (x + 1)*exp(x)"

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def derivative_sin_divided_by_cos() -> SolvedExercise:
        name = "sen / cos"
        steps = [
            "\\frac{d(\\frac{sen(x)}{\\cos(x)})} {dx}",
            "\\frac{\\frac{d\\left(sen\\left(x\\right)\\right)}{dx}\\cdot \\cos \\left(x\\right)\\ -\\ sen\\left(x\\right)\\ \\cdot \\ \\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}}{\\cos ^2\\left(x\\right)}",
            "\\frac{\\cos^2\\left(x\\right)\\ +\\ sen^2\\left(x\\right)\\ }{\\cos ^2\\left(x\\right)}",
            "\\frac{1}{\\cos^2\\left(x\\right)}"
        ]
        result = "\\frac{1}{\\cos^2\\left(x\\right)}"

        non_result_steps = steps[:len(steps) - 2]

        steps_non_latex = [
            "Derivative(sin(x)/cos(x), x)",
            "(-sin(x)*Derivative(cos(x), x) + cos(x)*Derivative(sin(x), x))/cos(x)**2",
            "(sin(x)**2 + cos(x)**2)/cos(x)**2",
            "1/(cos(x)**2)"
        ]

        result_non_latex = "1/(cos(x)**2)"

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def sum_derivative_x2_derivative_sum_x_cos() -> SolvedExercise:
        name = "deriv x**2 + dervi suma x + cos"

        steps = [
            "\\frac{d\\left(x^2\\right)}{dx}+\\frac{d\\left(x\\ +\\cos \\left(x\\right)\\right)}{dx}",
            "\\frac{d\\left(x^2\\right)}{dx}+\\frac{d\\left(x\\right)}{dx}+\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}",
            "2\\cdot x+\\frac{d\\left(x\\right)}{dx}+\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}",
            "2\\cdot x+1+\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}",
            "2\\cdot x+1-\\sin \\left(x\\right)"
        ]
        result = "2\\cdot x+1-\\sin \\left(x\\right)"

        non_result_steps = steps[:len(steps) - 1]

        result_non_latex = "2*x + 1 - sin(x)"
        steps_non_latex = [
            "Derivative(x**2, x) + Derivative(x + cos(x), x)",
            "Derivative(x, x) + Derivative(x**2, x) + Derivative(cos(x), x)",
            "2*x + Derivative(x, x) + Derivative(cos(x), x)",
            "2*x + 1 + Derivative(cos(x), x)",
            "2*x + 1 - sin(x)"
        ]

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)


    @staticmethod
    def derivative_mult_of_three_elem() -> SolvedExercise:
        name = "multiplication of 3 elem"

        steps = [
            "x^2\\sin (x)\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}+\\cos (x)\\frac{d\\left(x^2\\sin (x)\\right)}{dx}",
            "x^2\\sin (x)\\ \\left(-\\sin \\left(x\\right)\\right)+\\cos (x)\\frac{d\\left(x^2\\sin (x)\\right)}{dx}",
            "-\\ x^2\\sin ^2(x)\\ +\\cos (x)\\frac{d\\left(x^2\\sin (x)\\right)}{dx}",
            '- x^{2} \\sin^{2}{\\left(x \\right)} + \\left(x^{2} \\frac{d}{d x} \\sin{\\left(x \\right)} + \\sin(x) \\frac{d}{d x} x^{2}\\right) \\cos{\\left(x \\right)}',
            '- x^{2} \\sin^{2}{\\left(x \\right)} + \\left(x^{2} \\frac{d}{d x} \\sin{\\left(x \\right)} + 2 x \\sin{\\left(x \\right)}\\right) \\cos{\\left(x \\right)}',
            '- x^{2} \\sin^{2}{\\left(x \\right)} + \\left(x^{2} \\cos{\\left(x \\right)} + 2 x \\sin{\\left(x \\right)}\\right) \\cos{\\left(x \\right)}'
        ]

        result = '- x^{2} \\sin^{2}{\\left(x \\right)} + \\left(x^{2} \\cos{\\left(x \\right)} + 2 x \\sin{\\left(x \\right)}\\right) \\cos{\\left(x \\right)}'

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
            "x**2*(sin(x)*Derivative(cos(x), x)) + cos(x)*Derivative(x**2*sin(x), x)",
            "x**2*((-sin(x))*sin(x)) + cos(x)*Derivative(x**2*sin(x), x)",
            "-x**2*sin(x)**2 + cos(x)*Derivative(x**2*sin(x), x)",
            "-x**2*sin(x)**2 + (x**2*Derivative(sin(x), x) + sin(x)*Derivative(x**2, x))*cos(x)",
            "-x**2*sin(x)**2 + (x**2*Derivative(sin(x), x) + sin(x)* 2 * x)*cos(x)",
            "-x**2*sin(x)**2 + (x**2*cos(x) + sin(x)* 2 * x)*cos(x)"
        ]

        result_non_latex = "x**2*(- sin(x)**2) + (x**2*cos(x) + sin(x)* 2 * x)*cos(x)"

        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)


    # INTEGRAL EXERCISES

    @staticmethod
    def integral_add_x_cosx() -> SolvedExercise:
        name = "sum of two integrals"

        steps = [
            '\\int (x + \\cos(x)) dx',
            '\\int (x) dx + \\int (\\cos(x)) dx',
            'x^2 / 2 + \\int (\\cos(x)) dx',
            'x^2 / 2 + \\sin(x)',
        ]

        result = 'x^2 / 2 + sin(x)'

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [
            'Integral(x+ cos(x),x)',
            'Integral(x,x) + Integral(cos(x),x)',
            'x**2 / 2 + Integral(cos(x),x)',
            'x**2 / 2 + sin(x)',
        ]

        result_non_latex = 'x**2 / 2 + sin(x)'
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def integral_parts_mult_x_cosx():
        name = "parts rule mult cosx and x"

        # TODO: check again the steps
        steps = [
            '\\int (x * \\cos(x)) dx',
            '\\int (u(x) * \\frac{v(x)}{dx}) dx', # TODO think if this step should be included
            'u(x) * v(x) - \\int (\\frac{d(u(x))}{dx} * v(x)) dx', # u = x; v = sin(x)
            'x * \\sin(x) - \\int (\\frac{d(x)}{dx} * \\sin(x)) dx',
            'x * \\sin(x) - \\int (1 * \\sin(x)) dx',
            'x * \\sin(x) - \\int (\\sin(x)) dx',
            'x*\\sin(x) + \\cos(x)'
        ]

        result = 'x*\\sin(x) + \\cos(x)'

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [

        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)

    @staticmethod
    def integral_substitution():
        #   TODO
        name = "substitution"

        steps = [
            '\\int ( x^2 / (\\sqrt[3]{1+2x}) ) dx', # 1+2x = t^3 => x = ( t^3 - 1 ) / 2 ; 2dx = 3t^2 dt dx = (3t^2 dt)/2
            '\\int ( \\frac{ (( t^3 - 1 ) / 2)^2}{t} * (3*t^2)/2 ) dt',
            '(3/2) * \\int ( (t^6-2t^3+1)/4 *t ) dt',
            '3/8 * (\\int (t^7 - 2t^4 + t) dt)',
            '3/8 * (\\int (t^7) dt - \\int( 2t^4 + t) dt)',
            '3/8 * (\\int (t^7) dt - \\int( 2t^4) dt + \\int (t) dt)',
            '3/8 * (\\int (t^7) dt - \\int( 2t^4) dt + t^2/2)',
            '3/8 * (\\int (t^7) dt - 2t^5/5 + t^2/2)',
            '3/8 * (t^8/8 - 2t^5/5 + t^2/2)', # t = \\sqrt[3]{1 +2x}
            '3/8 * ((\\sqrt[3]{1 +2x})^8/8 - 2(\\sqrt[3]{1 +2x})^5/5 + (\\sqrt[3]{1 +2x})^2/2)',
            '3/64 * (\\sqrt[3]{1 +2x})^8 - 6/40 * (\\sqrt[3]{1 +2x})^5 + 3/16 *(\\sqrt[3]{1 +2x})^2',
            '3/64 * (\\sqrt[3]{1 +2x})^8 - 3/20 * (\\sqrt[3]{1 +2x})^5 + 3/16 *(\\sqrt[3]{1 +2x})^2',
        ]

        result = '3/64 * (\\sqrt[3]{1 +2x})^8 - 3/20 * (\\sqrt[3]{1 +2x})^5 + 3/16 *(\\sqrt[3]{1 +2x})^2'

        non_result_steps = steps[:len(steps) - 1]

        steps_non_latex = [

        ]

        result_non_latex = ''
        return SolvedExercise(name, steps, result, non_result_steps, result_non_latex, steps_non_latex)
