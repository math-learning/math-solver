from mathlearning.utils.list.commutative_group_transformer import CommutativeGroupTransformer
from mathlearning.utils.list.non_commutative_group_transformer import NonCommutativeGroupTransformer
from mathlearning.utils.list.list_size_transformer import ListSizeTransformer
from mathlearning.utils.list.list_utils import ListUtils
from typing import List
from mathlearning.model.expression import Expression

from mathlearning.utils.logger import Logger

logger = Logger.getLogger()


def to_string(template, expression):
    return "Template: " + template.to_string() + " - Expression: " + expression.to_string()


class Equality:
    def __init__(self,
                 template: Expression,
                 expression: Expression):
        self.template = template
        self.expression = expression

    def to_string(self) -> str:
        return "Equality " + to_string(self.template, self.expression)

    def __eq__(self, other):
        if isinstance(other, Equality):
            return self.template == other.template and self.expression == other.expression
        return False


class MatchAnalysisReport:
    def __init__(self,
                 template: Expression,
                 expression: Expression,
                 match: bool,
                 equalities: List[Equality]):
        self.template = template
        self.expression = expression
        self.expression_match_template = match
        self.equalities = equalities

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, MatchAnalysisReport):
            if len(self.equalities) != len(other.equalities):
                return False
            for i in range(0, len(self.equalities)):
                if not self.equalities[i] in other.equalities:
                    return False
            return self.template == other.template and self.expression == other.expression and self.expression_match_template == other.expression_match_template and self.equalities == other.equalities

        return False


class TemplateMatchAnalyzer:

    def __init__(self):
        self.commutative_list_size_transformer = ListSizeTransformer(CommutativeGroupTransformer())
        self.non_commutative_list_size_transformer = ListSizeTransformer(NonCommutativeGroupTransformer())
        self.list_utils = ListUtils()

    def analyze(self,
                template: Expression,
                template_conditions: List,
                expression: Expression
                ) -> MatchAnalysisReport:
        analysis = MatchAnalysisReport(template, expression, True, [])
        return self.analyze_rec(template, template_conditions, expression, analysis)

    def analyze_rec(self,
                    template: Expression,
                    template_conditions: List,
                    expression: Expression,
                    analysis: MatchAnalysisReport
                    ) -> MatchAnalysisReport:

        logger.info("Analizing " + to_string(template, expression))

        if not analysis.expression_match_template:
            return analysis

        # Handle two simpy expressions
        if not template.contains_user_defined_funct() and not expression.contains_user_defined_funct():
            # TODO: REFACTOR
            logger.info("Comparing two sympy expressions")

            conditions = template_conditions.get(template.to_string())
            if conditions != None and "IS_CONSTANT" in conditions:
                match = expression.is_constant()
            else:
                match = template.is_equivalent_to(expression)

            analysis = self.build_match_analysis_report(match, analysis, template, template_conditions, expression)

        elif template.is_user_defined_func():
            logger.info("Template is user defined function")
            match = template.free_symbols_match(expression)
            analysis = self.build_match_analysis_report(match, analysis, template, template_conditions, expression)

        elif not template.compare_func(expression):
            logger.info("Functions dont match")
            analysis = self.build_match_analysis_report(False, analysis, template, template_conditions, expression)

        # Handle non leaves with at least one user defined function
        elif template.children_amount() == expression.children_amount():
            logger.info("Analyzing children with equal sizes")
            analysis = self.analyze_exp_with_user_def_func_eq_sizes(template, template_conditions, expression, analysis)

        # Handle different size children. for example f(x)  = x + x^2
        else:
            logger.info("Analyzing children with different sizes")
            analysis = self.analyze_exp_with_user_def_func_diff_sizes(template, template_conditions, expression,
                                                                      analysis)

        return analysis

    def meets_the_conditions(self,
                             equalities: List[Equality],
                             template_conditions: List
                             ) -> bool:
        # TODO
        return True

    def build_match_analysis_report(self,
                                    match: bool,
                                    analysis: MatchAnalysisReport,
                                    template: Expression,
                                    template_conditions,
                                    expression: Expression
                                    ) -> MatchAnalysisReport:
        # TODO: conditions
        equalities = analysis.equalities
        if match:
            current_equalities = analysis.equalities
            new_equality = Equality(template, expression)
            equalities = current_equalities[:]
            equalities.append(new_equality)
            logger.info("Adding: " + new_equality.to_string())

        return MatchAnalysisReport(analysis.template, analysis.expression, match, equalities)

    def analyze_exp_with_user_def_func_eq_sizes(self,
                                                template: Expression,
                                                template_conditions: List,
                                                expression: Expression,
                                                analysis: MatchAnalysisReport
                                                ) -> MatchAnalysisReport:
        if template.compare_func(expression):
            if template.is_commutative():
                return self.analyze_commutative_children_eq_len(template.get_children(), template_conditions,
                                                                expression.get_children(), analysis)
            else:
                return self.analyze_children_non_commutative_eq_len(template, template_conditions, expression, analysis)

    # if the function is commutative we should compare all children combinations 
    # of the expression and the template
    # for example: comparing f(x) + x with x^2 + x
    # + is commutative so we should analyze:
    # 1. f(x) == x ^ 2  && x == x ?
    # 2. f(x) == x && x ^ 2 == x ?
    def analyze_commutative_children_eq_len(self,
                                            template_children,
                                            template_conditions,
                                            expression_children,
                                            analysis: MatchAnalysisReport
                                            ) -> MatchAnalysisReport:
        comparison_cases = self.list_utils.pair_combinations(template_children, expression_children)
        case_analysis = analysis
        for case in comparison_cases:
            case_analysis = self.analyze_case(case, template_conditions, analysis)
            if case_analysis.expression_match_template:
                return case_analysis
        return case_analysis

    # A comparison case is a collection of pairs to compare for ex:
    # [ [x, x] , [f(x), x + 3]  ] 
    # the analysis then consist in comparing x with x and f(x) with x + 3
    def analyze_case(self, comparison_case, template_conditions, analysis):
        result = analysis
        for pair in comparison_case:
            result = self.analyze_rec(pair[0], template_conditions, pair[1], result)
        return result

    # If the function is non commutative we must respect the order
    # Ex: comparing x - x^2 with g(y) - f(x)
    # we only compare x with g(y) and x ^2 with f(x)
    def analyze_children_non_commutative_eq_len(self,
                                                template: Expression,
                                                template_conditions: List,
                                                expression: Expression,
                                                analysis: MatchAnalysisReport
                                                ) -> MatchAnalysisReport:
        result = analysis
        template_children = template.get_children()
        expression_children = expression.get_children()
        for i in range(0, len(template)):
            result = self.analyze_rec(template_children[i], template_conditions, expression_children[i], result)
        return result

    # TODO refactor
    def analyze_exp_with_user_def_func_diff_sizes(self,
                                                  template: Expression,
                                                  template_conditions: List,
                                                  expression: Expression,
                                                  analysis: MatchAnalysisReport
                                                  ) -> MatchAnalysisReport:

        if template.children_amount() >= expression.children_amount():
            return self.build_match_analysis_report(False, analysis, template, template_conditions, expression)

        possible_expression_children = expression.get_children_with_size(template.children_amount())

        for children in possible_expression_children:
            if template.is_commutative():
                new_analysis = self.analyze_commutative_children_eq_len(template.get_children(), template_conditions,
                                                                        children, analysis)
            else:
                new_analysis = self.analyze_children_non_commutative_eq_len(template.get_children(),
                                                                            template_conditions, children, analysis)
            if new_analysis.expression_match_template:
                return new_analysis

        return self.build_match_analysis_report(False, analysis, template, template_conditions, expression)
