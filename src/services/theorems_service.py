class TheoremsService:
    def get_theorems_that_can_be_applied_to(self, expression, theorems):
        theorems_that_can_be_applied = []
        for theorem in theorems:
            if theorem.apply_to(expression) != None:
                theorems_that_can_be_applied.append(theorem)
        return theorems_that_can_be_applied