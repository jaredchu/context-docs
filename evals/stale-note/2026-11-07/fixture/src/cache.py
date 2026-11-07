class Cache:
    """Ephemeral per-instance cache; no external service or persistence."""
    def __init__(self):
        self.values = {}

    def put(self, key, value):
        self.values[key] = value

    def get(self, key):
        return self.values.get(key)
