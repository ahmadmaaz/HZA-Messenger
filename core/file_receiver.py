import struct
import base64
import socket
from .store import Store
import threading


class FileReceiver:

    def __init__(self, store: Store, message_emitter):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", store.get_current_port_file()))
        self.thread = threading.Thread(target=self.listen_to_files, args=(message_emitter,))
        self.thread.start()

    def _listen_to_file(self, client, emitter):
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
            emitter.msg.emit("1" + "⁂" + file_name.split('/')[-1] + "⁂" + encoded_data)
            print(f"File '{file_name.split('/')[-1]}' received successfully.")

        except Exception as e:
            print(f"An error occurred while handling the client: {e}")
        finally:
            self.socket.close()

    def listen_to_files(self, emitter):
        self.socket.listen(1)
        try:
            while True:
                client, addr = self.socket.accept()
                print(f"Connection established with {addr}")
                client_thread = threading.Thread(target=self._listen_to_file, args=(client, emitter))
                client_thread.start()
        except Exception as e:
            print(f"An error occurred with the server: {e}")
        finally:
            self.socket.close()
