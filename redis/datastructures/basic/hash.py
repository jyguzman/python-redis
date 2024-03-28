class Hash:
    def __init__(self, name: str, **pairs):
        self.name = name
        self.pairs = pairs

    def hset(self, key):
        pass

    def hget(self, key):
        return self.pairs[key]