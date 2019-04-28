from server.src.model.template_match_analyzer import TemplateMatchAnalyzer
from src.model.expression import Expression


class Theorem:
    def __init__(self, name, left, right):
        self.name = name
        self.left = Expression(left)
        self.right = Expression(right)
        self.analyzer = TemplateMatchAnalyzer()

    def to_json(self):
        return {'name': self.name, 'right': str(self.right), 'left': str(self.left)}

    def apply_to(self, expression):
        template = self.left
        analysis = self.analyzer.analyze(template, expression)
        
        return None
