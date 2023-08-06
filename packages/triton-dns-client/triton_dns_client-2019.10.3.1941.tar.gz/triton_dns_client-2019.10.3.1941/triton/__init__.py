import asyncio
import typing
from .resolver.local_cache import Cache
loop = asyncio.get_event_loop()
cache = Cache(loop)
from . import resolver
from . import dns
from . import protocol





from . import resolver
from .query import query, sync_query


async def full_chain(domain, record_type=1, dnssec=False):
    return await resolver.find(domain, record_type, dnssec)


def sync_full_chain(domain, record_type=1, dnssec=False):
    rs = resolver.ChainResolver(domain, record_type)
    return loop.run_until_complete(rs.go())
