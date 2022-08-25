import asyncio

import aiohttp
import orjson


async def make_request(method: str, host: str, endpoint: str, session: aiohttp.ClientSession, protocol='https',
                       params: dict = None) -> dict:
    """

    :param host: Хост для совершения запроса;
    :param endpoint: Эндпоинт для совершения запроса;
    :param session: Сессия aiohttp для совершения запросов;
    :param protocol: Протокол для совершения запроса. По-умолчанию HTTPS;
    :param params: словарь параметров, которые передаются в запросе;
    :return: Результат запроса JSON, представленный в виде dict
    """
    url = f'{protocol}://{host}{endpoint}'
    if params:
        url = f'{url}?{"&".join([f"{key}={value}" for key, value in params.items()])}'
    response = await session.get(url)

    result_json = orjson.loads(await response.text())
    return result_json


async def main():
    async with aiohttp.ClientSession() as session:
        result = await make_request('get', 'api.binance.com', '/api/v3/depth', session, params={
            'symbol': 'BTCUSDT',
            'limit': 10
        })
        import pprint
        pprint.pprint(result)


if __name__ == '__main__':
    asyncio.run(main())
