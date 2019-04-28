from sqlalchemy.sql import expression
from sympy.core.relational import Equality

from server.src.utils.list_utils import ListUtils

class Equality:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class MatchAnalysisReport:
    def __init__(self, template, expression, match, equalities):
        self.template = template
        self.expression = expression
        self.expression_match_template = match
        self.equalities = equalities

class TemplateMatchAnalyzer:

    def analyze(self, template, expression):
        analysis = MatchAnalysisReport(template, expression, None, [])
        return self.analyze_rec(template, expression, analysis)

    def analyze_rec(self, template, expression, analysis):
        if not analysis.expression_match_template:
            return analysis

        if not template.contains_user_defined_funct() and not expression.contains_user_defined_funct():
            match = template.compare(expression)
        elif template.is_user_defined_func():
            match = template.free_symbols_match(expression)
        elif template.children_amount() == expression.children_amount():
            match = self.analyze_exp_with_user_def_func_eq_sizes(template, expression, analysis)
        else:
            # TODO
            self.analyze_exp_with_user_def_func_diff_sizes(template, expression, analysis)
        
        return self.build_match_analysis_report(match, analysis, template, expression)

    def build_match_analysis_report(self, match, analysis, template, expression):
        if match:
            current_equalities = analysis.equalities
            new_equality = Equality(template, expression)
            equalities = current_equalities[:]
            equalities.append(new_equality)

        return MatchAnalysisReport(analysis.template, analysis.expression, match, equalities)

    def analyze_exp_with_user_def_func_eq_sizes(self, template, expression, analysis):
        if template.compare_func(expression):
            if template.is_commutative:
                return self.analyze_commutative_children_eq_len(template, expression, analysis)
            else:
                return self.analyze_children_non_commutative_eq_len(template, expression, analysis)
    
    # if the function is commutative we should compare all children combinations 
    # of the expression and the template
    # for example: comparing f(x) + x with x**2 + x
    # + is commutative so we should analyze:
    # 1. ¿f(x) == x ** 2  && x == x ?
    # 2. ¿f(x) == x && x ** 2 == x ?
    def analyze_commutative_children_eq_len(self, template, expression, analysis):
        comparison_cases = ListUtils.combinations(template,expression)
        case_analysis = analysis
        for case in comparison_cases:
            case_analysis = self.analyze_case(case, analysis)
            if analysis.expression_match_template:
                return case_analysis
        return case_analysis

    # A comparison case is a collection of pairs to compare for ex:
    # [ [x, x] , [f(x), x + 3]  ] 
    # the analysis then consist in comparing x with x and f(x) with x + 3
    def analyze_case(self, comparison_case, analysis):
        result = analysis
        for pair in comparison_case:
            result = self.analyze_rec(pair[0], pair[1], result)
        return result

    
    # If the function is non commutative we must respect the order
    # Ex: comparing x - x**2 with g(y) - f(x)
    # we only compare x with g(y) and x **2 with f(x)
    def analyze_children_non_commutative_eq_len(self, template, expression, analysis):
        result = analysis
        template_children = template.get_children()
        expression_children = expression.get_children()
        for i in range(0, len(template)):
            result = self.analyze_rec(template_children[i], expression_children[i], result)
        return result

    # TODO
    def analyze_exp_with_user_def_func_diff_sizes(self, template, expression, analysis):
        raise Exception("not implemented yet")
    
