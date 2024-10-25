from enum import Enum

class ConnectionState(Enum):
    CLOSED = 0
    SYN_SENT = 1
    ESTABLISHED = 2
