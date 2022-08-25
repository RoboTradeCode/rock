import hmac
from base64 import b64encode
from hashlib import sha512
from time import time_ns


class EventFactory:
    def __init__(self, api_key: str, secret: str):
        self.api_key = api_key
        self.secret = secret

    def login(self) -> dict:
        nonce = self._nonce()
        sign = self._sign(nonce)
        event = {
            "method": "login",
            "id": 1,
            "api_key": self.api_key,
            "sign": sign,
            "nonce": nonce,
        }
        return event

    @staticmethod
    def subscribe(topics: list[str]) -> dict:
        event = {"id": 1, "method": "subscribe", "topics": topics}
        return event

    @staticmethod
    def _nonce() -> int:
        return time_ns()

    def _sign(self, nonce: int) -> str:
        key = self.secret.encode()
        msg = f"{self.api_key}{nonce}".encode()
        digest = hmac.new(key, msg, sha512).digest()
        sign = b64encode(digest).decode()
        return sign
