from collections import deque

class RedisList:
    def __init__(self, name: str):
        self.name = name
        self.list = deque([])

    def lpush(self, val: str | int):
        self.list.appendleft(val)

    def rpush(self, val: str | int):
        self.list.appendleft(val)

    def lrange(self, name: str, start: int, end: int):
        pass

    def rrange(self, name: str, start: int, end: int):
        pass