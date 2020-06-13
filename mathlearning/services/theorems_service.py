from mathlearning.model.theorem import Theorem
from typing import List
from mathlearning.model.expression import Expression


class TheoremsService:
    def possible_theorems_for(self,
                            expression: Expression,
                            theorems: List[Theorem]
                            ) -> List[Theorem]:
        possible_theorems = []
        for theorem in theorems:
            if theorem.there_is_a_chance_to_apply_to(expression):
                possible_theorems.append(theorem)
        return possible_theorems
