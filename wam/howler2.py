import pika, sys

import uuid, time, json
import threading


# this thread handles recieving messages from the broker
class WolfEarsThread (threading.Thread):
    def __init__(self, channel):
        threading.Thread.__init__(self)
        self.channel = channel
    def run(self):
        try:
            self.channel.start_consuming()
        except:
            for err in sys.exc_info():
                print(err)


# this class handles communication with other wolf instances
class Howler:
    def __init__(self, queue_name, handle_message,  username='wolf', password='auuuuu', host='localhost', port=5672, virtual_host='pack'):
        self.connection = None
        self.channel = None
        # queue name is agent id
        self.queue = None
        self.queue_name = queue_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.broadcast_exchange = 'broadcast'

        self.handle_message = handle_message

    # opens a connection to the broker, setups queues and bind to exchanges
    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.virtual_host, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        # bind to broadcast exchange
        self.channel.exchange_declare(exchange='broadcast', type='fanout')
        self.channel.queue_declare(self.queue_name)
        self.channel.queue_bind(exchange='broadcast', queue=self.queue_name)
        # bind to my individual exchange
        self.channel.exchange_declare(exchange=self.queue_name, type='direct')
        self.channel.queue_bind(exchange=self.queue_name, queue=self.queue_name)
        # self.channel.queue_declare(queue=self.queue_name, durable=True)

    # passed as callback to the message listenign thread. handles incoming messages
    def consume_messages(self, ch, method, properties, body):
        self.handle_message(body)
        print('consuming')

    # starts the listening thread
    def start_consuming(self):
        print('omnomnomnom')
        self.channel.basic_consume(self.consume_messages, queue=self.queue_name, no_ack=True)
        WolfEarsThread(self.channel).start()
        print('ave maria')

    # sends a message to the 'broadcast' exchange, that every wolf subscribes to
    def broadcast_message(self, message_body):
        message = json.dumps(message_body)
        self.channel.basic_publish(exchange=self.broadcast_exchange, body=message)

    # sends a message to the selected exchange, route
    def send_message(self, exchange, route, message_body):
        message = json.dumps(message_body)
        self.channel.basic_publish(exchange=exchange, routing_key=route, body=message)

    # propose: Alfa proponuje wybranemu agentowi objęcia nowej roli (Alfa, Beta, Delta)
    def propose_new_role(self, target, role):
        msg = {
            'type': 'propose',
            'sender': self.queue_name,
            'receiver': target,
            'content': {'new_role': role},
            'language': 'JSON',
            'protocol': 'IP2',
            'conversation-id': '', #TODO implement
            'reply_with': '', #TODO implement
        }
        self.send_message(target, target, json.dumps(msg))

    # reject-proposal: Agent odrzuca propozycję.
    # Komunikat kończy konwersację agentów i tym samym protokół interakcji IP2.
    # Niepotrzebne pola zostały usunięte ze struktury wiadomości
    def reject_proposal(self, target):
        msg = {
            'type': 'reject-proposal',
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP2',
            'conversation-id': '', #TODO implement

        }
        self.send_message(target, target, msg)

    #accept-proposal: Komunikat ten sygnalizuje akceptację propozycji objęcia nowej roli
    # i tak samo jak poprzedni komunikat kończy protokół interakcji.
    def accept_proposal(self, target):
        msg = {
            'type': 'accept-proposal',
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP2',
            'conversation-id': '', #TODO implement
        }
        self.send_message(target, target, msg)

    # nie zaimplementowane - bez sensu. informacja o nowym szefie przychodzi broadcastem
    def subscribe(self, target):
        pass

    # refuse: następuje kiedy odbiorcą wiadomości nie jest agentem o roli Alfa
    def refuse(self, target):
        msg = {
            'type': 'refuse',
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP3',
            'conversation-id': '', #TODO implement
        }
        self.send_message(target, target, msg)

    # accept: następuje kiedy odbiorcą wiadomości nie jest agentem o roli Alfa
    def accept(self, target):
        msg = {
            'type': 'accept',
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP3',
            'conversation-id': '', #TODO implement
        }
        self.send_message(target, target, msg)

    # inform-result: komunikat jest wysyłany kiedy dochodzi do zmiany lidera grupy
    def new_leader(self, target):
        msg = {
            'type': 'inform-result',
            'content': {'new_leader': self.queue_name},
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP3',
            'conversation-id': '', #TODO implement
            'language': 'json',
            'ontology': 'wolfpack'
        }
        self.broadcast_message(msg)

    # query-ref: pytanie odbiorcy o położenie i poziom zaufania
    def get_position(self, target):
        msg = {
            'type': 'query-ref',
            'content': {'get': ['position','confidence_level']}, #dict cant have two same keys, so no get: position, get:confidence_level
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP3',
            'language': 'json',
            'ontology': 'wolfpack',
            'conversation-id': '',  # TODO implement
            'reply-with': ''
        }
        self.send_message(target, target, msg)

    # inform-ref: odpowiedź na pytanie o położenie i poziom zaufania
    def send_position(self, target, position, confidence_level):
        msg = {
            'type': 'inform-ref',
            'content': {'position': position,'confidence_level': confidence_level},
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP4',
            'language': 'json',
            'ontology': 'wolfpack',
            'conversation-id': '',  # TODO implement
            'reply-with': ''
        }
        self.send_message(target, target, msg)

    def refuse_send_position(self, target, reason):
        msg = {
            'type': 'refuse',
            'content': {'reason': reason},
            'sender': self.queue_name,
            'receiver': target,
            'protocol': 'IP4',
            'language': 'json',
            'ontology': 'wolfpack',
            'conversation-id': '',  # TODO implement
        }
        self.send_message(target, target, msg)

