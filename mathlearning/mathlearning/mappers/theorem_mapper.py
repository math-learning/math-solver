from mathlearning.model.theorem import Theorem
from typing import List

class TheoremMapper:

    @staticmethod
    def theorems(json_theorems) -> List[Theorem]:
        parsed_theorems = []
        for theo in json_theorems:
            theo_object = Theorem(theo.get("name"), theo.get("left"), theo.get("right"), theo.get("conditions"))
            parsed_theorems.append(theo_object)
        return parsed_theorems
