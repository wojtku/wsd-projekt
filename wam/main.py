import uuid
import time, pika, json, sys
from howler2 import Howler




wolf_id = 'wolf2' #str(uuid.uuid4())

class WolfMockup():

    def __init__(self, wolfname):
        self.id = wolfname
        self.howler = Howler(wolfname, handle_message=self.handle_message)
        self.howler.connect()
        self.howler.start_consuming()

        # memory
        self.Alpha = None
        self.Beta = None
        self.Gamma = None
        self.Delta = None
        self.position = (12, 32)
        self.confidence_level = 0.1

    # this method handles the messages passed via callback from howler
    def handle_message(self, body):
        print(body)
        body = json.loads(body.decode("utf-8"))
        try:
            if 'type' in body.keys():
                # sample of how to handle a message
                if body['type'] == 'query-ref' and body['protocol'] == 'IP3':
                    # this is unnecessary, but could make the system more flexible
                    response_dict = {}
                    for attr in body['content']['get']:
                        response_dict[attr] = getattr(self, attr)
                    sender = body['sender']
                    self.howler.send_position(sender, self.position, self.confidence_level)
        except:
            for err in sys.exc_info():
                print(err)


howler = WolfMockup(wolf_id)


print('udpa')
