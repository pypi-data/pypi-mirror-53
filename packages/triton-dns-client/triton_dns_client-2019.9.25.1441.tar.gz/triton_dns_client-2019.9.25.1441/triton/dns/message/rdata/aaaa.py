from ipaddress import IPv6Address
from .base import ResourceRecord


class AAAA(ResourceRecord):
    class _Binary(ResourceRecord._Binary):

        @property
        def full(self):
            return bin(int(self.resource_record.address))[2:].zfill(8 * 4 * 4)

    id = 28
    repr = ['address']

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.address = IPv6Address(answer.message.stream.read(f'uint:{read_len * 8}'))
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        try:
            instance.address = IPv6Address(data.get('address'))
        except AttributeError:
            instance.address = IPv6Address(data[0])
        return instance

    @property
    def __dict__(self):
        return {'address': int(self.address)}
