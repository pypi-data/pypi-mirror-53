from triton.dns.message.domains.domain import Domain
from bitstring import BitArray


class ResourceRecord:
    repr = []

    class _Binary:
        def __init__(self, resource_record):
            self.resource_record = resource_record

        @property
        def full_bytes(self):
            return BitArray(bin=self.full).bytes


    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    def __repr__(self):
        return str({x: str(getattr(self, x)) if not isinstance(getattr(self, x), Domain) else getattr(self, x).label for x in self.repr })

    @classmethod
    def find_subclass_by_id(cls, id):
        for subclass in ResourceRecord.__subclasses__():
            if subclass.id == id:
                return subclass
        raise ValueError(f'No subclass with id {id}')