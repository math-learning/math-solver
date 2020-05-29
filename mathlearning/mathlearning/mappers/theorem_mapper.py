from mathlearning.model.integrate_by_parts import IntegrateByPartsTheorem
from mathlearning.model.theorem import Theorem
from typing import List


class TheoremMapper:

    @staticmethod
    def theorems(theorems: List) -> List[Theorem]:
        parsed_theorems = []
        for theo in theorems:
            theo_object = TheoremMapper.theorem(theo)
            parsed_theorems.append(theo_object)
        return parsed_theorems

    @staticmethod
    def theorem(theo: dict) -> List[Theorem]:
        if theo.get("name") == 'IntegrateByPartsTheorem':
            return IntegrateByPartsTheorem()

        return Theorem(theo.get("name"), theo.get("left"), theo.get("right"), theo.get("conditions"))

