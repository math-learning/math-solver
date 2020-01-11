from mathlearning.model.theorem import Theorem
from typing import List
from mathlearning.model.expression import Expression


class TheoremsService:
    def get_theorems_that_can_be_applied_to(self,
                                            expression: Expression,
                                            theorems: List[Theorem]
                                            ) -> List[Theorem]:
        theorems_that_can_be_applied = []
        for theorem in theorems:
            if len(theorem.apply_to(expression)) != 0:
                theorems_that_can_be_applied.append(theorem)
        return theorems_that_can_be_applied
