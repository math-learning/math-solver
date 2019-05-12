

from src.utils.list_utils import ListUtils


class ExpressionManipulator:
    
    def get_expression_children_grouped(self, expression, expected_size):
        if expected_size > len(expression.get_children()):
            return None
        
        combinations = []
        
        if expression.is_commutative():
            combinations = ListUtils.combinations_indices_diferent_sizes(len(expression), expected_size)
        else:
            combinations = 
