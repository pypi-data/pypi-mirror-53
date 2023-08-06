from ipaddress import IPv4Address, IPv6Address

import triton
from triton import query


class ResolveStatus:
    def __init__(self):
        self.secure = True


class ChainResolver:

    # According to IANA https://www.iana.org/domains/root/servers
    root_nameservers = {
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

    def __init__(self, target_domain, target_type):
        self.target_domain = target_domain
        self.target_type = target_type
        self.current_nameservers = self.__class__.root_nameservers
        self.status = ResolveStatus()
        self.current_resolve_depth = 1
        self.result = None

    @property
    def current_resolve_domain(self):
        return '.'.join(self.target_domain.split('.')[-self.current_resolve_depth:])

    async def update_nameservers(self, zone_nameservers):
        if self.target_domain in self.current_nameservers:
            return
        if zone_nameservers.additional.by_type(triton.dns.message.rdata.A) or \
                zone_nameservers.additional.by_type(triton.dns.message.rdata.AAAA):
            self.current_nameservers = {}
            for ns_a in zone_nameservers.additional.by_type(triton.dns.message.rdata.A):
                if self.current_nameservers.get(ns_a.name.lower()):
                    self.current_nameservers[ns_a.name.lower()].append(ns_a.rdata.address)
                else:
                    self.current_nameservers[ns_a.name.lower()] = [ns_a.rdata.address]
            for ns_aaaa in zone_nameservers.additional.by_type(triton.dns.message.rdata.AAAA):
                if self.current_nameservers.get(ns_aaaa.name.lower()):
                    self.current_nameservers[ns_aaaa.name.lower()].append(ns_aaaa.rdata.address)
                else:
                    self.current_nameservers[ns_aaaa.name.lower()] = [ns_aaaa.rdata.address]
        else:
            self.current_nameservers = {}
            for ns in zone_nameservers.authority.by_type(triton.dns.message.rdata.NS):
                aaaa_rr = await ChainResolver(ns.rdata.nsdname.label.lower(), 28).go()
                a_rr = await ChainResolver(ns.rdata.nsdname.label.lower(), 1).go()
                if aaaa_rr:
                    for aaaa in aaaa_rr.answer.by_type(triton.dns.message.rdata.AAAA):
                        if self.current_nameservers.get(aaaa.name.lower()):
                            self.current_nameservers[aaaa.name.lower()].append(aaaa.rdata.address)
                        else:
                            self.current_nameservers[aaaa.name.lower()] = [aaaa.rdata.address]
                if a_rr:
                    for a in a_rr.answer.by_type(triton.dns.message.rdata.A):
                        if self.current_nameservers.get(a.name.lower()):
                            self.current_nameservers[a.name.lower()].append(a.rdata.address)
                        else:
                            self.current_nameservers[a.name.lower()] = [a.rdata.address]

    async def go(self):
        if self.result:
            return self.result
        await self.find_target_zone_nameservers()
        for ns_ips in self.current_nameservers.values():
            for ip in ns_ips:
                try:
                    result = await query(str(ip), self.current_resolve_domain, self.target_type,
                                         dnssec=self.status.secure)
                    if result:
                        if self.status.secure:
                            try:
                                zone_keys = await query(str(ip), self.current_resolve_domain, 48)
                            except triton.protocol.exception.TimeoutError:
                                continue
                            assert await result.verify_rrsig(zone_keys)
                        self.result = result
                        return result
                except OSError:
                    continue

    async def find_target_zone_nameservers(self, parent_zone_ds=None):
        for ns_ips in self.current_nameservers.values():
            for ip in ns_ips:
                if self.current_resolve_domain not in self.current_nameservers:
                    try:
                        zone_nameservers = await query(str(ip), self.current_resolve_domain, 2)
                    except OSError:
                        continue
                    except triton.protocol.exception.TimeoutError:
                        continue
                    if self.status.secure:
                        try:
                            zone_keys = await query(str(ip), '.'.join(self.current_resolve_domain.split('.')[1:]), 48)
                            zone_ds = await query(str(ip), self.current_resolve_domain, 43)
                            try:
                                assert await zone_ds.verify_rrsig(zone_keys)
                                if parent_zone_ds and self.current_resolve_depth != 1:
                                    assert await zone_keys.verify_keys(parent_zone_ds)
                                    parent_zone_ds = zone_ds
                                parent_zone_ds = zone_ds
                                assert await zone_keys.verify_rrsig(zone_keys)
                                assert await zone_nameservers.verify_rrsig(zone_keys)
                            except triton.dns.dnssec.exceptions.VerificationError:
                                self.status.secure = False
                        except triton.protocol.exception.TimeoutError:
                            pass
                    await self.update_nameservers(zone_nameservers)
                    if self.current_resolve_domain != self.target_domain:
                        self.current_resolve_depth += 1
                        return await self.find_target_zone_nameservers(parent_zone_ds)
                    else:
                        return True
                else:
                    if self.current_resolve_domain != self.target_domain:
                        self.current_resolve_depth += 1
                        return await self.find_target_zone_nameservers()
                    else:
                        return True