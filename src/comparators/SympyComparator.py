from src.comparators.ComparatorUtils import ComparatorUtils
from src.comparators.ComparisonResult import ComparisonResult


class SympyComparator:

    def __init__(self):
        self.comparator_utils = ComparatorUtils()

    def compare(self, structure, expression, equalities):
        if structure.func == expression.func:
            if len(structure.args) == len(expression.args):
                if structure.is_commutative:
                    print("is cummulative")
                    pairs_to_compare = self.comparator_utils.get_children_pairs(structure.args, expression.args)
                    for children_pairs in pairs_to_compare:
                        comparison = self.comparator_utils.compare_children_combinations(children_pairs, equalities)
                        if comparison.structures_match:
                            return comparison
                else:
                    print("comparing non commutative")
                    pairs_to_compare = self.comparator_utils.get_equivalent_children_pairs(len(structure), structure.args, expression.args)
                    return self.comparator_utils.compare_children_combinations(pairs_to_compare, equalities)
        return ComparisonResult(False, [])