from src.model.theorem import Theorem


class TheoremMapper:

    @staticmethod
    def from_json_to_theorems(json_theorems):
        parsed_theorems = []
        for theo in json_theorems:
            theo_object = Theorem(theo.get("name"), theo.get("left"), theo.get("right"), theo.get("conditions"))
            parsed_theorems.append(theo_object)
        return parsed_theorems
