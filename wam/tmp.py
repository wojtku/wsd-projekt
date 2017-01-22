import uuid
import time, pika
from howler2 import Howler


wolf_id = 'wolf3' #str(uuid.uuid4())
howler = Howler(wolf_id, handle_message=None)
howler.connect()

msg_dict = {
    'type': 'propose',
    'sender': wolf_id,
    'content': 'yo yo yo'}

howler.get_position('wolf2')



print('udpa')
