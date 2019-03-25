class ComparisonPair:
    def __init__(self, structure_child, expression_child):
        self.structure_child = structure_child
        self.expression_child = expression_child


class ComparatorUtils:
    def get_equivalent_children_pairs(self, length, structure_children, expression_children):
        comparison_pairs = []
        for i in range(0, length):
            comparison_pairs .append(ComparisonPair(structure_children[i], expression_children[i]))
        return comparison_pairs

    def both_nodes_are_leaves(self, structure, expression):
        return len(structure.args) == len(expression.args) and len(structure.args) == 0


    def get_children_pairs(self, structure_children, expression_children):
        return self.get_children_pairs_rec(structure_children, expression_children, [], [])


    def get_children_pairs_rec(self, structure_children, expression_children, accum, possibles):
        if len(structure_children) == 1 and len(expression_children) == 1:
            accum.append(ComparisonPair(structure_children[0], expression_children[0]))
            possibles.append(accum)
            return possibles

        # TODO: RENAME
        for expression_child in expression_children:
            new_accum = accum[:]
            new_accum.append(ComparisonPair(structure_children[0], expression_child))
            structure_children_without_first = structure_children[1:]
            expression_children_without_child = list(expression_children[:])
            expression_children_without_child.remove(expression_child)
            expression_children_without_child = tuple(expression_children_without_child)
            possibles = self.get_children_pairs_rec(structure_children_without_first, expression_children_without_child, new_accum, possibles)

        return possibles

