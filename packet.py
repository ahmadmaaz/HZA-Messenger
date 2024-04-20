class DataPacket:
    def __init__(self,id,seq,data,finalChunk,checkAscii):
        self.id=id
        self.seq=seq
        self.data=data
        self.finalChunk=finalChunk
        self.checkAscii=checkAscii