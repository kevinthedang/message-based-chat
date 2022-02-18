import pika

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
        self.setup_channel()

    def connection_close(self):
        ''' This will be called when the connection to RabbitMQ is closed.
        '''
        self._channel.close()
        self._channel = None
        self._connection.close()
    
    def setup_channel(self):
        ''' This method will open a new channel with RabbitMQ.
        '''
        self._channel = self._connection.channel()

    def setup_exchange(self, queue_name):
        ''' Set up the exchange on RabbitMQ. The exchange name and type are held
            as parameters to help with declaring the exchange.
        '''
        self._channel.exchange_declare(
            exchange = RMQ_DEFAULT_EXCHANGE_NAME,
            exchange_type = RMQ_DEFAULT_EXCHANGE_TYPE,
            )
        self._channel.queue_declare(queue = queue_name)
        self._channel.queue_bind(exchange = RMQ_DEFAULT_EXCHANGE_NAME, queue = queue_name, routing_key = RMQ_ROUTING_KEY)
        self._channel.basic_qos(prefetch_count = 1)

    def publish_message(self, message) -> bool:
        ''' This method will attempt to publish a message to RabbitMQ.
            The method will inform of a successful publish or not through the terminal.
        '''
        self._channel.confirm_delivery()
        try: 
            self._channel.basic_publish(exchange = RMQ_DEFAULT_EXCHANGE_NAME, routing_key = RMQ_ROUTING_KEY, body = message, properties = pika.BasicProperties(delivery_mode = 2), mandatory = True)
            print(f' [x] "{message}" was sent to the MQ')
        except pika.exceptions.UnroutableError:
            print('Message was returned.')
            return False
        self.connection_close()
        return True
        
    def consume_message(self, destination_queue, max_messages):
        ''' This method will consume a message from RabbitMQ
        '''
        message_list = []
        try:
            ''' How do I get this returned?
                what is the format? there is an error with delivery but it comes with the correct message.
                How do I control the amount of messages? What is the correct parameter that deals with this?
            '''
            for method_frame, properties, body in self._channel.consume(queue = destination_queue, inactivity_timeout = 3, auto_ack = True):
                if not method_frame == None:
                    message_list.append(body)
                    if method_frame.delivery_tag == max_messages:
                        break

        except pika.exceptions.UnroutableError:
            print(f' [x] "{destination_queue}" queue not found / No messages in "{destination_queue}"')

        requeued_messages = self._channel.cancel()
        print("Requeued %i messages " % requeued_messages)
        self.connection_close()
        if len(message_list) == 0:
                message_list.append('No messages currently in queue.')
        return message_list


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

    def send_message(self, message_content: str, target_queue: str = RMQ_DEFAULT_PUBLIC_QUEUE) -> bool:
        ''' This will send a request to send a message to the exchange.
            The exchange will distribute it to the queue based on the target queue.
            it will only return a true if the message was sent correctly, false otherwise.
        '''
        self._server.setup_exchange(target_queue)
        return self._server.publish_message(message_content)

    def receieve_messages(self, num_messages: int = GET_ALL_MESSAGES, destination: str = RMQ_DEFAULT_PUBLIC_QUEUE) -> list:
        ''' Get a set of messages and return them in a list
            messages will be strings, so it will return a list of strings

            The following error is found when using the private queue:
            pika.exceptions.ChannelClosedByBroker: (404, "NOT_FOUND - no queue 'kevin' in vhost '/'")
        '''
        self._server.setup_exchange(destination)
        return self._server.consume_message(destination_queue = destination, max_messages = num_messages)