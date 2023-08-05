from .base import Algorithm
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA1, SHA256, SHA512


class RSASHA1(Algorithm):
    id = 5


class RSASHA1_NSEC3_SHA1(Algorithm):
    id = 7


class RSASHA256(Algorithm):
    id = 8

    @classmethod
    async def verify(cls, signature, key, resource_record):
        instance = cls()
        instance.key = RSA.import_key(key)
        instance.key

class RSASHA512(Algorithm):
    id = 10