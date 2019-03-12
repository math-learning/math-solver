class DifferentArgNumberComparator:

    def compare(self, structure, expression):
        if len(structure.args) < len(expression.args) and one_is_user_defined_function(structure.args):
            print("alskdjf")