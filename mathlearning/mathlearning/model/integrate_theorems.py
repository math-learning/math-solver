from mathlearning.model.integrate_by_parts import IntegrateByPartsTheorem
from mathlearning.model.theorem import Theorem


class IntegrateTheorems:

  @staticmethod
  def integrate_of_a_sum():
    return Theorem(
      "Integral de la suma",
      "\\int (f(x) + g(x)) dx",
      "\\int (f(x)) dx + \\int (g(x)) dx",
      {}
    )

  @staticmethod
  def integrate_multiply_for_constant():
    return Theorem(
      "Integral por una constante",
      "\\int ( a * f(x)) dx",
      "a * \\int (f(x)) dx",
      {
        "a": [
          "IS_REAL",
          "IS_CONSTANT"
        ]
      }
    )

  @staticmethod
  def integrate_by_parts():
    return IntegrateByPartsTheorem()

  @staticmethod
  def get_all():
    return [
        IntegrateTheorems.integrate_by_parts(),
        IntegrateTheorems.integrate_multiply_for_constant(),
        IntegrateTheorems.integrate_of_a_sum()
    ]
