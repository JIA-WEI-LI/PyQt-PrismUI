class FontValue:
    def __init__(self, raw: str):
        self.raw = raw

    def __int__(self):
        if isinstance(self.raw, str) and self.raw.endswith("px"):
            return int(self.raw[:-2])
        raise ValueError("Cannot convert font value to int")

    def __str__(self):
        return self.raw