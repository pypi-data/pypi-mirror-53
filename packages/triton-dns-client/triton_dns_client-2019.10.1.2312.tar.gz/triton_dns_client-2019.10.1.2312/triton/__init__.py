import asyncio

from . import dns
from . import protocol


async def query(dns_server, domain, record_type=1, dnssec=False, timeout=5) -> dns.Message:
    assert record_type in [rr.id for rr in dns.message.rdata.ResourceRecord.__subclasses__()], 'Unknown Resource ' + \
    f'Record type {record_type}'
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
