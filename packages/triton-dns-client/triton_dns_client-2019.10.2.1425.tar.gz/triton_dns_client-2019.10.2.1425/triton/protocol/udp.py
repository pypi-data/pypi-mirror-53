import asyncio

from triton.dns.message import Message
from .exception import TimeoutError


class UdpClient:
    def __init__(self, loop, message: Message, on_con_lost, timeout=5):
        self.loop = loop
        self.message = message
        self.transport = None
        self.on_con_lost = on_con_lost
        loop.create_task(self.timeout_task(timeout))

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.message.Binary.full)

    def datagram_received(self, data, addr):
        task = asyncio.Task(self.to_async(data))

    @asyncio.coroutine
    def to_async(self, data):
        message = yield from Message.parse_bytes(data)
        self.on_con_lost.set_result(message)

    def error_received(self, exc):
        self.on_con_lost.set_exception(exc)

    def connection_lost(self, exc):
        return self.message

    async def timeout_task(self, time):
        await asyncio.sleep(time)
        try:
            if not self.on_con_lost.result():
                self.on_con_lost.set_exception(TimeoutError)
                self.on_con_lost.exception()
        except asyncio.base_futures.InvalidStateError:
            self.on_con_lost.set_exception(TimeoutError)
            self.on_con_lost.exception()

    @classmethod
    async def send_message(cls, message, host, port=53, timeout=5):
        loop = asyncio.get_event_loop()
        on_con_lost = loop.create_future()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: cls(loop, message, on_con_lost, timeout),
            remote_addr=(host, port))
        try:
            message = await on_con_lost
            return message
        finally:
            transport.close()
