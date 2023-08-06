from .resolver import Resolver


class Connection:

    def __init__(self, loop, server_connector):
        self.loop = loop
        self.server_connector = server_connector
        self.Resolver = Resolver(self)
