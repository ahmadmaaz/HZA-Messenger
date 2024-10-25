from .exceptions import CorruptedPacket, DropPacket


def calculate_ascii_comb(data):
    ascii = 0
    for i in range(0, len(data) - 1):
        ascii += abs(ord(data[i]) - ord(data[i + 1]))
    ascii += sum(ord(c) for c in data)
    return ascii


def validate_packet(packet, seq=None, clientSeq=-1):
    check_ascii = calculate_ascii_comb(packet.data)
    if (check_ascii != packet.checkAscii) or (packet.data == "False" and packet.ackSeq is not None):
        raise CorruptedPacket("Corrupted Packet")
    if seq == None and packet.ackSeq is not None:
        raise DropPacket("Not expected ack")
