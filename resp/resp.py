from typing import List, Tuple
from enum import Enum, auto

CRLF = '\r\n'

class RespType(Enum):
    SIMPLE_STRING = auto()
    BULK_STRING = auto()
    SIMPLE_ERROR = auto()
    INTEGER = auto()
    ARRAY = auto()
    NULL = auto()

def serializeInt(n: int | str) -> str:
    if n is str:
        n = int(n)
    return f':{n}{CRLF}'


def serializeSimpleString(s: str) -> str:
    return f'+{s}{CRLF}'


def serializeSimpleError(e: str) -> str:
    return f'-{e}{CRLF}'


def serializeBulkString(s: str) -> str:
    if s == '-1':
        return f'$-1{CRLF}'
    return f'${len(s)}{CRLF}{s}{CRLF}'

def serialize(type: RespType, msg: str) -> str:
    if type == RespType.NULL:
        return serializeBulkString('-1')
    return {
        RespType.SIMPLE_STRING: serializeSimpleString,
        RespType.SIMPLE_ERROR: serializeSimpleError,
        RespType.INTEGER: serializeInt,
        RespType.BULK_STRING: serializeBulkString
    }[type](msg)


def serializeRequest(req: str) -> str:
    tokens = req.split()
    bulk_strings = ''.join(serializeBulkString(t) for t in tokens)
    return ''.join([f'*{len(tokens)}{CRLF}', bulk_strings, CRLF])


def take_until_cr_or_pos(msg: str, idx: int, pos: int = -1) -> Tuple[str, int]:
    res = []
    end = pos if pos > -1 else len(msg)
    while idx < end and msg[idx] != '\r':
        res.append(msg[idx])
        idx += 1
    return ''.join(res), idx


def deserializeInt(msg: str, idx: int = 0) -> Tuple[int, int]:
    idx += 1
    num, idx = take_until_cr_or_pos(msg, idx)
    return int(num), idx + 2


def deserializeSimpleString(msg: str, idx: int = 0) -> Tuple[str, int]:
    idx += 1
    s, idx = take_until_cr_or_pos(msg, idx)
    return s, idx + 2


def deserializeSimpleError(msg: str, idx: int = 0) -> Tuple[str, int]:
    err, idx = take_until_cr_or_pos(msg, idx)
    return err, idx + 2


def deserializeBulkString(msg: str, idx: int = 0) -> Tuple[str, int] | Tuple[None, int]:
    idx += 1
    str_len, idx = take_until_cr_or_pos(msg, idx)
    str_len = int(str_len)
    if str_len == -1:
        return None, idx + 2

    idx += 2
    bulk_string, idx = take_until_cr_or_pos(msg, idx, idx + str_len)
    return bulk_string, idx + 2


def deserializeArray(msg: str, idx: int = 0) -> Tuple[List, int]:
    idx += 1
    array_len, idx = take_until_cr_or_pos(msg, idx)
    result = [None for _ in range(int(array_len))]
    idx += 2
    for i in range(len(result)):
        result[i], idx = deserialize(msg, idx)
    return result, idx


def deserialize(msg: str, idx: int = 0):
    return {
        '*': deserializeArray,
        '$': deserializeBulkString,
        '+': deserializeSimpleString,
        '-': deserializeSimpleError,
        ':': deserializeInt
    }[msg[idx]](msg, idx)


def deserializeMsg(msg: str):
    return deserialize(msg)[0]


if __name__ == "__main__":
    print(deserializeMsg(f':5678{CRLF}'))
    print(deserializeMsg(f"*2{CRLF}*2{CRLF}$-1{CRLF}-ERR: WRONGTYPE{CRLF}*2{CRLF}:3{CRLF}$6{CRLF}jordie{CRLF}"))
    print(serializeRequest('set name jordie'))
