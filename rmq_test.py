from socket import gaierror
import unittest

from rmq import MessageServer

class BasicTest(unittest.TestCase):
    """
    Basic testing class using unittest library base class
    """    

    def test_server_connection(self):
        ''' Tests the Connection the RabbitMQ Server
            'server.establish_connection()' is causing NoneType issues
        '''
        server = MessageServer()
        self.assertRaises(gaierror, server.establish_connection())

    