import base64
import hashlib
import hmac
import json
import time
import websockets


class Websocket:
    def __init__(self, uri: str, api_key: str = None, api_secret: str = None):
        self._client: websockets.WebSocketClientProtocol = None
        self._uri = uri
        self._api_key = api_key
        self._api_secret = api_secret

    async def connect(self) -> None:
        """
        Установить соединение с сервером

        Когда соединение с сервером установлено, сервер отправляет приветственное
        сообщение с идентификатором сеанса в поле JSON session_id
        """
        self._client = await websockets.connect(self._uri)
        await self.recv()

    async def login(self) -> None:
        """
        Аутентифицироваться на сервере

        Аутентифицированный API позволяет получать информацию о сделках пользователей,
        изменениях кошельков и ордеров в режиме реального времени. Чтобы использовать
        этот API, необходимо установить соединение, а затем аутентифицироваться на
        сервере, используя этот метод. В противном случае соединение будет прервано на
        стороне сервера через 30 секунд
        """
        nonce = self._nonce()
        sign = self._sign(nonce)
        event = {
            "method": "login",
            "api_key": self._api_key,
            "sign": sign,
            "nonce": nonce,
        }
        await self._send(event)
        await self.recv()

    async def subscribe(self, topics: list[str]) -> None:
        """
        Подписаться на получение данных

        При успехе придёт сообщение с типом subscribed. После получения этого
        сообщения все данные, связанные с темами, будут отправляться в соединение. При
        ошибке придёт сообщение с типом error
        """
        event = {"id": 1, "method": "subscribe", "topics": topics}
        await self._send(event)
        await self.recv()

    async def recv(self) -> dict:
        """
        Получить от сервера сообщение, декодировав его из формата JSON
        """
        message = await self._client.recv()
        event = json.loads(message)
        return event

    async def _send(self, event: dict) -> None:
        """
        Отправить на сервер сообщение, закодировав его в формат JSON
        """
        message = json.dumps(event)
        await self._client.send(message)

    def _sign(self, nonce: int) -> str:
        """
        Получить подпись

        Подпись представляет собой объединённую строку api_key и nonce, зашифрованную
        методом HMAC-SHA512 с использованием секретного ключа. Байты подписи должны быть
        представлено в виде строки base64. Формула:
        sign = base64(sha512(api_key + nonce, api_secret))
        """
        key = self._api_secret.encode()
        msg = f"{self._api_key}{nonce}".encode()
        digest = hmac.new(key, msg, hashlib.sha512).digest()
        sign = base64.b64encode(digest).decode()
        return sign

    @staticmethod
    def _nonce() -> int:
        """
        Получить nonce

        Nonce представляет собой числовое значение (>0), которое никогда не должно
        повторяться или уменьшаться. Используется при получении подписи для сообщения
        """
        return time.time_ns()
