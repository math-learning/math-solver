import json

from mathlearning.mappers.theorem_mapper import TheoremMapper
from mathlearning.model.expression import Expression
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
        expression = Expression(node_dictionary['expression'], is_latex=False)
        theorem_applied = TheoremMapper.theorem(node_dictionary['theorem_applied'])
        return SolutionTreeNode(expression, theorem_applied, branches)
