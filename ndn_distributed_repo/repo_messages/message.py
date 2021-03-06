from ndn.encoding import *
from .add import AddMessageBody
from .remove import RemoveMessageBody
from .store import StoreMessageBody
from .claim import ClaimMessageBody
from .heartbeat import HeartbeatMessageBody
from .expire import ExpireMessageBody


class MessageTypes:
    ADD = 1
    REMOVE = 2
    STORE = 3
    CLAIM = 4
    HEARTBEAT = 5
    EXPIRE = 6

class MessageTlv(TlvModel):
    header = UintField(0x80)
    body = BytesField(0x81)

class Message:
    def __init__(self, nid:str, seq:int, raw_bytes:bytes):
        self.nid = nid
        self.seq = seq
        self.message = MessageTlv.parse(raw_bytes)

    def get_message_header(self):
        return self.message.header

    def get_message_body(self):
        message_type = self.message.header
        raw_bytes = self.message.body.tobytes()
        if message_type == MessageTypes.ADD:
            return AddMessageBody(self.nid, self.seq, raw_bytes)
        elif message_type == MessageTypes.REMOVE:
            return RemoveMessageBody(self.nid, self.seq, raw_bytes)
        elif message_type == MessageTypes.STORE:
            return StoreMessageBody(self.nid, self.seq, raw_bytes)
        elif message_type == MessageTypes.CLAIM:
            return ClaimMessageBody(self.nid, self.seq, raw_bytes)
        elif message_type == MessageTypes.HEARTBEAT:
            return HeartbeatMessageBody(self.nid, self.seq, raw_bytes)
        elif message_type == MessageTypes.EXPIRE:
            return ExpireMessageBody(self.nid, self.seq, raw_bytes)
        else:
            return None


