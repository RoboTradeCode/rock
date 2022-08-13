import websockets
from typing import Callable


def keep_connection(io: Callable) -> Callable:
    async def wrapped(self, *args, **kwargs):
        if self.websocket is None:
            await self.connect()

        while True:
            try:
                return await io(self, *args, **kwargs)
            except websockets.ConnectionClosed:
                await self.connect()

    return wrapped
