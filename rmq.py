import pika

GET_ALL_MESSAGES = -1
RMQ_HOST = 'cps-devops.gonzaga'
RMQ_PORT = 5672
RMQ_USER = 'class'
RMQ_PASS = 'CPSC313'
RMQ_DEFAULT_PUBLIC_QUEUE = 'general'
RMQ_DEFAULT_PRIVATE_QUEUE = ''

connection =  pika.BlockingConnection(pika.ConnectionParameters('http://cps-devops.gonzaga.edu:5672'))
channel = connection.channel()

def on_connected(connection):
    connection.channel(on_open_callback=on_channel_open)

# when the channel is open, this is called
def on_channel_open(new_channel):
    global channel
    channel = new_channel
    channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

def on_queue_declared(frame):
    channel.basic_consume('test', handle_delivery)

def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    print(body)

# Step #1: Connect to RabbitMQ using the default parameters
parameters = pika.ConnectionParameters()
connection = pika.SelectConnection(parameters, on_open_callback=on_connected)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()

class MessageServer():
    '''
    '''
    def __init__(self) -> None:
        ''' Set up all the RMQ settings
            Create and set up connection, channels, queues, exchanges, etc.
        '''
        self.__connection = pika.create_connection()
        # self.__public_exchange = pika.create_exchange()

    def send_message(self, message: str, target_queue: str) -> bool:
        ''' 
        '''
        pass

    def receieve_messages(self, destination: str, num_messages: int = GET_ALL_MESSAGES) -> list:
        ''' Get a set of messages and return them in a list
            messages will be strings, so it will return a list of strings
        '''
        pass