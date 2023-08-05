from bitstring import BitArray
from .base import ResourceRecord
import base64


class DS(ResourceRecord):
    class _Binary(ResourceRecord._Binary):

        @property
        def full(self):
            result = bin(self.resource_record.flags)[2:].zfill(16)
            result += bin(self.resource_record.protocol)[2:].zfill(8)
            result += bin(self.resource_record.algorithm)[2:].zfill(8)
            result += BitArray(bytes=self.resource_record.public_key).bin
            return result

    id = 43
    repr = ['key_tag', 'protocol', 'algorithm', 'public_key']

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.key_tag = answer.message.stream.read(f'uint:16')
        instance.protocol = answer.message.stream.read(f'uint:8')
        instance.algorithm = answer.message.stream.read(f'uint:8')
        # str_ = answer.message.stream.read(f'bin:{read_len*8 - 32}')
        # instance.public_key = ''.join([chr(int(x, base=2)) for x in [str_[i:i + 8] for i in range(0, len(str_), 8)]])
        instance.public_key = answer.message.stream.read(f'bytes:{read_len*8 - 32}')
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.key_tag = data.get('key_tag')
        instance.algorithm = data.get('algorithm')
        instance.digest_type = data.get('digest_type')
        instance.digest = data.get('digest')
        return instance

    @property
    def __dict__(self):
        return {'flags': int(self.key_tag),
                'protocol': int(self.protocol),
                'algorithm': int(self.algorithm),
                'public_key': str(self.public_key)}
