from src.model.Theorem import Theorem
from sympy.parsing.sympy_parser import parse_expr

class TheoremMapper:

    def from_json_to_theorems(self, json_theorems):
        parsed_theorems = []
        for theo in json_theorems:
            theo_object = Theorem(theo.get("name"), parse_expr(theo.get("left")), parse_expr(theo.get("right")))
            parsed_theorems.append(theo_object)
        return parsed_theorems