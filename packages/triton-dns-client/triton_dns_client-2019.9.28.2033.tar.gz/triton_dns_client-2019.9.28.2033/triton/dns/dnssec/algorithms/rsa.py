import datetime

from Cryptodome.Hash import SHA1, SHA256, SHA512, SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from bitstring import BitArray

from .base import Algorithm


class RSAPublicKey:
    def __init__(self, rr):
        len_pe = rr.rdata._public_key[0]
        self.public_exponent = int.from_bytes(rr.rdata._public_key[1:1 + len_pe], byteorder='big')
        self.modulus = int.from_bytes(rr.rdata._public_key[1 + len_pe:], byteorder='big')


class ValidationError(Exception):
    pass


class RSAAlgorithm(Algorithm):
    signer: RSA
    hasher: SHA

    @classmethod
    def verify_rrset(cls, key_rr, rrset, rrsig):
        assert key_rr.rdata.algorithm == cls.id
        assert rrsig.rdata._algorithm == cls.id
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        if rrsig.rdata.signature_expiration < now:
            raise ValidationError('Signature expired')
        elif rrsig.rdata.signature_inception > now:
            raise ValidationError('Signature inception time is in future')
        rsa_key = RSAPublicKey(key_rr)
        _key = cls.signer.construct((rsa_key.modulus, rsa_key.public_exponent))
        signer = PKCS1_v1_5.new(_key)
        hash = cls.hasher.new()
        hash.update(BitArray(bin=rrsig.rdata.Binary.without_signature).bytes)
        hash.update(b''.join([x.Binary.full_canonical_bytes for x in rrset]))
        return signer.verify(hash, rrsig.rdata._signature)


class RSASHA1(RSAAlgorithm):
    id = 5
    signer = RSA


class RSASHA1_NSEC3_SHA1(RSAAlgorithm):
    id = 7
    signer = RSA
    hasher = SHA1


class RSASHA256(RSAAlgorithm):
    id = 8
    signer = RSA
    hasher = SHA256


class RSASHA512(RSAAlgorithm):
    id = 10
    signer = RSA
    hasher = SHA512
