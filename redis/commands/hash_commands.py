from redis.datastructures.basic.hash import Hash
from ..store.store import Store
from command import Command


class HashCommand(Command):
    def __init__(self, name: str, hash_name: str):
        super().__init__(name)
        self.hash_name = hash_name

    @property
    def hash(self) -> Hash:
        _hash = self.store.getHash(self.hash_name)
        if _hash:
            return _hash
        return Hash(self.hash_name)

    def execute(self):
        pass


class Hget(HashCommand):
    def __init__(self, hash_name: str, field_name: str):
        super().__init__('hget', hash_name)
        self.field_name = field_name

    def execute(self):
        return self.hash.hget(self.field_name)
