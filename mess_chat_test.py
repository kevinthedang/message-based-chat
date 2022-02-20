import unittest
import requests
 
STARTUP_URL = 'http://localhost:8000/'
SEND_URL = 'http://localhost:8000/send/'
RECEIVE_URL = 'http://127.0.0.1:8000/messages/'
PUBLIC_QUEUE = 'general'

class APITest(unittest.TestCase):
    """
    Basic testing class using unittest library base class
    """
    book = '{}'.format(STARTUP_URL)

    def test_startup(self):
        ''' This test will test the startup responce when running uvicorn.
        '''
        startup = requests.get(STARTUP_URL)
        self.assertEqual(startup.status_code, 200)


    def test_send(self):
        ''' This test will test the sending of a message using query parameters.
        '''
        send_message = requests.post(SEND_URL, data = {'message' : 'Send API Test!', 'target_queue' : PUBLIC_QUEUE})
        self.assertEqual(send_message.status_code, 200)

    def test_messages(self):
        ''' This test will test the receiving of messages from the server using query parameters.
            Cases: 1 Message
        '''
        receive_message = requests.get(RECEIVE_URL, data = {'message_cout' : 1, 'queue_destination' : PUBLIC_QUEUE})
        self.assertEqual(receive_message.status_code, 200)