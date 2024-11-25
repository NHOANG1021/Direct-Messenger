import unittest
import socket
import ds_messenger
import ds_protocol


class TestDSMessenger(unittest.TestCase):
    '''
    Unit tests for the ds_messenger module
    '''
    def setUp(self) -> None:
        '''
        setup variables for the unit test
        '''
        self.recipient = 'Nicholas'
        self.message = 'unit test message'
        self.server = '168.235.86.101'
        self.port = 3021
        self.username = 'Nicholas'
        self.password = 'Hoang'
        self.dm_obj = ds_messenger.DirectMessage(self.recipient, self.message)
        self.dms_obj = ds_messenger.DirectMessenger(self.server,
                                                    self.port,
                                                    self.username,
                                                    self.server)

    def test_DirectMessage(self):
        '''
        tests the DirectMessage class
        '''
        test_dm_obj = ds_messenger.DirectMessage('NICHOLAS', 'HOANG')
        test_self_type = type(self.dm_obj)
        test_type = type(test_dm_obj)
        self.assertEqual(test_type, test_self_type)

    def test_DirectMessenger_send(self):
        '''
        tests the DirectMessenger class' send() method
        '''
        result = self.dms_obj.send(self.message, self.recipient)
        # print(result)
        self.assertEqual(result, True)

    def test_DirectMessenger_retrieve_new(self):
        '''
        tests the DirectMessenger class' retrieve_new() method
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.server, self.port))

            send1 = client.makefile('w')  # treat the socket almost like a file
            recv = client.makefile('r')

            unread = '{"token":"' + "ad0913a1-fc89-4461-8826-"
            unread += "1cb5ab897a2b" + '", "directmessage": "new"}'
            send1.write(unread)
            send1.flush()
            recv_msg = recv.readline()[:-1]
            new_messages = ds_protocol.extract_json_dm(recv_msg)
            dm_objects = []
            for i in new_messages:
                create_object = ds_messenger.DirectMessage(i[0], i[1])
                dm_objects.append(create_object)

        self.assertEqual(type(dm_objects), list)

    def test_DirectMessenger_retrieve_all(self):
        '''
        tests the DirectMessenger class' retrieve_all() method
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.server, self.port))

            send1 = client.makefile('w')
            recv = client.makefile('r')

            all = '{"token":"' "ad0913a1-fc89-4461-8826-1cb5"
            all += "ab897a2b" '", "directmessage": "all"}'
            send1.write(all)
            send1.flush()
            recv_msg = recv.readline()[:-1]
            new_messages = ds_protocol.extract_json_dm(recv_msg)
            dm_objects = []
            for i in new_messages:
                create_object = ds_messenger.DirectMessage(i[0], i[1])
                dm_objects.append(create_object)

        self.assertEqual(type(dm_objects), list)

    def test_DirectMessengerLoadData(self):
        '''
        tests the DirectMessenger class' load_data() method
        '''
        f = open('all.txt', 'r', encoding='utf-8')
        contents = f.read()
        length = len(contents)
        self.assertGreater(length, 1)


if __name__ == '__main__':
    unittest.main()
