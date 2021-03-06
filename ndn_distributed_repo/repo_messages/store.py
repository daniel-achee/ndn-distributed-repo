from ndn.encoding import *
from .message_base import MessageBodyBase

class StoreMessageBodyTypes:
    SESSION_ID = 83
    NODE_NAME = 84
    EXPIRE_AT = 85
    FAVOR = 86

    INSERTION_ID = 90

class StoreMessageBodyTlv(TlvModel):
    session_id = BytesField(StoreMessageBodyTypes.SESSION_ID)
    node_name = BytesField(StoreMessageBodyTypes.NODE_NAME)
    expire_at = UintField(StoreMessageBodyTypes.EXPIRE_AT)
    favor = BytesField(StoreMessageBodyTypes.FAVOR)
    insertion_id = BytesField(StoreMessageBodyTypes.INSERTION_ID)

class StoreMessageBody(MessageBodyBase):
    def __init__(self, nid:str, seq:int, raw_bytes:bytes):
        super(StoreMessageBody, self).__init__(nid, seq)
        self.message_body = StoreMessageBodyTlv.parse(raw_bytes)

    async def apply(self, global_view, svs, config):
        session_id = self.message_body.session_id.tobytes().decode()
        node_name = self.message_body.node_name.tobytes().decode()
        expire_at = self.message_body.expire_at
        favor = float(self.message_body.favor.tobytes().decode())
        insertion_id = self.message_body.insertion_id.tobytes().decode()
        val = "[MSG][STORE]   sid={sid};iid={iid}".format(
            sid=session_id,
            iid=insertion_id
        )
        print(val)
        # if insertion 
        insertion = global_view.get_insertion(insertion_id)
        if (insertion == None) or (insertion['is_deleted'] == True):
            # TODO: add store to pending 
            print('add to pending store')
        else:
            global_view.store_file(insertion_id, session_id)
        # update session
        global_view.update_session(session_id, node_name, expire_at, favor, self.seq)
        return
