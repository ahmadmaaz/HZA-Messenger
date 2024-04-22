import socket
import pickle
import threading
import os
import struct
from packet import DataPacket
from utils import calculate_ascii_comb, validate_packet
from connection_state import ConnectionState
from exceptions import CorruptedPacket,DropPacket
import base64

connection_state = ConnectionState.CLOSED
sender_port = 0
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
current_port_file=0
sender_port_file=0
id= 0
seq = 0  # Initialize seq
clientSeq=-1
def send_packet_with_timeout(dataPacket):
    while True:
        try:
            peer_socket.sendto(pickle.dumps(dataPacket), ('localhost', sender_port))
            peer_socket.settimeout(.2)
            message, peer1_address = peer_socket.recvfrom(1000)
            packet = pickle.loads(message)
            validate_packet(packet,seq,clientSeq=clientSeq)
            peer_socket.settimeout(0)
            return packet
        except socket.timeout:
            print("Timeout occurred. Retrying...")
        except CorruptedPacket as e:
            print(e)
        except Exception as e:
            print(e)
            pass
def send_packet(dataPacket):
    peer_socket.sendto(pickle.dumps(dataPacket), ('localhost', sender_port))
def listen_to_packets(emitter):
    global clientSeq
    chunks = set()
    while True:
        try:
            message, peer1_address = peer_socket.recvfrom(1000)
            if peer1_address[1] != sender_port:
                raise Exception("Received packet from different port")
            packet = pickle.loads(message)
            if packet.data in ["SYNACK","SYN"] and packet.seq==0:  # a peer is still stuck in handshake
                msgToSend= "ACK" if packet.data=="SYNACK" else "SYNACK"
                send_packet(pickle.dumps(DataPacket(id, seq, msgToSend, False, calculate_ascii_comb(msgToSend),0)))
                continue
            if clientSeq >=packet.seq:
                send_packet(DataPacket(id, seq, "True", False, calculate_ascii_comb("True"),packet.seq))
                continue
            validate_packet(packet,seq=None,clientSeq=clientSeq)
            chunks.add((packet.data, packet.seq))
            clientSeq=packet.seq
            print(packet.data)
            if packet.finalChunk:
                sorted_chunks = sorted(chunks, key=lambda x: x[1])
                emitter.msg.emit("1" + ''.join(chunk[0] for chunk in sorted_chunks))
                chunks.clear()
            send_packet(DataPacket(id, seq, "True", False, calculate_ascii_comb("True"),packet.seq))
        except CorruptedPacket as e:
            send_packet(DataPacket(id, seq, "False", False, calculate_ascii_comb("False"),packet.seq))
            print(e)
        except DropPacket as e:
            print(e)
        except Exception as e:
            pass
def send_button(msg,emitter, callback=None):
    global id 
    global seq
    print(msg)
    message_parts = [msg[i:i + 6] for i in range(0, len(msg), 6)]
    for i in range(0, len(message_parts)):
        data = message_parts[i]
        send_packet_with_timeout(DataPacket(id, seq, data, i == len(message_parts) - 1, calculate_ascii_comb(data)))
        seq += len(data)
    emitter.msg.emit("0" + msg)
    id += 1
    if callback:
        callback()

def handle_client(client,emitter):
    try:
        file_name_length_data = client.recv(4)
        file_name_length = struct.unpack('!I', file_name_length_data)[0]
        file_name = client.recv(file_name_length).decode('utf-8')

        file_size_data = client.recv(8)
        file_size = struct.unpack('!Q', file_size_data)[0]
        received_bytes = b""
        total_received = 0

        while total_received < file_size:
            chunk = client.recv(4096)  # Receive in chunks
            if not chunk:
                break  # Connection closed unexpectedly
            if b"<END>" in chunk:
                chunk = chunk.split(b"<END>")[0]
                received_bytes += chunk
                break  # Break once the marker is encountered
            total_received += len(chunk)
            received_bytes += chunk
        encoded_data = base64.b64encode(received_bytes).decode('utf-8')
        emitter.msg.emit("1" + "⁂"+file_name.split('/')[-1]+"⁂"+encoded_data)
        print(f"File '{file_name.split('/')[-1]}' received successfully.")

    except Exception as e:
        print(f"An error occurred while handling the client: {e}")
    finally:
        client.close()


def listen_to_files(emitter):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", current_port_file))
    server.listen(5) 
    try:
        while True:
            client, addr = server.accept()
            print(f"Connection established with {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client,emitter))
            client_thread.start()
    except Exception as e:
        print(f"An error occurred with the server: {e}")
    finally:
        server.close()

def send_file_to_server(file_name,emitter):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", sender_port_file))

        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"File '{file_name}' not found.")

        file_size = os.path.getsize(file_name)

        file_name_bytes = file_name.encode('utf-8')
        client.send(struct.pack('!I', len(file_name_bytes)))  # Send the length of the file name
        client.send(file_name_bytes)  # Send the file name
        client.send(struct.pack('!Q', file_size))  # Send the file size (Q for unsigned long long)

        with open(file_name, "rb") as file:
            while True:
                data = file.read(4096)  
                if not data:
                    break
                client.sendall(data)
        client.send(b"<END>")
        emitter.msg.emit("0" + "⁂"+file_name.split('/')[-1])

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
def run(emitter,cs, sp,cpf,spf):
    global current_socket,sender_port , id, seq,current_port_file,sender_port_file
    peer_socket.bind(('localhost', cs))
    current_socket=cs
    sender_port=sp
    current_port_file=cpf
    sender_port_file=spf
    print( cs, sp , cpf,spf)
    want_to_initiate = input("do you want to initiate connection (y or n): ")
    if want_to_initiate == "y":
        print("trying to connect")
        send_packet_with_timeout(DataPacket(id, seq, "SYN", False, calculate_ascii_comb("SYN")))
        connection_state = ConnectionState.SYN_SENT
        id+=1
        seq+= len("SYN")
        send_packet(DataPacket(id, seq, "ACK", False, calculate_ascii_comb("ACK"),0))
        id+=1
        seq+= len("ACK")
        connection_state = ConnectionState.ESTABLISHED
    else:
        message, peer1_address = peer_socket.recvfrom(1000)
        send_packet_with_timeout(DataPacket(id, seq, "SYNACK", False, calculate_ascii_comb("SYNACK"),0))
        id+=1
        seq+= len("SYNACK")
        connection_state = ConnectionState.ESTABLISHED

    print("connection established")
    receive_thread = threading.Thread(target=listen_to_packets,args=(emitter,))
    receive_thread.start()
    receive_thread = threading.Thread(target=listen_to_files,args=(emitter,))
    receive_thread.start() 


    
    
