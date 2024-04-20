import socket
import pickle
import threading
from packet import DataPacket
from utils import calculate_ascii_comb
from connection_state import ConnectionState
connection_state = ConnectionState.CLOSED

# Create a UDP socket
sender_port = 0
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
id = 0
seq = 0

def sendPacket(dataPacket):
    while True:
        try:
            peer_socket.sendto(pickle.dumps(dataPacket), ('localhost', sender_port))
            peer_socket.settimeout(2)
            message, peer1_address = peer_socket.recvfrom(1000)
            peer_socket.settimeout(0)
            return message
        except socket.timeout:
            print("Timeout occurred. Retrying...")


def listenToPackets():
    chunks = set()
    while True:
        # Receive message from Peer 1
        try:
            message, peer1_address = peer_socket.recvfrom(1000)
            if peer1_address[1]!=sender_port:
                #Another client trying to connect
                pass
            packet = pickle.loads(message)
            checkAscii = calculate_ascii_comb(packet.data)
            if checkAscii != packet.checkAscii:
                peer_socket.sendto(b'False', ('localhost', sender_port))
                continue
            print(f"Received '{packet.data}', id '{packet.id}', seq '{packet.seq}' ")
            chunks.add((packet.data, packet.seq))
            if packet.finalChunk:
                sorted_chunks = sorted(chunks, key=lambda x: x[1])
                print(''.join(chunk[0] for chunk in sorted_chunks))
                chunks.clear()
            peer_socket.sendto(b'True', ('localhost', sender_port))
        except:
            continue

if __name__ == "__main__":
    running_socket = int(input("current port: "))
    peer_socket.bind(('localhost', running_socket))
    sender_port = int(input("target port: "))
    wantToInitiate= input("do you want to initiate connection (y or n): ")

    if wantToInitiate=="y":
        print("trying to connect")
        sendPacket(DataPacket(id, seq, "SYN", False, calculate_ascii_comb("SYN")))
        connection_state = ConnectionState.SYN_SENT
        peer_socket.sendto(pickle.dumps(DataPacket(id, seq, "SYN", False, calculate_ascii_comb("SYN"))), ('localhost', sender_port))
        connection_state = ConnectionState.ESTABLISHED
    else:
        message, peer1_address = peer_socket.recvfrom(1000)
        if peer1_address[1]!=sender_port:
            #Another client trying to connect
            pass
        sendPacket(DataPacket(id, seq, "SYNCACK", False, calculate_ascii_comb("SYNC-ACK")))
        connection_state = ConnectionState.ESTABLISHED

    print("connection established")
    receive_thread = threading.Thread(target=listenToPackets)
    receive_thread.start()
    while True:
        if(connection_state!=ConnectionState.ESTABLISHED):
            continue
        msg = input("What do you want to send: ")
        message_parts = [msg[i:i+6] for i in range(0, len(msg), 6)]
        for i in range(0, len(message_parts)):
            data = message_parts[i]
            print(calculate_ascii_comb(data))
            sendPacket(DataPacket(id, seq, data, i == len(message_parts) - 1, calculate_ascii_comb(data)))
            seq += len(data)
        id += 1
