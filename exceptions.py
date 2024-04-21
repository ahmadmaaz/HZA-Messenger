class CorruptedPacket(Exception):
    """CorruptedPacket exception class."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message