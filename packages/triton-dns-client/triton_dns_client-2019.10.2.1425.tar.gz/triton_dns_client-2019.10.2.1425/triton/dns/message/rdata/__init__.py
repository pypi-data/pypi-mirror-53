from .a import A
from .aaaa import AAAA
from .base import ResourceRecord
from .caa import CAA
from .dnskey import DNSKEY
from .ds import DS
from .mx import MX
from .ns import NS
from .nsec import NSEC, NSEC3, NSEC3PARAM
from .opt import OPT
from .rrsig import RRSIG
from .soa import SOA
from .txt import TXT
from .cname import CNAME

rdata_cls = {rr.id: rr for rr in ResourceRecord.__subclasses__()}
