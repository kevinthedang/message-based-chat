import unittest
import mess_chat
import requests
import pytest
 
SERVER_URL = 'http://cps-devops.gonzaga.edu:5672/'
STARTUP_URL = 'http://localhost:8000/'
RECEIVE_URL = 'http://127.0.0.1:8000/messages/?=message_count=1&queue_destination=general'

class APITest(unittest.TestCase):
    """
    Basic testing class using unittest library base class
    """
    book = '{}'.format(STARTUP_URL)

    def test_startup(self):
        ''' This test will test the startup responce when running uvicorn.
        '''
        startup = requests.get(STARTUP_URL)
        print(APITest.book)
        self.assertEqual(startup.status_code, 200)


    def test_send(self):
        ''' This test will test the sending of a message using query parameters.
            Cases:
        '''

    def test_messages(self):
        ''' This test will test the receiving of messages from the server using query parameters.
            Cases:
        '''