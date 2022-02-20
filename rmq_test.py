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
            Case 1: No Messages
            Case 2: Empty String Message
            Case 3: Test for one messaage
            Case 4: Test for 2 messages
            Case 5: Test for 3 messages
            Case 6: Test for 3 messages with a greater max_messages
        '''
        server = MessageServer()
        self.assertTrue(server.server_setup())

        test_none = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_NO_PUBLISHES), channel_type = server._public_channel)
        self.assertEqual(len(TEST_NO_PUBLISHES), len(test_none), 'Length does not match')

        self.assertTrue(server.publish_message(TEST_0_PUBLISHES[0], channel_type = server._public_channel))
        test_empty_string = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_0_PUBLISHES), channel_type = server._public_channel)
        self.assertEqual(len(TEST_0_PUBLISHES), len(test_empty_string), 'Length does not match')
        self.assertEqual(TEST_0_PUBLISHES, test_empty_string, 'Messages do not match')

        self.assertTrue(server.publish_message(TEST_1_PUBLISHES[0], channel_type = server._public_channel))
        test_1 = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_1_PUBLISHES), channel_type = server._public_channel)
        self.assertEqual(len(TEST_1_PUBLISHES), len(test_1), 'Length does not match')
        self.assertEqual(TEST_1_PUBLISHES, test_1, 'Messages do not match')

        for message in TEST_2_PUBLISHES:
            self.assertTrue(server.publish_message(message, channel_type = server._public_channel))
        test_2 = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_1_PUBLISHES), channel_type = server._public_channel)
        self.assertEqual(len(TEST_2_PUBLISHES), len(test_2), 'Length does not match')
        self.assertEqual(TEST_2_PUBLISHES, test_2, 'Messages do not match')

        for message in TEST_3_PUBLISHES:
            self.assertTrue(server.publish_message(message, channel_type = server._public_channel))
        test_3 = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_1_PUBLISHES), channel_type = server._public_channel)
        self.assertEqual(len(TEST_3_PUBLISHES), len(test_3), 'Length does not match')
        self.assertEqual(TEST_3_PUBLISHES, test_3, 'Messages do not match')

        for message in TEST_3_PUBLISHES:
            self.assertTrue(server.publish_message(message, channel_type = server._public_channel))
        test_3 = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_1_PUBLISHES) + 3, channel_type = server._public_channel)
        self.assertEqual(len(TEST_3_PUBLISHES), len(test_3), 'Length does not match')
        self.assertEqual(TEST_3_PUBLISHES, test_3, 'Messages do not match')

    def test_more_messages(self):
        ''' We want to test if the can publish and subscribe to RabbitMQ.
            In this case we are just going to test a larger message count.
        '''
        server = MessageServer()
        self.assertTrue(server.server_setup())
        
        for message in TEST_MANY_PUBLISHES:
            server.publish_message(message, channel_type = server._public_channel)

        message_list = server.consume_message(destination_queue = RMQ_DEFAULT_PUBLIC_QUEUE, max_messages = len(TEST_MANY_PUBLISHES), channel_type = server._public_channel)
        self.assertEqual(len(message_list), len(TEST_MANY_PUBLISHES), 'Length does not match')
        self.assertEqual(TEST_MANY_PUBLISHES, message_list, 'Messages do not match')
        