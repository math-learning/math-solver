from mathlearning.model.derivative_theorems import DerivativeTheorems
from mathlearning.model.integrate_theorems import IntegrateTheorems


class Theorems:
    @staticmethod
    def get_all():
        return DerivativeTheorems.get_all() + IntegrateTheorems.get_all()