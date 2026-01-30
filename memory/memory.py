memory = {}


def remember(key: str, value: str):
    memory[key] = value


def recall(key: str):
    return memory.get(key)