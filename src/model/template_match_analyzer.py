from src.utils.list.index_combinations_strategy import \
    CommutativeGroupTransformer
from src.utils.list.index_combinations_strategy_only_continuous import \
    NonCommutativeGroupTransformer
from src.utils.list.list_size_transformer import ListSizeTransformer
from src.utils.list.list_utils import ListUtils


class Equality:
    def __init__(self, template, expression):
        self.template = template
        self.expression = expression
    
    def to_string(self):
        return "Equality template: " + self.template.to_string() + " . expression: " + self.expression.to_string()

    def __eq__(self, other):
        if isinstance(other, Equality):
            return self.template == other.template and self.expression == other.expression
        return False
    
class MatchAnalysisReport:
    def __init__(self, template, expression, match, equalities):
        self.template = template
        self.expression = expression
        self.expression_match_template = match
        self.equalities = equalities
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, MatchAnalysisReport):
            if len(self.equalities) != len(other.equalities):
                return False
            for i in range(0,len(self.equalities)):
                if not self.equalities[i] in other.equalities:
                    return False
            return self.template == other.template and self.expression == other.expression and self.expression_match_template == other.expression_match_template and self.equalities == other.equalities

        return False

class TemplateMatchAnalyzer:

    def __init__(self):
        self.commutative_list_size_transformer = ListSizeTransformer(CommutativeGroupTransformer())
        self.non_commutative_list_size_transformer = ListSizeTransformer(NonCommutativeGroupTransformer())
        self.list_utils = ListUtils()

    def analyze(self, template, expression):
        analysis = MatchAnalysisReport(template, expression, True, [])
        return self.analyze_rec(template, expression, analysis)

    def analyze_rec(self, template, expression, analysis):
        print ("Analizing")
        print("Template: " +template.to_string())
        print("Expression: " +expression.to_string())
        if not analysis.expression_match_template:
            return analysis

        # Handle two simpy expressions
        if not template.contains_user_defined_funct() and not expression.contains_user_defined_funct():
            match = template.is_equivalent_to(expression)
            analysis = self.build_match_analysis_report(match, analysis, template, expression)

        elif template.is_user_defined_func():
            match = template.free_symbols_match(expression)
            analysis = self.build_match_analysis_report(match, analysis, template, expression)

        # Handle non leaves with at least one user defined function
        elif template.children_amount() == expression.children_amount():
            analysis = self.analyze_exp_with_user_def_func_eq_sizes(template, expression, analysis)
        
        # Handle different size children. for example f(x)  = x + x**2
        else:    
            analysis = self.analyze_exp_with_user_def_func_diff_sizes(template, expression, analysis)
        
        return analysis

    def build_match_analysis_report(self, match, analysis, template, expression):
        if match:
            current_equalities = analysis.equalities
            new_equality = Equality(template, expression)
            equalities = current_equalities[:]
            equalities.append(new_equality)
            print("Adding: " + new_equality.to_string())

        return MatchAnalysisReport(analysis.template, analysis.expression, match, equalities)

    def analyze_exp_with_user_def_func_eq_sizes(self, template, expression, analysis):
        if template.compare_func(expression):
            if template.is_commutative():
                return self.analyze_commutative_children_eq_len(template.get_children(), expression.get_children(), analysis)
            else:
                return self.analyze_children_non_commutative_eq_len(template, expression, analysis)
    
    # if the function is commutative we should compare all children combinations 
    # of the expression and the template
    # for example: comparing f(x) + x with x**2 + x
    # + is commutative so we should analyze:
    # 1. ¿f(x) == x ** 2  && x == x ?
    # 2. ¿f(x) == x && x ** 2 == x ?
    def analyze_commutative_children_eq_len(self, template_children, expression_children, analysis):
        comparison_cases = self.list_utils.pair_combinations(template_children, expression_children)
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

    # TODO refactor
    def analyze_exp_with_user_def_func_diff_sizes(self, template, expression, analysis):
        if len(template.get_children()) >= len(expression.get_children()):
            return self.build_match_analysis_report(False, analysis, template, expression)

        possible_expression_children = expression.get_children_with_size(len(template.get_children()))
        
        for children in possible_expression_children:
            if template.is_commutative():
                new_analysis = self.analyze_commutative_children_eq_len(template.get_children(), children, analysis)
            else:
                new_analysis = self.analyze_children_non_commutative_eq_len(template.get_children(), children, analysis)
            if new_analysis.expression_match_template:
                return new_analysis
        
        return self.build_match_analysis_report(False, analysis, template, expression)