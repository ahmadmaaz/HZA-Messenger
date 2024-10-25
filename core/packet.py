class DataPacket:

    def __init__(self, id, seq, data, final_chunk: bool, check_ascii, ack_seq=None):
        self.id = id
        self.seq = seq
        self.data = data
        self.final_chunk = final_chunk
        self.check_ascii = check_ascii
        self.ack_seq = ack_seq
