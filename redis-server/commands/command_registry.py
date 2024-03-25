def register_command(name):
    def decorator(cls):
        command_registry[name] = cls
        return cls
    return decorator


command_registry = {}