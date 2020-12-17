import aiohttp
import asyncio

from loguru import logger

list_proxy = [
    '109.160.76.209:8080',
    '5.58.50.5:8080',
    '103.78.252.65:8080',
    '117.204.255.151:8080',
    '171.97.131.203:8080',
    '140.227.11.26:3128',
    '101.108.172.74:8080',
    '136.228.165.138:8080',
    '103.214.113.28:8080',
    '160.238.251.142:3128',
    '5.58.88.175:8080',
    '193.192.176.249:8080',
    '14.207.85.231:8080',
    '118.174.232.181:8080',
    '179.222.94.2:8080',
    '168.90.121.44:8080',
    '103.126.218.138:8080',
    '183.88.224.206:8080',
    '182.253.246.187:8080',
    '177.106.55.20:3128'
]


async def fetch_proxy(url: str) -> tuple:
    logger.info(f'parse url{url}')
    try:
        async with aiohttp.ClientSession() as session:
            logger.info(f'parse url{url}')
            async with session.get(f'http://ya.ru', proxy=f'{url}') as response:
                logger.info(f'Status {response.status}')
                return url, response.status
    except ValueError:
        return "", 500


async def fetch_fastest_proxy() -> str:
    futures = [fetch_proxy(url) for url in list_proxy]

    done, pending = await asyncio.wait(
        futures
    )
    best_url = ""
    for fut in pending:
        fut.cancel()

    for fut in done:
        status_code, best_url = fut.result()
        logger.info(f'return status: {status_code}, url {url}')
    return best_url


loop = asyncio.get_event_loop()
res = loop.run_until_complete(fetch_fastest_proxy())
loop.close()

logger.info(f'best url {res}')
