import pickle
from core.exceptions import CorruptedPacket, DropPacket
from core.packet import DataPacket
from core.utils import calculate_ascii_comb, validate_packet
from .store import *

class MessageReceiver:
    def __init__(self, message_sender, store: Store, message_emitter):
        self.message_sender = message_sender
        self.store = store
        self.thread = threading.Thread(target=self.listen_to_messages, args=(message_emitter,))
        self.thread.start()

    def listen_to_messages(self, emitter):
        chunks = set()
        message_sender = self.message_sender
        print(self.store.get_peer_socket())
        while True:
            try:
                message, peer1_address = self.store.get_peer_socket().recvfrom(1060)
                if peer1_address[1] != self.store.get_sender_port():
                    raise Exception("Received packet from different port")
                packet = pickle.loads(message)
                if packet.data in ["SYNACK", "SYN"] and packet.seq == 0:  # a peer is still stuck in handshake
                    msgToSend = "ACK" if packet.data == "SYNACK" else "SYNACK"
                    message_sender.send_packet(pickle.dumps(
                        DataPacket(id, self.store.get_seq(), msgToSend, False, calculate_ascii_comb(msgToSend), 0)))
                    continue
                if self.store.get_client_seq() >= packet.seq:
                    message_sender.send_packet(
                        DataPacket(id, self.store.get_seq(), "True", False, calculate_ascii_comb("True"), packet.seq))
                    continue
                validate_packet(packet, seq=None, clientSeq=self.store.get_client_seq())
                chunks.add((packet.data, packet.seq))
                self.store.set_client_seq(packet.seq)
                if packet.finalChunk:
                    sorted_chunks = sorted(chunks, key=lambda x: x[1])
                    emitter.msg.emit("1" + ''.join(chunk[0] for chunk in sorted_chunks))
                    chunks.clear()
                message_sender.send_packet(
                    DataPacket(id, self.store.get_seq(), "True", False, calculate_ascii_comb("True"), packet.seq))
            except CorruptedPacket as e:
                self.message_sender.send_packet(
                    DataPacket(id, self.store.get_seq(), "False", False, calculate_ascii_comb("False"), packet.seq))
                print(e)
            except DropPacket as e:
                print(e)
            except Exception as e:
                pass
