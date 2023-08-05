import base64
from bitstring import BitArray

from .base import ResourceRecord


class DNSKEY(ResourceRecord):
    class _Binary(ResourceRecord._Binary):

        @property
        def full(self):
            result = bin(self.resource_record.flags)[2:].zfill(16)
            result += bin(self.resource_record.protocol)[2:].zfill(8)
            result += bin(self.resource_record.algorithm)[2:].zfill(8)
            result += BitArray(bytes=self.resource_record._public_key).bin
            return result

    id = 48
    repr = ['flags', 'protocol', 'algorithm', 'public_key']

    @classmethod
    async def parse_bytes(cls, answer: 'Answer', read_len: int) -> 'DNSKEY':
        instance = cls(answer)
        instance.flags = answer.message.stream.read(f'uint:16')
        instance.protocol = answer.message.stream.read(f'uint:8')
        instance.algorithm = answer.message.stream.read(f'uint:8')
        instance._public_key = answer.message.stream.read(f'bytes:{read_len - 4}')
        return instance

    @classmethod
    async def parse_dict(cls, answer: 'Answer', data: dict) -> 'DNSKEY':
        instance = cls(answer)
        instance.flags = data.get('flags')
        instance.protocol = 3
        instance.algorithm = data.get('algorithm')
        instance._public_key = data.get('public_key')
        return instance

    @property
    def public_key(self):
        return base64.b64encode(self._public_key).decode()

    @property
    def key_tag(self):
        if self.algorithm == 1:
            return 0
        else:
            ac = 0
            for i, k in enumerate(BitArray(bin=self.Binary.full).bytes):
                ac += k if i & 1 else k << 8
            ac += (ac >> 16) & 0xFFFF
            return ac & 0xFFFF
