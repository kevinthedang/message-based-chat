import unittest
from rmq import RMQ_DEFAULT_PUBLIC_QUEUE, MessageServer

TEST_NO_PUBLISHES = ['No messages currently in queue.']
TEST_0_PUBLISHES = ['']
TEST_1_PUBLISHES = ['Hello World!']
TEST_2_PUBLISHES = ['I am here!', 'I am here too!']
TEST_3_PUBLISHES = ['I am here!', 'I am here too!', 'Am I here too?']
TEST_MANY_PUBLISHES = ['Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 
                        'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 
                        'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 
                        'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 
                        'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 
                        'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.', 'Spam Test.']

class RMQTest(unittest.TestCase):
    ''' Basic testing class for the exchange of messages and setup for RMQ.
    '''

    def test_exchange_and_setup(self):
        ''' The serveer setup will make sure the Queues work as well
        '''
        server = MessageServer()
        self.assertTrue(server.establish_connection())
        self.assertTrue(server.setup_channels())
        self.assertTrue(server.setup_exchange())
        self.assertTrue(server.server_setup())

    def test_publish_and_receive(self):
        ''' We want to test if the can publish and subscribe to RabbitMQ.
            Case 1: Test for one messaage
            Case 2: Test for 2 messages with a greater max_messages
            Case 3: Test for not equaling with a smaller max_messages
        '''
        server = MessageServer()
        self.assertTrue(server.server_setup())

        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = 1, channel_type = server._public_channel)
        self.assertEqual(TEST_NO_PUBLISHES, message_list, 'Messages do not match')

        self.assertTrue(server.publish_message('', channel_type = server._public_channel))
        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = 1, channel_type = server._public_channel)
        self.assertEqual(len(message_list), len(TEST_0_PUBLISHES), 'Length does not match')
        self.assertEqual(TEST_0_PUBLISHES, message_list, 'Messages do not match')

        self.assertTrue(server.publish_message('Hello World!', channel_type = server._public_channel))
        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = 1, channel_type = server._public_channel)
        self.assertEqual(len(message_list), len(TEST_1_PUBLISHES), 'Length does not match')
        self.assertEqual(TEST_1_PUBLISHES, message_list, 'Messages do not match')

        self.assertTrue(server.publish_message('I am here!', channel_type = server._public_channel))
        self.assertTrue(server.publish_message('I am here too!', channel_type = server._public_channel))
        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = 5, channel_type = server._public_channel)
        self.assertEqual(len(message_list), len(TEST_2_PUBLISHES), 'Length does not match')
        self.assertEqual(TEST_2_PUBLISHES, message_list, 'Messages do not match')

        self.assertTrue(server.publish_message('I am here!', channel_type = server._public_channel))
        self.assertTrue(server.publish_message('I am here too!', channel_type = server._public_channel))
        self.assertTrue(server.publish_message('Am I here too?', channel_type = server._public_channel))
        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = 1, channel_type = server._public_channel)
        self.assertNotEqual(len(message_list), len(TEST_3_PUBLISHES), 'Length should not match')
        self.assertNotEqual(TEST_3_PUBLISHES, message_list, 'Messages should not match')

        self.assertTrue(server.publish_message('I am here!', channel_type = server._public_channel))
        self.assertTrue(server.publish_message('I am here too!', channel_type = server._public_channel))
        self.assertTrue(server.publish_message('Am I here too?', channel_type = server._public_channel))
        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = 3, channel_type = server._public_channel)
        self.assertEqual(len(message_list), len(TEST_3_PUBLISHES), 'Lengths should match')
        self.assertEqual(TEST_3_PUBLISHES, message_list, 'Messages should match')

    def test_more_messages(self):
        ''' We want to test if the can publish and subscribe to RabbitMQ.
            In this case we are just going to test a larger message count.
        '''
        server = MessageServer()
        self.assertTrue(server.server_setup())

        for message in TEST_MANY_PUBLISHES:
            self.assertTrue(server.publish_message(message, channel_type = server._public_channel))
        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_MANY_PUBLISHES), channel_type = server._public_channel)
        self.assertEqual(len(message_list), len(TEST_MANY_PUBLISHES), 'Length does not match')
        self.assertEqual(TEST_MANY_PUBLISHES, message_list, 'Messages do not match')
    