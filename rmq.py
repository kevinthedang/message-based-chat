import pika

GET_ALL_MESSAGES = -1
RMQ_HOST = 'cps-devops.gonzaga.edu'
RMQ_PORT = 5672
RMQ_USER = 'class'
RMQ_PASS = 'CPSC313'
RMQ_DEFAULT_PUBLIC_QUEUE = 'general'
RMQ_DEFAULT_PRIVATE_QUEUE = ''
RMQ_TEST_HOST = 'localhost'
RMQ_DEFAULT_VH = '/'

credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
parameters = pika.ConnectionParameters(host=RMQ_HOST, port=RMQ_PORT, virtual_host=RMQ_DEFAULT_VH, credentials=credentials)
connection =  pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

channel.queue_declare(queue=RMQ_DEFAULT_PUBLIC_QUEUE)
channel.basic_publish(exchange='', routing_key='general', body='hello kevin')
print(" [x] Sent 'hello kevin'")

connection.close()

class RMQConnection():
    '''
    '''
    def __init__(self) -> None:
        pass

class MessageServer():
    '''
    '''
    def __init__(self) -> None:
        ''' Set up all the RMQ settings
            Create and set up connection, channels, queues, exchanges, etc.
        '''
        # self.__connection = pika.create_connection()
        # self.__public_exchange = pika.create_exchange()
        pass

    def send_message(self, message: str, target_queue: str) -> bool:
        ''' 
        '''
        pass

    def receieve_messages(self, destination: str, num_messages: int = GET_ALL_MESSAGES) -> list:
        ''' Get a set of messages and return them in a list
            messages will be strings, so it will return a list of strings
        '''
        pass