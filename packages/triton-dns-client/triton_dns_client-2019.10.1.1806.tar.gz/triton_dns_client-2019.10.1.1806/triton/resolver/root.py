from ipaddress import IPv4Address, IPv6Address

import triton
from triton import query

# According to IANA https://www.iana.org/domains/root/servers
root_ns = {
    'a.root-servers.net': [IPv4Address('198.41.0.4'), IPv6Address('2001:503:ba3e::2:30')],
    'b.root-servers.net': [IPv4Address('199.9.14.201'), IPv6Address('2001:500:200::b')],
    'c.root-servers.net': [IPv4Address('192.33.4.12'), IPv6Address('2001:500:2::c')],
    'd.root-servers.net': [IPv4Address('199.7.91.13'), IPv6Address('2001:500:2d::d')],
    'e.root-servers.net': [IPv4Address('192.203.230.10'), IPv6Address('2001:500:a8::e')],
    'f.root-servers.net': [IPv4Address('192.5.5.241'), IPv6Address('2001:500:2f::f')],
    'g.root-servers.net': [IPv4Address('192.112.36.4'), IPv6Address('2001:500:12::d0d')],
    'h.root-servers.net': [IPv4Address('198.97.190.53'), IPv6Address('2001:500:1::53')],
    'i.root-servers.net': [IPv4Address('192.36.148.17'), IPv6Address('2001:7fe::53')],
    'j.root-servers.net': [IPv4Address('192.58.128.30'), IPv6Address('2001:503:c27::2:30')],
    'k.root-servers.net': [IPv4Address('193.0.14.129'), IPv6Address('2001:7fd::1')],
    'l.root-servers.net': [IPv4Address('199.7.83.42'), IPv6Address('2001:500:9f::42')],
    'm.root-servers.net': [IPv4Address('202.12.27.33'), IPv6Address('2001:dc3::35')],
}


class ResolveStatus:
    def __init__(self):
        self.secure = True


async def find(label, type=1, dnssec=False):
    status = ResolveStatus()
    queries = ['.'.join(label.split('.')[::-1][:n + 1][::-1]) for n in range(len(label.split('.')))]
    zone_ns, zone_keys, zone_ds = await subfind(status, queries[0])  # Searching for first zone
    for q in queries[1:]:  # Finding each subdomain zone nameserver
        zone = await subfind(status, q, zone_ns, zone_ds)
        if zone[0].authority:  # NS answers are placed in authority section.
            zone_ns, zone_keys, zone_ds = zone
        else:  # If no for zone => no point in trying to find its subzones
            break
    for ns in zone_ns.additional:  # Trying all nameservers
        try:
            result = await query(str(ns.rdata.address), label, type, dnssec)
            if result:
                return result
        except triton.protocol.exception.TimeoutError:
            continue
        except OSError:
            print(f'Cannot connect to {ns.rdata.address}')
        except ConnectionRefusedError:
            print(f'Server {ns.rdata.address} refused connection')


async def subfind(status, label, zone_ns=None, zone_ds=None):
    if not zone_ns:
        return await in_root(status, label)
    else:
        return await in_sub(status, label, zone_ns, zone_ds)


async def in_sub(status, label, zone_ns, parent_ds):
    for ns in zone_ns.additional:
        try:
            zone = await query(str(ns.rdata.address), label, 2, dnssec=True)
            zone_keys = await query(str(ns.rdata.address), ''.join(label.split('.')[1:]), 48, dnssec=True)
            zone_ds = await query(str(ns.rdata.address), label, 43, dnssec=True)
            if zone_ds.answer:
                assert await zone_ds.verify_rrsig(zone_keys)
            if not zone_ds.answer:
                status.secure = False
            if status.secure:
                try:
                    assert await zone_ds.verify_rrsig(zone_keys)
                    assert await zone_keys.verify_rrsig(zone_keys)
                    assert await zone.verify_rrsig(zone_keys)
                except triton.dns.dnssec.exceptions.VerificationError:
                    status.secure = False
            if zone:
                return zone, zone_keys, zone_ds
        except triton.protocol.exception.TimeoutError:
            continue
        except OSError:
            print(f'Server {ns.rdata.address} refused connection')
            continue


async def in_root(status, label):
    for nsname, ip in root_ns.items():
        try:
            zone = await query(str(ip[0]), label, 2, dnssec=True, timeout=1)
            zone_keys = await query(str(ip[0]), '.', 48, dnssec=True, timeout=1)
            zone_ds = await query(str(ip[0]), label, 43, dnssec=True, timeout=1)
            if not zone_ds.answer:
                status.secure = False
            if status.secure:
                try:
                    assert await zone_ds.verify_rrsig(zone_keys)
                    assert await zone_keys.verify_rrsig(zone_keys)
                    assert await zone.verify_rrsig(zone_keys)
                except triton.dns.dnssec.exceptions.VerificationError:
                    status.secure = False
            if zone:
                return zone, zone_keys, zone_ds
        except triton.protocol.exception.TimeoutError:
            continue
