from mathlearning.model.expression import Expression
from mathlearning.model.theorem import Theorem
from typing import List


class Exercise:
    def __init__(self, input_data: Expression, theorems: List[Theorem], result: Expression):
        self.theorems = theorems
        self.input_data = input_data
        self.result = result
