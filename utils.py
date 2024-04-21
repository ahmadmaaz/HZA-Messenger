from exceptions import CorruptedPacket
def calculate_ascii_comb(data):
    ascii=0
    for i in range(0,len(data)-1):
        ascii+= abs(ord(data[i])-ord(data[i+1]))
    ascii+=sum(ord(c) for c in data)
    return ascii


def validate_packet(packet,seq = None):
    checkAscii = calculate_ascii_comb(packet.data)
    if (checkAscii != packet.checkAscii ) or (packet.data=="False" and packet.ackSeq!= None):
        raise CorruptedPacket("Corrupted Packet")
    if seq!=None and packet.ackSeq!=seq:
        raise Exception("Not expected seq, requesting again")
    if seq==None and packet.ackSeq!=None:
        raise Exception("Not expected ack")



    