import unittest
import requests
import json
 
STARTUP_URL = 'http://localhost:8000/'
SEND_URL = 'http://localhost:8000/send/'
RECEIVE_URL = 'http://127.0.0.1:8000/messages/'
PUBLIC_QUEUE = 'general'
MESSAGE_TEST = 'Send API Test!'

class APITest(unittest.TestCase):
    """
    Basic testing class for the FastAPI send and recieve
    """
    book = '{}'.format(STARTUP_URL)

    def test_startup(self):
        ''' This test will test the startup responce when running uvicorn.
        '''
        startup = requests.get(STARTUP_URL)
        self.assertEqual(startup.status_code, 200)

    def test_send_receive(self):
        ''' This test will test the receiving of messages from the server using query parameters.
            First consume will try to clear the queue
            1 Message will be send to be received by FastAPI, it will make sure the status code is ok and
            the message matches what was sent
        '''
        send_message = requests.post(SEND_URL, params = {'message' : MESSAGE_TEST, 'target_queue' : PUBLIC_QUEUE})
        self.assertEqual(send_message.status_code, 200)
        receive_message = requests.get(RECEIVE_URL, params = {'message_count' : 1, 'queue_destination' : PUBLIC_QUEUE})
        self.assertEqual(receive_message.status_code, 200)
        json_load = json.loads(receive_message.text)
        messages = json_load['data'][0]
        self.assertEqual(messages, MESSAGE_TEST)