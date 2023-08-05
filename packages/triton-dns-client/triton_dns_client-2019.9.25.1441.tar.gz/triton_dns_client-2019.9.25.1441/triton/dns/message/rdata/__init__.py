from .a import A
from .opt import OPT
from .aaaa import AAAA
from .mx import MX
from .ns import NS
from .soa import SOA
from .txt import TXT
from .dnskey import DNSKEY
from .rrsig import RRSIG
from .ds import DS
from .caa import CAA
from .base import ResourceRecord

rdata_cls = {rr.id: rr for rr in ResourceRecord.__subclasses__()}
