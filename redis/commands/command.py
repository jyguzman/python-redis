from ..store.store import Store
from typing import Dict

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
