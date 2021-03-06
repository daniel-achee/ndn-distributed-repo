from ndn.encoding import *
from .message_base import MessageBodyBase
import json

class HeartbeatMessageBodyTypes:
    SESSION_ID = 83
    NODE_NAME = 84
    EXPIRE_AT = 85
    FAVOR = 86

class HeartbeatMessageBodyTlv(TlvModel):
    session_id = BytesField(HeartbeatMessageBodyTypes.SESSION_ID)
    node_name = BytesField(HeartbeatMessageBodyTypes.NODE_NAME)
    expire_at = UintField(HeartbeatMessageBodyTypes.EXPIRE_AT)
    favor = BytesField(HeartbeatMessageBodyTypes.FAVOR)

class HeartbeatMessageBody(MessageBodyBase):
    def __init__(self, nid:str, seq:int, raw_bytes:bytes):
        super(HeartbeatMessageBody, self).__init__(nid, seq)
        self.message_body = HeartbeatMessageBodyTlv.parse(raw_bytes)

    async def apply(self, global_view, svs, config):
        session_id = self.message_body.session_id.tobytes().decode()
        node_name = self.message_body.node_name.tobytes().decode()
        expire_at = self.message_body.expire_at
        favor = float(self.message_body.favor.tobytes().decode())
        val = "[MSG][HB] sid={sid};name={nam};exp={exp};fav={fav}".format(
            sid=session_id,
            nam=node_name,
            exp=expire_at,
            fav=favor
        )
        # print(val)
        global_view.update_session(session_id, node_name, expire_at, favor, self.seq)
        sessions = global_view.get_sessions()
        # print(json.dumps(sessions))
        return
