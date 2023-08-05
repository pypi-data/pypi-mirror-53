from bitstring import BitArray

from triton.dns.dnssec.digest import Digest
from .base import ResourceRecord


class DS(ResourceRecord):
    class _Binary(ResourceRecord._Binary):

        @property
        def full(self):
            result = bin(self.resource_record.key_tag)[2:].zfill(16)
            result += bin(self.resource_record.algorithm)[2:].zfill(8)
            result += bin(self.resource_record.digest_type)[2:].zfill(8)
            result += BitArray(bytes=self.resource_record._digest).bin
            return result

    id = 43
    repr = ['key_tag', 'algorithm', 'algorithm', 'digest_type', 'digest']

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        """
        Parses wire-format bytes to DS instance
        :param answer: triton.dns.message.Answer
        :param read_len: Answer.rdata_length
        :return: DS instance
        """
        instance = cls(answer)
        instance.key_tag = answer.message.stream.read(f'uint:16')
        instance.algorithm = answer.message.stream.read(f'uint:8')
        instance.digest_type = answer.message.stream.read(f'uint:8')
        instance._digest = answer.message.stream.read(f'bytes:{read_len - 4}')
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        """
        Parses dict values to create this RR type
        :param answer: triton.dns.message.Answer
        :param data: dictionary with {'key_tag', 'algorithm', 'digest_type', 'digest'} values
        :return: DS instance
        """
        instance = cls(answer)
        instance.key_tag = data.get('key_tag')
        instance.algorithm = data.get('algorithm')
        instance.digest_type = data.get('digest_type')
        instance._digest = data.get('digest')
        return instance

    @property
    def digest(self):
        """
        digest field is represented as HEX according to RFC
        :return: hex value of _digest
        """
        return self._digest.hex()

    @property
    def __dict__(self):
        """
        Monkey-patch dict. Excludes all unnecessary attr
        :return: dict of fields according to RFC
        """
        return {'flags': int(self.key_tag),
                'protocol': int(self.algorithm),
                'algorithm': int(self.digest_type),
                'public_key': str(self.digest)}

    def verify_key(self, key):
        """
        Verifies that DNSKEY answer matches this DS record digest
        :param key: triton.dns.message.Answer
        :return: True if matches, False if not. Raises if key_tag dont match
        """
        return Digest.verify_from_ds(key, self.answer)

    def verify_from_message(self, message):
        """
        Verifies that corresponding DNSKEY exist in message and its correct
        :param message: triton.dns.Message
        :return: True is exist and matches and False in any other condition
        """
        for answer in message.answer:
            if answer.type == 48:
                if answer.rdata.key_tag == self.key_tag:
                    return Digest.verify_from_ds(answer, self.answer)
        return False
