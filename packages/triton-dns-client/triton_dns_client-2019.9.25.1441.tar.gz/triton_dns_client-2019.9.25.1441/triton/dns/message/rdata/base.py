
class ResourceRecord:
    repr = []
    class _Binary:
        def __init__(self, resource_record):
            self.resource_record = resource_record

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    def __repr__(self):
        return str({x: getattr(self, x) for x in self.repr})