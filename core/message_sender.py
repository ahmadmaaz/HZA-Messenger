from .store import Store
import pickle
from core.utils import *
import socket
from core.packet import DataPacket

class MessageSender:
    def __init__(self, store: Store):
        self.store = store

    def send_message(self, msg, emitter, callback=None):
        message_parts = [msg[i:i + 1000] for i in range(0, len(msg), 1000)]
        for i in range(0, len(message_parts)):
            data = message_parts[i]
            self.send_packet_with_timeout(
                DataPacket(self.store.get_id(), self.store.get_seq(), data, i == len(message_parts) - 1,
                           calculate_ascii_comb(data))
            )
            self.store.set_seq(self.store.get_seq() + len(data))
        emitter.msg.emit("0" + msg)
        self.store.set_id(self.store.get_id() + 1)
        if callback:
            callback()

    def send_packet_with_timeout(self, data_packet):
        print(self.store.get_peer_socket())
        while True:
            try:
                self.store.get_peer_socket().sendto(pickle.dumps(data_packet),
                                                    ('localhost', self.store.get_sender_port()))
                self.store.get_peer_socket().settimeout(.2)
                message, peer1_address = self.store.get_peer_socket().recvfrom(1060)
                packet = pickle.loads(message)
                validate_packet(packet, self.store.get_seq(), clientSeq=self.store.get_client_seq())
                self.store.get_peer_socket().settimeout(0)
                return packet
            except socket.timeout:
                print("Timeout occurred. Retrying...")
            except CorruptedPacket as e:
                print(e)
            except Exception as e:
                pass

    def send_packet(self, data_packet):
        self.store.get_peer_socket().sendto(pickle.dumps(data_packet), ('localhost', self.store.get_sender_port()))
