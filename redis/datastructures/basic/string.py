class RedisString:
    def __init__(self, name: str, val: str):
        self.name = name
        self.val = val

    def set(self, val: str):
        self.val = val

    def get(self):
        return self.val
