import base64
from typing import AnyStr, Dict

import aiohttp


async def download(url: str, result: Dict[str, str]):
    """ async download method """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result[url] = await response.text()


def base64_decode(data: AnyStr) -> str:
    """ adding missing padding '='

    return a base64 decoded string """
    if str == type(data):
        data = data.encode()
    data += b'='*(-len(data) % 4)
    return base64.b64decode(data).decode()


def base64_encode(data: AnyStr) -> str:
    """ return a base64 encoded string """
    if str == type(data):
        data = data.encode()
    return base64.b64encode(data).decode()


def urlsafe_base64_decode(data: AnyStr) -> str:
    """ adding missing padding '='

    return a urlsafe_base64 decoded string """
    if str == type(data):
        data = data.encode()
    data += b'='*(-len(data) % 4)
    return base64.urlsafe_b64decode(data).decode()


def urlsafe_base64_encode(data: AnyStr) -> str:
    """ return a urlsafe_base64 encoded string which removes paddings """
    if str == type(data):
        data = data.encode()
    return base64.urlsafe_b64encode(data).decode().rstrip("=")
