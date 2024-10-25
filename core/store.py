import socket
import threading
from .connection_state import ConnectionState

class Store:
    def __init__(self, sender_port=0, current_port=0, current_port_file=0, sender_port_file=0):
        self._lock = threading.Lock()
        self._connection_state = ConnectionState.CLOSED
        self._sender_port = sender_port
        self._current_port = current_port
        self._current_port_file = current_port_file
        self._sender_port_file = sender_port_file
        self._id = 0
        self._seq = 0
        self._clientSeq = -1

        self._peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._peer_socket.bind(('localhost', current_port))

    def set_sender_port(self, value):
        with self._lock:
            self._sender_port = value

    def get_sender_port(self):
        with self._lock:
            return self._sender_port

    def set_current_port(self, value):
        with self._lock:
            self._current_port = value

    def get_current_port(self):
        with self._lock:
            return self._current_port

    def set_connection_state(self, state):
        with self._lock:
            self._connection_state = state

    def get_connection_state(self):
        with self._lock:
            return self._connection_state

    def set_peer_socket(self, sock):
        with self._lock:
            self._peer_socket = sock

    def get_peer_socket(self):
        with self._lock:
            return self._peer_socket

    def set_current_port_file(self, value):
        with self._lock:
            self._current_port_file = value

    def get_current_port_file(self):
        with self._lock:
            return self._current_port_file

    def set_sender_port_file(self, value):
        with self._lock:
            self._sender_port_file = value

    def get_sender_port_file(self):
        with self._lock:
            return self._sender_port_file

    def set_id(self, value):
        with self._lock:
            self._id = value

    def get_id(self):
        with self._lock:
            return self._id

    def set_seq(self, value):
        with self._lock:
            self._seq = value

    def get_seq(self):
        with self._lock:
            return self._seq

    def set_client_seq(self, value):
        with self._lock:
            self._clientSeq = value

    def get_client_seq(self):
        with self._lock:
            return self._clientSeq
