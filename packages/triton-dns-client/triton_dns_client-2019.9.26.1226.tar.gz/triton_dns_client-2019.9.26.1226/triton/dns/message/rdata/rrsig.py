from .base import ResourceRecord
from triton.dns.message.domains.domain import Domain
import base64
from bitstring import BitArray


class RRSIG(ResourceRecord):
    type_covered: int
    algorithm: int
    labels: int
    original_ttl: int
    signature_expiration: int
    signature_inception: int
    key_tag: int
    signers_name: str
    signature: bytes

    class _Binary(ResourceRecord._Binary):

        @property
        def full(self):
            result = format(self.resource_record.type_covered, 'b').zfill(16)
            result += format(self.resource_record.algorithm, 'b').zfill(8)
            result += format(self.resource_record.labels, 'b').zfill(8)
            result += format(self.resource_record.original_ttl, 'b').zfill(32)
            result += format(self.resource_record.signature_expiration, 'b').zfill(32)
            result += format(self.resource_record.signature_inception, 'b').zfill(32)
            result += format(self.resource_record.key_tag, 'b').zfill(16)
            for prt in self.resource_record.signers_name.split('.'):
                sig_name = ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in prt]])
                result += f'{bin(int(len(sig_name) / 8))[2:].zfill(8)}{sig_name}'
            else:
                result += str().zfill(8)
            result += BitArray(bytes=self.resource_record._signature).bin
            return result

        @property
        def without_signature(self):
            result = format(self.resource_record.type_covered, 'b').zfill(16)
            result += format(self.resource_record.algorithm, 'b').zfill(8)
            result += format(self.resource_record.labels, 'b').zfill(8)
            result += format(self.resource_record.original_ttl, 'b').zfill(32)
            result += format(self.resource_record.signature_expiration, 'b').zfill(32)
            result += format(self.resource_record.signature_inception, 'b').zfill(32)
            result += format(self.resource_record.key_tag, 'b').zfill(16)
            for prt in self.resource_record.signers_name.split('.'):
                sig_name = ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in prt]])
                result += f'{bin(int(len(sig_name) / 8))[2:].zfill(8)}{sig_name}'
            else:
                result += str().zfill(8)
            return result

    id = 46
    repr = ['type_covered',
            'algorithm',
            'labels',
            'original_ttl',
            'signature_expiration',
            'signature_inception',
            'key_tag',
            'signers_name',
            'signature']

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        start = answer.message.stream.pos
        instance.type_covered = answer.message.stream.read(f'uint:16')
        instance.algorithm = answer.message.stream.read(f'uint:8')
        instance.labels = answer.message.stream.read(f'uint:8')
        instance.original_ttl = answer.message.stream.read(f'uint:32')
        instance.signature_expiration = answer.message.stream.read(f'uint:32')
        instance.signature_inception = answer.message.stream.read(f'uint:32')
        instance.key_tag = answer.message.stream.read(f'uint:16')
        instance.signers_name = Domain.decode(answer.message)
        end = answer.message.stream.pos
        instance._signature = answer.message.stream.read(f'bytes:{int(read_len - (end - start)/8)}')
        return instance


    @property
    def signature(self):
        return base64.b64encode(self._signature).decode()

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.type_covered = data.get('type_covered')
        instance.algorithm = data.get('algorithm')
        instance.labels = data.get('labels')
        instance.original_ttl = data.get('original_ttl')
        instance.signature_expiration = data.get('signature_expiration')
        instance.signature_inception = data.get('signature_inception')
        instance.key_tag = data.get('key_tag')
        instance.signers_name = data.get('signers_name')
        instance._signature = data.get('signature')
        return instance

    @property
    def __dict__(self):
        return {'type_covered': int(self.type_covered),
                'algorithm': int(self.algorithm),
                'labels': int(self.labels),
                'original_ttl': int(self.original_ttl),
                'signature_expiration': int(self.signature_expiration),
                'signature_inception': int(self.signature_inception),
                'key_tag': int(self.key_tag),
                'signers_name': str(self.signers_name),
                'signature': str(self.signature)}

    async def verify(self, message_with_keys):
        for answer in message_with_keys.answer:
            if answer.rdata.key_tag == self.key_tag:
                pass