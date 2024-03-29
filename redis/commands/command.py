from ..store.store import Store
from typing import Dict
from resp.resp import RespType, serialize


def register_command(name):
    def decorator(cls):
        command_registry[name] = cls
        return cls

    return decorator


command_registry: Dict[str, 'Command'] = {}


class Command:
    def __init__(self, args):
        self.args = args
        self.store: Store | None = None
        self.reply_types = ()

    def execute(self):
        pass

    def ok(self) -> str:
        return serialize(RespType.SIMPLE_STRING, 'OK')

    def null(self):
        return serialize(RespType.NULL, '')

    def error(self, err: str) -> str:
        return serialize(RespType.SIMPLE_ERROR, err)

    @property
    def name(self):
        return self.__class__.__name__


@register_command('echo')
class Echo(Command):
    def __init__(self, args):
        super().__init__(args)
        self.arg = args[0]
        self.reply_types = 'BULK_STRING'

    def execute(self) -> str:
        return self.arg


@register_command('ping')
class Ping(Command):
    def __init__(self, args):
        super().__init__(args)
        self.reply_types = RespType.SIMPLE_STRING

    def execute(self) -> str:
        return serialize(RespType.SIMPLE_STRING, 'PONG')
