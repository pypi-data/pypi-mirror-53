from Cryptodome.Hash import SHA1 as CD_SHA1
from Cryptodome.Hash import SHA256 as CD_SHA256
from .base import Digest


class SHA1(Digest):
    hasher = CD_SHA1
    id = 1


class SHA256(Digest):
    hasher = CD_SHA256
    id = 2


