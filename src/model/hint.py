class TextHint:
    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'name': self.name}
