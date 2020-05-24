from mathlearning.model.integrate_by_parts import IntegrateByPartsTheorem

class IntegrateTheorems:
  @staticmethod
  def integrate_by_parts():
    return IntegrateByPartsTheorem()

  @staticmethod
  def get_all():
    return [
        IntegrateTheorems.integrate_by_parts()
    ]
