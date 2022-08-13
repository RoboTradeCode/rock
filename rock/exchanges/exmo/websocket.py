import json
import logging
import websockets
from .enums import EventCode, EventType
from .factories import EventFactory
from .utils import keep_connection

logger = logging.getLogger(__name__)


# TODO: Use class methods instead static methods
class WebsocketApi:
    def __init__(self, uri: str, api_key: str = None, secret: str = None):
        self.uri = uri
        self.event_factory = EventFactory(api_key, secret)
        self.websocket: websockets.WebSocketClientProtocol = None

    async def connect(self):
        websocket = await websockets.connect(self.uri)
        self.websocket = websocket

    async def login(self):
        event = self.event_factory.login()
        await self._send(event)

    async def subscribe(self, topics: list[str]):
        event = self.event_factory.subscribe(topics)
        await self._send(event)

    async def wait_state(self) -> dict:
        while event := await self._recv():
            if event.get("event") in [EventType.SNAPSHOT, EventType.UPDATE]:
                return event

    @keep_connection
    async def _send(self, event: dict):
        message = json.dumps(event)
        await self.websocket.send(message)

    @keep_connection
    async def _recv(self) -> dict:
        message = await self.websocket.recv()
        event = json.loads(message)
        self._raise_for_event(event)
        return event

    @staticmethod
    def _raise_for_event(event: dict):
        WebsocketApi._raise_for_code(event)
        WebsocketApi._raise_for_event_type(event)

    @staticmethod
    def _raise_for_code(event: dict):
        message = event.get("message")
        match event.get("code"):
            case EventCode.MAINTENANCE_IN_PROGRESS:
                raise RuntimeError(message)

    @staticmethod
    def _raise_for_event_type(event: dict):
        message = event.get("message")
        match event.get("event"):
            case EventType.ERROR:
                raise RuntimeError(message)
            case EventType.INFO:
                logger.info(message)
            case EventType.LOGGED_IN:
                logger.info("Logged in")
            case EventType.SUBSCRIBED:
                topic = event.get("topic")
                logger.info(f"Subscribed topic: {topic}")
