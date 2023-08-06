import asyncio
import typing
from . import dns
from . import protocol
from ipaddress import IPv6Address, IPv4Address, AddressValueError


def try_ip_convert(str_ip):
    try:
        IPv6Address(str_ip)
    except AddressValueError:
        try:
            IPv4Address(str_ip)
        except AddressValueError:
            return False
    return True


async def resolve_multiple(dns_server, domain: typing.Text, record_type=1, dnssec=False, timeout=5):
    assert isinstance(domain, list)
    result = []
    for name in domain:
        q = await query(dns_server, name, record_type, dnssec, timeout)
        if q:
            result.append(q)
    return result


async def query(dns_server, domain: typing.Text, record_type=1, dnssec=False, timeout=0.8) -> dns.Message:
    assert record_type in [rr.id for rr in dns.message.rdata.ResourceRecord.__subclasses__()], 'Unknown Resource ' + \
    f'Record type {record_type}'
    assert isinstance(domain, str), 'domain value should be string'
    assert try_ip_convert(dns_server), 'dns_server should be of value IPv4 or IPv6'
    m = await dns.Message.create_question(domain, record_type, dnssec=dnssec)
    result = await protocol.UdpClient.send_message(m, dns_server, timeout=timeout)
    return result


def sync_query(dns_server, domain, record_type=1, dnssec=False, timeout=5):
    return asyncio.run(query(dns_server, domain, record_type, dnssec, timeout=timeout))


from . import resolver


async def full_chain(domain, record_type=1, dnssec=False):
    return await resolver.find(domain, record_type, dnssec)


def sync_full_chain(domain, record_type=1, dnssec=False):
    return asyncio.run(resolver.find(domain, record_type, dnssec))
