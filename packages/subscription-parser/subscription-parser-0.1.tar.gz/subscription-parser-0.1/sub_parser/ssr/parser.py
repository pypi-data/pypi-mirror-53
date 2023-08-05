import asyncio
import re
import urllib.parse as urlparse
from typing import Dict, List

from .. import utils


class SSRNode(object):
    def __init__(self):
        self.host: str
        self.port: str
        self.protocol: str
        self.method: str
        self.obfs: str
        self.password: str
        self.obfsparam: str
        self.protoparam: str
        self.remarks: str


def _download(url: str) -> List[str]:
    """ download single ssr subscription resource """
    return _download_urls([url])[url]


def _download_urls(urls: List[str]) -> Dict[str, List[str]]:
    """ download multiplied ssr subscription resource """
    if len(urls) == 0:
        return {}
    contents: Dict[str, str] = {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [utils.download(url, contents) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return {url: (["ssr://"+utils.urlsafe_base64_decode(l.replace("ssr://", "", 1)) for l in contents[url].splitlines()]
                  if contents[url].startswith("ssr://")
                  else["ssr://"+utils.urlsafe_base64_decode(l.replace("ssr://", "", 1)) for l in utils.urlsafe_base64_decode(contents[url]).splitlines()])
            for url in urls}


def deserialize(sub_url: str) -> List[SSRNode]:
    """ download single ssr subscription url and deserialize it to SSRNodes """
    return deserialize_urls([sub_url])[sub_url]


def deserialize_urls(sub_urls: List[str]) -> Dict[str, List[SSRNode]]:
    """ download multiplied ssr subscription urls and store deserialized 
    SSRNodes in dict of which the key represent the subscription url """
    serialized_urls: Dict[str, List[SSRNode]] = {}
    netloc_re = re.compile(
        "(?P<host>.*):(?P<port>.*):(?P<protocol>.*):(?P<method>.*):(?P<obfs>.*):(?P<password>.*)")

    for item in _download_urls(sub_urls).items():
        sub_url = item[0]
        serialized_url: List[SSRNode] = []
        for url in item[1]:
            split_result = urlparse.urlsplit(url)
            netloc = re.match(netloc_re, split_result.netloc)
            query: Dict[str, str] = {item[0]: "+".join(item[1]).replace(" ", "+") for item in urlparse.parse_qs(
                split_result.query, keep_blank_values=True).items()}

            node = SSRNode()
            node.host = netloc["host"]
            node.port = netloc["port"]
            node.protocol = netloc["protocol"]
            node.method = netloc["method"]
            node.obfs = netloc["obfs"]
            node.obfsparam = utils.urlsafe_base64_decode(query["obfsparam"])
            node.password = utils.urlsafe_base64_decode(netloc["password"])
            node.protoparam = utils.urlsafe_base64_decode(query["protoparam"])
            node.remarks = utils.urlsafe_base64_decode(query["remarks"])

            serialized_url.append(node)
        serialized_urls[sub_url] = serialized_url
    return serialized_urls


def serialize(node: List[SSRNode]) -> List[str]:
    pass
