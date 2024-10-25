import socket
import os
import struct
from .store import Store

class FileSender:
    def __init__(self, store: Store):
        self.store = store

    def send_file(self, file_name, emitter):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", self.store.get_sender_port_file()))

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
            emitter.msg.emit("0" + "⁂" + file_name.split('/')[-1])

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()
