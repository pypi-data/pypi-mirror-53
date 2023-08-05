import asyncio
import re
import urllib.parse as urlparse
from typing import Dict, List

from .. import utils

__all__=[
    "SSNode"
]

class SSNode(object):
    def __init__(self):
        self.method: str
        self.password: str
        self.hostname: str
        self.port: str
        self.plugin: str
        self.group: str
        self.obfs: str
        self.obfs_host: str
        self.tag: str


def _download(url: str) -> List[str]:
    """ download single ss subscription resource """
    return _download_urls([url])[url]


def _download_urls(urls: List[str]) -> Dict[str, List[str]]:
    """ donwload multiplied ss subscription resource """
    if len(urls) == 0:
        return {}
    contents: Dict[str, str] = {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [utils.download(url, contents) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return {url: (contents[url].splitlines()
                  if contents[url].startswith("ss://")
                  else utils.base64_decode(contents[url]).splitlines())
            for url in urls}


def deserialize(sub_url: str) -> List[SSNode]:
    """ download single ss subscription url and deserialize it to SSNodes """
    return deserialize_urls([sub_url])[sub_url]


def deserialize_urls(sub_urls: List[str]) -> Dict[str, List[SSNode]]:
    """ download multiplied ss subscription urls and store deserialized 
    SSNodes in dict of which the key represent the subscription url """
    serialized_urls: Dict[str, List[SSNode]] = {}

    plugin_re = re.compile(
        "(?P<plugin>.*);obfs=(?P<obfs>.*);obfs-host=(?P<obfs_host>.*)")
    netloc_re = re.compile("(?P<user_info>.*)@(?P<hostname>.*):(?P<port>.*)")

    for item in _download_urls(sub_urls).items():
        sub_url = item[0]
        serialized_url: List[SSNode] = []
        for url in item[1]:
            split_result = urlparse.urlsplit(url)

            query: Dict[str, str] = {item[0]: " ".join(item[1]) for item in urlparse.parse_qs(
                split_result.query, keep_blank_values=True).items()}

            plugin = re.match(plugin_re, urlparse.unquote(query["plugin"]))
            netloc = re.match(netloc_re, split_result.netloc)
            user_info = utils.urlsafe_base64_decode(netloc["user_info"])

            node = SSNode()
            node.hostname = urlparse.unquote(netloc["hostname"])
            node.port = urlparse.unquote(netloc["port"])
            node.method, node.password = user_info.split(":", 1)
            node.plugin = plugin["plugin"]
            node.group = utils.urlsafe_base64_decode(query["group"])
            node.obfs = plugin["obfs"]
            node.obfs_host = plugin["obfs_host"]
            node.tag = urlparse.unquote(split_result.fragment)
            serialized_url.append(node)
        serialized_urls[sub_url] = serialized_url
    return serialized_urls


def serialize(node: List[SSNode]) -> List[str]:
    pass
