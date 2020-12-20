import struct
import sys

class pkt:
    def __init__(self):
        self.struct = 'i32s256s512s32s512s'
        self.req = 0
        self.userID = b'' # 32 bytes max
        self.msg = b''  # set to 256
        self.idList = b'' # set to 512
        self.externalIP = b'' # 32
        self.ipTable = b'' # 512

    def setPacketInfo(self, req, userID, msg, idList, externalIP, ipTable):
        self.req = req
        self.userID = userID
        self.msg = msg
        self.idList = idList
        self.externalIP = externalIP
        self.ipTable = ipTable

        send = struct.pack(self.struct, req, userID, msg, idList, externalIP, ipTable)

        return send

    def readPacket(self, read):
        self.req, self.userID, self.msg, self.idList, self.externalIP, self.ipTable = struct.unpack(self.struct, read)
