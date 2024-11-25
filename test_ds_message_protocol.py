import socket
import unittest
import ds_client


class TestDSProtocol(unittest.TestCase):
    '''
    Unit tests for the ds_protocol module
    '''
    def setUp(self):
        '''
        setup for unit tests
        '''
        self.server = '168.235.86.101'
        self.port = 3021
        self.username = 'qwerty1021'
        self.password = 'asdfghjkl1021'
        self.message = 'unit test message'

    def test_send_dm(self):
        '''
        tests the send() function in ds_client
        '''
        test = ds_client.send_dm(self.server,
                                 self.port,
                                 self.username,
                                 self.password,
                                 self.message)
        self.assertTrue(test)

    def test_unread(self):
        '''
        tests the unread() function in ds_client
        '''
        join_msg = '{"join": {"username": "' + self.username + '","password":"'
        join_msg += self.password + '", "token":""}}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.server, self.port))
            send1 = client.makefile('w')  # treat the socket almost like a file
            recv = client.makefile('r')

            send1.write(join_msg + '\r\n')
            send1.flush()
            recv_msg = recv.readline()[:-1]

            user_token_start_index = recv_msg.rfind(':') + 3
            user_token_end_index = recv_msg.rfind('"')
            user_token = recv_msg[user_token_start_index:user_token_end_index]

            dm = '{"token":"' + user_token + '", "directmessage": {"entry": "'
            dm += self.message + '","recipient":"' + self.username
            dm += '", "timestamp": "' + "1710480545.7132168" + '"}}\r\n'
            send1.write(dm)
            send1.flush()
            recv_msg = recv.readline()[:-1]
            recv_msg = ds_client.unread(send1, recv, user_token)

        self.assertEqual(recv_msg, '{"response": {"type": "ok", "messages": [{"message": "unit test message", "from": "qwerty1021", "timestamp": "1710480545.7132168"}]}}')

    def test_all(self):
        '''
        tests the all() function in ds_client
        '''
        username = 'asdfghjkl1021'
        password = 'qwerty1021'
        join_msg = '{"join": {"username": "' + username + '","password": "'
        join_msg += password + '", "token":""}}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.server, self.port))
            send1 = client.makefile('w')  # treat the socket almost like a file
            recv = client.makefile('r')
            send1.write(join_msg + '\r\n')
            send1.flush()
            recv_msg = recv.readline()[:-1]

            user_token_start_index = recv_msg.rfind(':') + 3
            user_token_end_index = recv_msg.rfind('"')
            user_token = recv_msg[user_token_start_index:user_token_end_index]

            recv_msg = ds_client.all(send1, recv, user_token)
        self.assertEqual(recv_msg, '{"response": {"type": "ok", "messages": [{"message": "unit test message","from": "asdfghjkl1021", "timestamp": "1710881532.1917033"}]}}')


if __name__ == '__main__':
    unittest.main()
