from .resolver import Resolver


class Connection:

    def __init__(self,
                 loop):
        self.loop = loop
        self.Resolver = Resolver(self)

