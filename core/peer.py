from .message_receiver import MessageReceiver
from .message_sender import MessageSender
from .store import Store
from .file_receiver import FileReceiver
from .file_sender import FileSender
from core.packet import DataPacket
from core.utils import calculate_ascii_comb


class Peer:

    def __init__(self):
        self.store = None
        self.file_receiver = None
        self.file_sender = None
        self.message_receiver = None
        self.message_sender = None

    def initialize_utils(self):
        self.message_receiver = MessageReceiver(self.message_sender, self.store, message_emitter=self.emitter)
        self.file_receiver = FileReceiver(self.store, message_emitter=self.emitter)
        self.file_sender = FileSender(self.store)

    def run(self, current_port, sender_port, current_port_file, sender_port_file, emitter):
        self.emitter = emitter
        self.store = Store(current_port, sender_port, current_port_file, sender_port_file)
        self.message_sender = MessageSender(self.store)
        want_to_initiate = input("do you want to initiate connection (y or n): ")
        if want_to_initiate == "y":
            print("trying to connect")
            self.message_sender.send_packet_with_timeout(
                DataPacket(self.store.get_id(), self.store.get_seq(), "SYN", False, calculate_ascii_comb("SYN")))
            # connection_state = ConnectionState.SYN_SENT
            self.store.set_id(self.store.get_id() + 1)
            self.store.set_seq(self.store.get_seq() + len("SYN"))
            self.message_sender.send_packet(
                DataPacket(self.store.get_id(), self.store.get_seq(), "ACK", False, calculate_ascii_comb("ACK"), 0))
            self.store.set_id(self.store.get_id() + 1)
            self.store.set_seq(self.store.get_seq() + len("ACK"))
            # connection_state = ConnectionState.ESTABLISHED
        else:
            message, peer1_address = self.store.get_peer_socket().recvfrom(1060)
            self.message_sender.send_packet_with_timeout(
                DataPacket(self.store.get_id(), self.store.get_seq(), "SYNACK", False, calculate_ascii_comb("SYNACK"),
                           0))
            self.store.set_id(self.store.get_id() + 1)
            self.store.set_seq(self.store.get_seq() + len("SYNACK"))
            # connection_state = ConnectionState.ESTABLISHED
        self.initialize_utils()
        print("connection established")
