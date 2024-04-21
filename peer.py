import socket
import pickle
import threading
from packet import DataPacket
from utils import calculate_ascii_comb, validate_packet
from connection_state import ConnectionState
from exceptions import CorruptedPacket

connection_state = ConnectionState.CLOSED

sender_port = 0
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
id = 0
seq = 0  # Initialize seq

def send_packet_with_timeout(dataPacket, seq=None):
    while True:
        try:
            peer_socket.sendto(pickle.dumps(dataPacket), ('localhost', sender_port))
            peer_socket.settimeout(1.75)
            message, peer1_address = peer_socket.recvfrom(1000)
            packet = pickle.loads(message)
            validate_packet(packet, seq)
            peer_socket.settimeout(0)
            return message
        except socket.timeout:
            print("Timeout occurred. Retrying...")
        except CorruptedPacket as e:
            print(e)
        except Exception as e:
            pass

def send_packet(dataPacket):
    peer_socket.sendto(pickle.dumps(dataPacket), ('localhost', sender_port))

def listen_to_packets():
    chunks = set()
    while True:
        try:
            message, peer1_address = peer_socket.recvfrom(1000)
            if peer1_address[1] != sender_port:
                raise Exception("Received packet from different port")
            packet = pickle.loads(message)
            validate_packet(packet)
            print(f"Received '{packet.data}', id '{packet.id}', seq '{packet.seq}' ")
            chunks.add((packet.data, packet.seq))
            if packet.finalChunk:
                sorted_chunks = sorted(chunks, key=lambda x: x[1])
                print(''.join(chunk[0] for chunk in sorted_chunks))
                chunks.clear()
            send_packet(DataPacket(id, seq, "True", False, calculate_ascii_comb("True"), packet.seq))
        except CorruptedPacket as e:
            send_packet(DataPacket(id, seq, "False", False, calculate_ascii_comb("False"), packet.seq))
            print(e)
        except Exception as e:
            pass

if __name__ == "__main__":
    running_socket = int(input("current port: "))
    peer_socket.bind(('localhost', running_socket))
    sender_port = int(input("target port: "))
    want_to_initiate = input("do you want to initiate connection (y or n): ")

    if want_to_initiate == "y":
        print("trying to connect")
        send_packet_with_timeout(DataPacket(id, seq, "SYN", False, calculate_ascii_comb("SYN"),0), seq)

        connection_state = ConnectionState.SYN_SENT
        send_packet(pickle.dumps(DataPacket(id, seq, "ACK", False, calculate_ascii_comb("ACK"),0), seq))

        connection_state = ConnectionState.ESTABLISHED
    else:
        message, peer1_address = peer_socket.recvfrom(1000)
        send_packet_with_timeout(DataPacket(id, seq, "SYNACK", False, calculate_ascii_comb("SYNACK"),0), seq)
        connection_state = ConnectionState.ESTABLISHED

    print("connection established")
    receive_thread = threading.Thread(target=listen_to_packets)
    receive_thread.start()
    while True:
        if connection_state != ConnectionState.ESTABLISHED:
            continue
        msg = input("What do you want to send: ")
        message_parts = [msg[i:i + 6] for i in range(0, len(msg), 6)]
        for i in range(0, len(message_parts)):
            data = message_parts[i]
            print(calculate_ascii_comb(data))
            send_packet_with_timeout(DataPacket(id, seq, data, i == len(message_parts) - 1, calculate_ascii_comb(data)), seq)
            seq += len(data)
        id += 1
