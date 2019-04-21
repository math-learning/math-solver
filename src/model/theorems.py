class Theorem:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    def to_json(self):
        return {'name': self.name, 'right': str(self.right), 'left': str(self.left)}


class Theorems:
    
    def that_can_be_applied(self, expression, theorems):
        