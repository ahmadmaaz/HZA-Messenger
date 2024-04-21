from exceptions import CorruptedPacket,DropPacket
def calculate_ascii_comb(data):
    ascii=0
    for i in range(0,len(data)-1):
        ascii+= abs(ord(data[i])-ord(data[i+1]))
    ascii+=sum(ord(c) for c in data)
    return ascii


def validate_packet(packet,seq = None,clientSeq = -1):
    checkAscii = calculate_ascii_comb(packet.data)
    if (checkAscii != packet.checkAscii ) or (packet.data=="False" and packet.ackSeq!= None):
        raise CorruptedPacket("Corrupted Packet")
    if seq==None and packet.ackSeq!=None:
        raise DropPacket("Not expected ack")





    