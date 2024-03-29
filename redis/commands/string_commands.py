from command import Command
from resp.resp import RespType, serialize

class StringCommand(Command):
    def __init__(self, *args):
        super().__init__(*args)

    def getString(self, name: str):
        return self.store.getString(name)

    def exists(self, name: str):
        return name in self.store.strings


class Set(StringCommand):
    def __init__(self, *args):
        super().__init__(*args)
        self.key = args[0]
        self.val = args[1]
        self.reply_types = (RespType.SIMPLE_STRING)

    def execute(self):
        self.store.setString(self.key, self.val)
        return self.ok


class Get(StringCommand):
    def __init__(self, *args):
        super().__init__(*args)
        self.key = args[0]
        self.reply_types = (RespType.BULK_STRING, RespType.NULL)

    def execute(self):
        if not self.exists(self.key):
            return self.null
        return self.store.getString(self.key).val
