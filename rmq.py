import pika
import logging

GET_ALL_MESSAGES = -1
RMQ_HOST = 'cps-devops.gonzaga.edu'
RMQ_PORT = 5672
RMQ_USER = 'class'
RMQ_PASS = 'CPSC313'
RMQ_DEFAULT_PUBLIC_QUEUE = 'general'
RMQ_DEFAULT_PRIVATE_QUEUE = ''
RMQ_TEST_HOST = 'localhost'
RMQ_DEFAULT_VH = '/'
RMQ_DEFAULT_EXCHANGE_NAME = ''
RMQ_DEFAULT_EXCHANGE_TYPE = 'fanout'
LOG_FORMAT = '%(asctime)s -- %(levelname)s -- %(message)s'
LOGGER = logging.getLogger(__name__)

class RMQPublisher():
    ''' This is the RMQ Publisher/
    '''
    def __init__(self) -> None:
        ''' Establishing Variables needed to perform connection to RMQ
        '''
        self._connection = None
        self._channel = None

    def establish_connection(self) -> None:
        credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
        parameters = pika.ConnectionParameters(host=RMQ_HOST, port=RMQ_PORT, virtual_host=RMQ_DEFAULT_VH, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters=parameters)
        self.connection_open()

    def connection_open(self):
        ''' This will be called once pika is connected to RabbitMQ.
            This will call for a channel to open.
        '''
        self.open_channel()

    def connection_close(self):
        ''' This will be called when the connection to RabbitMQ is closed.
        '''
        self._channel = None
        self._connection.close()
    
    def open_channel(self):
        ''' This method will open a new channel with RabbitMQ.
        '''
        self._connection.channel()
        self._channel = self._connection.channel()
        # self.setup_exchange(RMQ_DEFAULT_EXCHANGE_NAME)

    def setup_exchange(self, exchange_name):
        ''' Set up the exchange on RabbitMQ
        '''
        self._channel.exchange_declare(
            exchange = exchange_name,
            exchange_type = RMQ_DEFAULT_EXCHANGE_TYPE)

    def setup_queue(self):
        ''' Setup the queue on RabbitMQ
        '''
        self._channel.queue_declare(queue = RMQ_DEFAULT_PUBLIC_QUEUE)

    def publish_message(self, message):
        ''' Publish a message to RabbitMQ.
        '''
        self._channel.basic_publish(exchange = '', routing_key = 'message', body = message)
        print(f' [x] {message} was sent to the MQ')
        self.connection_close()
        

    def consume_callback(self, method, properties, body):
        print(" [x] Received %r" % body)

    def consume_message(self):
        '''
        '''
        self._channel.basic_consume(queue = RMQ_DEFAULT_PUBLIC_QUEUE, on_message_callback = self.consume_callback, auto_ack = True)
        print(' [*] Waiting for messages...')
        self._channel.start_consuming()


class MessageServer():
    ''' This will help with the execution of the connection to RabbitMQ. 
        This will also be sending an I/O signal to the class to send or receive messages.
    '''
    def __init__(self) -> None:
        ''' Set up all the RMQ settings within RMQConnection
            Create and set up connection, channels, queues, exchanges, etc.
        '''
        self._server = RMQPublisher()
        self._connection = self._server.establish_connection()
        self._server.setup_queue()
        print('Connection Successful.')
        # self.__public_exchange = pika.create_exchange()

    def send_message(self, message_content: str) -> bool:
        ''', target_queue: str'''
        ''' This will send a request to send a message to the exchange.
            The exchange will distribute it to all the queues.
        '''
        self._server.publish_message(message_content)
        pass

    def receieve_messages(self, num_messages: int = GET_ALL_MESSAGES) -> list:
        '''destination: str,'''
        ''' Get a set of messages and return them in a list
            messages will be strings, so it will return a list of strings
        '''
        self._connection = self._server.establish_connection()
        self._server.setup_queue()
        self._server.consume_message()
        pass

def main():
    logging.basicConfig(filename='mess_chat.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')
    example = MessageServer()

if __name__ == '__main__':
    main()