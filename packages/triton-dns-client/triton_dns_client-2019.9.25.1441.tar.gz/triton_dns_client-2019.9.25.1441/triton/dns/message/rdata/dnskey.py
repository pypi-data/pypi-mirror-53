from typing import Union

from bitstring import BitArray

from .base import ResourceRecord


class DNSKEY(ResourceRecord):
    class _Binary(ResourceRecord._Binary):

        @property
        def full(self):
            result = bin(self.resource_record.flags)[2:].zfill(16)
            result += bin(self.resource_record.protocol)[2:].zfill(8)
            result += bin(self.resource_record.algorithm)[2:].zfill(8)
            row = self.resource_record.public_key.decode() if isinstance(self.resource_record.public_key,
                                                                         bytes) else self.dnskey.public_key
            res = ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in row]])
            result += res
            return result

    id = 48
    repr = ['flags', 'protocol', 'algorithm', 'public_key']

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.flags = answer.message.stream.read(f'bin:16')
        instance.protocol = answer.message.stream.read(f'uint:8')
        instance.algorithm = answer.message.stream.read(f'uint:8')
        str_ = answer.message.stream.read(f'bin:{read_len - 4}')
        instance.public_key = ''.join([chr(int(x, base=2)) for x in [str[i:i + 8] for i in range(0, len(str_), 8)]])
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.flags = data.get('flags')
        instance.protocol = 3
        instance.algorithm = data.get('algorithm')
        instance.public_key = data.get('public_key')
        return instance

    @property
    def __dict__(self):
        return {'flags': int(self.flags),
                'protocol': int(self.protocol),
                'algorithm': int(self.algorithm),
                'public_key': str(self.public_key.decode()) if isinstance(self.public_key, bytes) else self.public_key}

    @property
    def key_tag(self):
        if self.algorithm == 1:
            pass
        else:
            ac = 0
            for i, k in enumerate(BitArray(bin=self.Binary.full).bytes):
                ac += k if i & 1 else k << 8
            ac += (ac >> 16) & 0xFFFF
            return ac & 0xFFFF
