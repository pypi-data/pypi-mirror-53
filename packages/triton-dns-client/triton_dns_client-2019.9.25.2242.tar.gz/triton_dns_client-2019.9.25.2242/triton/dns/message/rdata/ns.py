from ipaddress import IPv4Address
from ..domains.domain import Domain
from .base import ResourceRecord


class NS(ResourceRecord):
    class _Binary(ResourceRecord._Binary):

        @property
        def full(self):
            return Domain.sub_encode(self.resource_record.nsdname.label)

    id = 2
    repr = ['nsdname']

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.nsdname = Domain.decode(answer.message)
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        try:
            instance.nsdname = Domain(data.get('label', data.get('nsdname')), None)
        except AttributeError:
            instance.nsdname = Domain(data[2], None)
        return instance

    @property
    def __dict__(self):
        return {'nsdname': self.nsdname}