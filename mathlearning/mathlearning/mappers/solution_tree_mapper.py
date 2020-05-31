import json
from mathlearning.mappers.theorem_mapper import TheoremMapper
from mathlearning.model.expression import Expression
from mathlearning.model.expression_variable import ExpressionVariable
from mathlearning.services.result_service import SolutionTreeNode

class SolutionTreeMapper:

    @staticmethod
    def parse(tree_string: str) -> SolutionTreeNode:
        tree_dictionary = json.loads(tree_string)
        return SolutionTreeMapper.parse_node(tree_dictionary)

    @staticmethod
    def parse_node(node_dictionary: dict) -> SolutionTreeNode:
        branches = []
        for branch in node_dictionary['branches']:
            branches.append(SolutionTreeMapper.parse_node(branch))

        json_expression = json.loads(node_dictionary['expression'])
        expression = SolutionTreeMapper.parse_expression(json_expression)
        theorem_applied = node_dictionary['theorem_applied_name']
        return SolutionTreeNode(expression, theorem_applied, branches)

    @staticmethod
    def parse_expression(json_expression):
        main_expression = json_expression['expression']
        json_variables = json_expression['variables']
        variables = list(map(lambda variable: ExpressionVariable(variable['tag'], SolutionTreeMapper.parse_expression(variable['expression'])), json_variables))

        return Expression(main_expression, variables, is_latex=False)
