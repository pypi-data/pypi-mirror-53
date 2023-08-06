import typing
from ipaddress import IPv6Address, IPv4Address, AddressValueError
from triton.dns import Message, message
import triton


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


@triton.cache.find_or_store
async def query(dns_server, domain: typing.Text, record_type=1, dnssec=False, timeout=0.8, use_cache=True) -> Message:
    assert record_type in [rr.id for rr in message.rdata.ResourceRecord.__subclasses__()], 'Unknown Resource ' + \
                                                                                               f'Record type {record_type}'
    assert isinstance(domain, str), 'domain value should be string'
    assert try_ip_convert(dns_server), 'dns_server should be of value IPv4 or IPv6'
    m = await Message.create_question(domain, record_type, dnssec=dnssec)
    result = await triton.protocol.UdpClient.send_message(m, dns_server, timeout=timeout)
    return result


def sync_query(dns_server, domain, record_type=1, dnssec=False, timeout=5, use_cache=True):
    return triton.loop.run_until_complete(query(dns_server, domain, record_type, dnssec, timeout=timeout, use_cache=use_cache))
