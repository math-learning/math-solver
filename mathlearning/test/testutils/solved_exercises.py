from mathlearning.model.expression import Expression


class SolvedExercise:
    def __init__(self, name: str, steps: list, result: str):
        self.name = name
        self.steps = steps
        self.result = result


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
        result = "e^x\\cdot \\left(1\\ +x\\right)+\\ \\cos \\left(x\\right)\\cdot x^2+\\sin \\left(x\\right)\\cdot 2\\ \\cdot x"
        return SolvedExercise(name, steps, result)

    @staticmethod
    def derivative_sin_divided_by_cos() -> SolvedExercise:
        name = "sen / cos"
        steps = [
            "\\frac{d(\\frac{sen(x)}{cos(x)})} {dx}",
            "\\frac{\\frac{d\\left(sen\\left(x\\right)\\right)}{dx}\\cdot \\cos \\left(x\\right)\\ -\\ sen\\left(x\\right)\\ \\cdot \\ \\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}}{\\cos ^2\\left(x\\right)}",
            "\\frac{\\cos^2\\left(x\\right)\\ +\\ sen^2\\left(x\\right)\\ }{\\cos ^2\\left(x\\right)}",
            "\\frac{1}{\\cos^2\\left(x\\right)}"
        ]
        result = "\\frac{1}{\\cos^2\\left(x\\right)}"
        return SolvedExercise(name, steps, result)

    @staticmethod
    def sum_derivative_x2_derivative_sum_x_cos() -> SolvedExercise:
        name = "deriv x**2 + dervi suma x + cos"
        steps = [
            "{d\\left(x^2\\right)}{dx}+\\frac{d\\left(x\\ +\\cos \\left(x\\right)\\right)}{dx}",
            "\\frac{d\\left(x^2\\right)}{dx}+\\frac{d\\left(x\\right)}{dx}+\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}",
            "2\\cdot x+\\frac{d\\left(x\\right)}{dx}+\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}",
            "2\\cdot x+1+\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}",
            "2\\cdot x+1-\\sin \\left(x\\right)"
        ]
        result = "2\\cdot x+1-\\sin \\left(x\\right)"
        return SolvedExercise(name, steps, result)

    @staticmethod
    def derivative_mult_of_three_elem() -> SolvedExercise:
        name = "multiplication of 3 elem"
        steps = [
            "x^2\\sin (x)\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}+\\cos (x)\\frac{d\\left(x^2\\sin (x)\\right)}{dx}",
            "x^2\\sin (x)\\ \\left(-\\sin \\left(x\\right)\\right)+\\cos (x)\\frac{d\\left(x^2\\sin (x)\\right)}{dx}",
            "-\\ x^2\\sin ^2(x)\\ +\\cos (x)\\frac{d\\left(x^2\\sin (x)\\right)}{dx}",
            "x^2\\sin (x)\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}+\\cos (x)\\cdot \\left(\\frac{d\\left(x^2\\right)}{dx}\\cdot \\sin (x)+\\frac{d\\left(\\sin \\left(x\\right)\\right)}{dx}\\cdot x^2\\right)"
        ]
        result = "x^2\\sin (x)\\frac{d\\left(\\cos \\left(x\\right)\\right)}{dx}+\\cos (x)\\cdot \\left(\\frac{d\\left(x^2\\right)}{dx}\\cdot \\sin (x)+\\frac{d\\left(\\sin \\left(x\\right)\\right)}{dx}\\cdot x^2\\right)"
        return SolvedExercise(name, steps, result)
