from gc import callbacks
import pika
import logging
import functools

GET_ALL_MESSAGES = -1
RMQ_HOST = 'cps-devops.gonzaga.edu'
RMQ_PORT = 5672
RMQ_USER = 'class'
RMQ_PASS = 'CPSC313'
RMQ_DEFAULT_PUBLIC_QUEUE = 'general'
RMQ_DEFAULT_PRIVATE_QUEUE = 'kevin'
RMQ_TEST_HOST = 'localhost'
RMQ_DEFAULT_VH = '/'
RMQ_DEFAULT_EXCHANGE_NAME = 'general'
RMQ_DEFAULT_EXCHANGE_TYPE = 'fanout'
RMQ_ROUTING_KEY = 'my_message'
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
        self._consumer_tag = None

    def establish_connection(self) -> None:
        credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
        parameters = pika.ConnectionParameters(host=RMQ_HOST, port=RMQ_PORT, virtual_host=RMQ_DEFAULT_VH, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters=parameters)
        self.open_channel()

    def connection_close(self):
        ''' This will be called when the connection to RabbitMQ is closed.
        '''
        self._channel = None
        self._connection.close()
    
    def open_channel(self):
        ''' This method will open a new channel with RabbitMQ.
        '''
        self._channel = self._connection.channel()
        self.setup_exchange(RMQ_DEFAULT_EXCHANGE_NAME, RMQ_DEFAULT_EXCHANGE_TYPE)

    def setup_exchange(self, exchange_name, exchange_type):
        ''' Set up the exchange on RabbitMQ. The exchange name and type are held
            as parameters to help with declaring the exchange.
        '''
        self._channel.exchange_declare(
            exchange = exchange_name,
            exchange_type = exchange_type,
            )
        self._channel.queue_declare(queue = RMQ_DEFAULT_PUBLIC_QUEUE)
        self._channel.queue_bind(exchange = exchange_name, queue = RMQ_DEFAULT_PUBLIC_QUEUE, routing_key = RMQ_ROUTING_KEY)
        self._channel.basic_qos(prefetch_count = 1)

    def publish_message(self, message):
        ''' This method will attempt to publish a message to RabbitMQ.
            The method will inform of a successful publish or not through the terminal.
        '''
        self._channel.confirm_delivery()
        try: 
            self._channel.basic_publish(exchange = RMQ_DEFAULT_EXCHANGE_NAME, routing_key = RMQ_ROUTING_KEY, body = message, properties = pika.BasicProperties(delivery_mode = 2), mandatory = True)
            print(f' [x] {message} was sent to the MQ')
        except pika.exceptions.UnroutableError:
            print('Message was returned.')
        self.connection_close()
        
    def consume_callback(self, method, basic_deliver, properties, body):
        ''' This method helps us visualize the body of the message to the cmd.
            Once the body of the message is received, the connection is closed.
        '''
        print(" [x] Received %r" % body)
        self._channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def consume_message(self):
        ''' Consume a message from RabbitMQ
        '''
        self._channel.basic_consume(queue = RMQ_DEFAULT_PUBLIC_QUEUE, on_message_callback = self.consume_callback, auto_ack = True)
        print(' [*] Waiting for messages...')
        self._channel.start_consuming()
        self.connection_close()


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
        print('Connection Successful.')

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
        self._server.consume_message()
        pass

def main():
    logging.basicConfig(filename='mess_chat.log', level=logging.DEBUG, format=LOG_FORMAT, filemode='w')
    example = MessageServer()

if __name__ == '__main__':
    main()