from mathlearning.model.integrate_by_parts import IntegrateByPartsTheorem, IntegrateByPartsApplyTheorem, \
  IntegrateByPartsReplaceUVTheorem
from mathlearning.model.integrate_by_substitution import IntegrateBySubstitutionDefineUAndDUTheorem, \
  IntegrateBySubstitutionReplaceUAndDUTheorem
from mathlearning.model.theorem import Theorem


class IntegrateTheorems:

  @staticmethod
  def integrate_of_a_sum():
    return Theorem(
      "Integral de la suma",
      "\\int (f(x) + g(x)) dx",
      "(\\int (f(x)) dx) + (\\int (g(x)) dx)",
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

  # by parts rule

  @staticmethod
  def integrate_by_parts():
    return IntegrateByPartsTheorem()

  @staticmethod
  def integrate_by_parts_apply():
    return IntegrateByPartsApplyTheorem()

  @staticmethod
  def integrate_by_parts_replace_uv():
    return IntegrateByPartsReplaceUVTheorem()

  # substitution rule
  @staticmethod
  def integrate_by_substitution_define_u_du():
    return IntegrateBySubstitutionDefineUAndDUTheorem()

  @staticmethod
  def integrate_by_substitution_replace_u_du():
    return IntegrateBySubstitutionReplaceUAndDUTheorem()

  @staticmethod
  def get_all():
    return [
        IntegrateTheorems.integrate_by_parts(),
        IntegrateTheorems.integrate_multiply_for_constant(),
        IntegrateTheorems.integrate_of_a_sum(),
        IntegrateTheorems.integrate_by_parts_replace_uv(),
        IntegrateTheorems.integrate_by_parts_apply(),
        IntegrateTheorems.integrate_by_substitution_define_u_du(),
        IntegrateTheorems.integrate_by_substitution_replace_u_du(),

    ]
