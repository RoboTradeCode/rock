from typing import TypedDict, Optional


class ExchangeConfig(TypedDict):
    api_key: Optional[str]
    secret_key: Optional[str]
