import unittest

from src.model.expression import Expression
from src.model.template_match_analyzer import (MatchAnalysisReport,
                                               TemplateMatchAnalyzer,
                                               Equality)


class TestTemplateMatchAnalyzer(unittest.TestCase):

    def test_analyze(self):
        analyzer = TemplateMatchAnalyzer()
        template = Expression("f(x) + g(x)")
        expression = Expression("x + x^2")
        
        equalities = [Equality(Expression("f(x)"), Expression("x")),
                    Equality(Expression("g(x)"), Expression("x^2"))]
        expected = MatchAnalysisReport(template, expression, True, equalities)
        
        result = analyzer.analyze(template,[], expression)

        self.assertEquals(expected, result)
    

    def test_analyze_exp_with_user_def_func_diff_sizes(self):
        analyzer = TemplateMatchAnalyzer()
        template = Expression("f(x) + g(y)")
        expression = Expression("x + x^2 + y")
        analysis = MatchAnalysisReport(template, expression, True, [])
        result = analyzer.analyze_exp_with_user_def_func_diff_sizes(template, [], expression, analysis)

        self.assertTrue(result.expression_match_template)
    
    def test_analyze_derivatives(self):
        analyzer = TemplateMatchAnalyzer()
        template = Expression("\\frac{d(f(x) + g(x))}{dx}")
        expression = Expression("\\frac{d(x + x^2)}{dx}")
        
        result = analyzer.analyze(template, [], expression)

        equalities = [Equality(Expression("f(x)"), Expression("x")),
                    Equality(Expression("g(x)"), Expression("x^2"))]
        expected = MatchAnalysisReport(template, expression, True, equalities)

        self.assertEquals(expected, result)

    def test_analyze_derivatives_sum_of_three(self):
        analyzer = TemplateMatchAnalyzer()
        template = Expression("\\frac{d(f(x) + g(x))}{dx}")
        expression = Expression("\\frac{d(x + x^2 + \\cos (x))}{dx}")
        
        result = analyzer.analyze(template, [], expression)

        equalities = [Equality(Expression("f(x)"), Expression("x+ x^2 ")),
                    Equality(Expression("g(x)"), Expression(" \\cos(x)"))]
        expected = MatchAnalysisReport(template, expression, True, equalities)

        self.assertEquals(expected, result)