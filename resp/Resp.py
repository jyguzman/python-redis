from enum import auto

class Resp:

    CRLF = '\r\n'
    def __init__(self):
        pass

    def serializeInteger(self, n: int) -> str:
        return f":{n}{self.CRLF}"

    def serializeSimpleString(self, s: str) -> str:
        return f"+{s}{self.CRLF}"

    def serializeError(self, err: str) -> str:
        return f"-{err}{self.CRLF}"

    def serializeBulkString(self, s: str) -> str:
        return ""


if __name__ == "__main__":
    resp = Resp()
    print(resp.serializeInteger(10))