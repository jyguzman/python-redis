from command import Command


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
        self.key = args[1]
        self.val = args[2]

    def execute(self):
        self.store.setString(self.key, self.val)


class Get(StringCommand):
    def __init__(self, *args):
        super().__init__(*args)
        self.key = args[1]

    def execute(self):
        if not self.exists(self.key):
            return None
        return self.store.getString(self.key).val
