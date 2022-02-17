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

class RMQPublisher():
    ''' This is the RMQ Publisher
        - Only one connection needs to be made.
        - There should be two channels, followed by two queues.s
        - There should be one exchange, the queues will bind to the exchange.
    '''
    def __init__(self) -> None:
        ''' Establishing Variables needed to perform connection to RMQ
            The class just needs to hand a connection and a channel

            It might be that there needs to be two connections:
                - one for the private channel
                - one for the public channel

            consider a -> self._public_channel
                       -> self._private_channel
        '''
        self._connection = None
        self._channel = None

    def establish_connection(self) -> None:
        ''' This method will establish the connection to the RabbitMQ server.
            Proper authentication credentials and parameters are needed to access the server.
        '''
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
            Consider using parameters since we are going to be using more than 1 channel.
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

    def publish_message(self, message) -> bool:
        ''' This method will attempt to publish a message to RabbitMQ.
            The method will inform of a successful publish or not through the terminal.
        '''
        self._channel.confirm_delivery()
        try: 
            self._channel.basic_publish(exchange = RMQ_DEFAULT_EXCHANGE_NAME, routing_key = RMQ_ROUTING_KEY, body = message, properties = pika.BasicProperties(delivery_mode = 1), mandatory = True)
            print(f' [x] "{message}" was sent to the MQ')
        except pika.exceptions.UnroutableError:
            print('Message was returned.')
            return False
        self.connection_close()
        return True
        
    def consume_callback(self, method, basic_deliver, properties, body):
        ''' This method helps us visualize the body of the message to the cmd.
            Once the body of the message is received, the connection is closed.
        '''
        print(" [x] Received %r" % body)
        self._channel.basic_ack(delivery_tag = basic_deliver.delivery_tag)

    def consume_message(self, destination_queue):
        ''' This method will consume a message from RabbitMQ
        '''
        try:
            ''' How do I get this returned?
                what is the format? there is an error with delivery but it comes with the correct message.
                How do I control the amount of messages? What is the correct parameter that deals with this?
            '''
            self._channel.basic_consume(queue = destination_queue, on_message_callback = self.consume_callback, auto_ack = True)
            print(' [*] Waiting for messages...')
            self._channel.start_consuming()
        except pika.exceptions.UnroutableError:
            print(f' [x] "{destination_queue}" queue not found / No messages in "{destination_queue}"')
            return []
        self.connection_close()


class MessageServer():
    ''' This will help with the execution of the connection to RabbitMQ. 
        This will also be sending an I/O signal to the class to send or receive messages.
        Upon sending a request, the client will disconnect from the RabbitMQ server.
    '''
    def __init__(self) -> None:
        ''' Set up all the RMQ settings within RMQConnection
            Create and set up connection, channels, queues, exchanges, etc.
        '''
        self._server = RMQPublisher()
        self._connection = self._server.establish_connection()
        print('Connection Successful.')

    def send_message(self, message_content: str, target_queue: str = RMQ_DEFAULT_PUBLIC_QUEUE) -> bool:
        ''' This will send a request to send a message to the exchange.
            The exchange will distribute it to the queue based on the target queue.
            it will only return a true if the message was sent correctly, false otherwise.
        '''
        return self._server.publish_message(message_content)

    def receieve_messages(self, num_messages: int = GET_ALL_MESSAGES, destination: str = RMQ_DEFAULT_PUBLIC_QUEUE) -> list:
        ''' Get a set of messages and return them in a list
            messages will be strings, so it will return a list of strings

            The following error is found when using the private queue:
            pika.exceptions.ChannelClosedByBroker: (404, "NOT_FOUND - no queue 'kevin' in vhost '/'")
        '''
        self._server.consume_message(destination_queue = destination)
        pass