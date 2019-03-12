from src.model.Equality import Equality


class Axiom(Equality):
    def __init__(self, left, right):
        Equality.__init__(self,left,right)
