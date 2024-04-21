import os
import struct
import socket
import threading
def handle_client(client):
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
        file_name="Server"+file_name
        with open(file_name, "wb") as file:
            file.write(received_bytes)
        print(f"File '{file_name}' received successfully.")

    except Exception as e:
        print(f"An error occurred while handling the client: {e}")
    finally:
        client.close()


def receive_file_from_clients(server_address, server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_address, server_port))
    server.listen(5) 
    try:
        while True:
            client, addr = server.accept()
            print(f"Connection established with {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client,))
            client_thread.start()
    except Exception as e:
        print(f"An error occurred with the server: {e}")
    finally:
        server.close()

def send_file_to_server(server_address, server_port, file_name):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_address, server_port))

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

        print(f"Successfully sent '{file_name}' to {server_address}:{server_port}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()