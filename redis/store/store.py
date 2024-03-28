from redis.datastructures.basic.hash import Hash
from redis.datastructures.basic.string import RedisString
from typing import Dict, Any


class Store:
    def __init__(self):
        self.strings: Dict[str, RedisString] = {}
        self.hashes: Dict[str, Hash] = {}

    def getString(self, name: str):
        return self.strings.get(name, None)

    def setString(self, name: str, val: str):
        if name in self.strings:
            self.strings[name].val = val
        else:
            self.strings[name] = RedisString(name, val)

    def getHash(self, name) -> Hash | None:
        return self.hashes.get(name, None)
