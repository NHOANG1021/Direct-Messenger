import socket
import time
import ds_protocol


class DirectMessage:
    '''
    DirectMessage class to create objects
    '''
    def __init__(self, recipient, message):
        '''
        initializes neccesary variables
        '''
        self.recipient = recipient
        self.message = message
        self.timestamp = str(time.time())

    def __repr__(self) -> str:
        '''
        represents the DirectMessage objects as strings for readability
        '''
        return str((self.recipient, self.message, self.timestamp))


class DirectMessenger:
    '''
    All the required methods for GUI
    '''
    def __init__(self, server='168.235.86.101', port=3021, username=None,
                 password=None):
        '''
        Initializes variables required to communicate to server
        '''
        self.server = server
        self.port = port
        self.username = username
        self.password = password

        join_msg = '{"join": {"username": "'
        join_msg += self.username + '","password": "'
        join_msg += self.password + '", "token":""}}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))

            send1 = client.makefile('w')  # treat the socket like a file
            recv = client.makefile('r')

            send1.write(join_msg + '\r\n')
            send1.flush()

            recv_msg = recv.readline()[:-1]
            print(recv_msg)

            start_index = recv_msg.rfind(':') + 3
            end_index = recv_msg.rfind('"')
            user_token = recv_msg[start_index:end_index]
            self.token = user_token

    def send(self, message: str, recipient: str) -> bool:
        '''
        Functionality to direct message someone through the server
        '''
        # must return true if message successfully sent, false if send failed.
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, self.port))

                send1 = client.makefile('w')  # treat the socket like a file
                recv = client.makefile('r')

                dm = '{"token":"' + self.token + '", "directmessage": '
                dm += '{"entry": "'
                dm += message + '","recipient":"' + recipient + '", '
                dm += '"timestamp": "'
                dm += str(time.time()) + '"}}\r\n'
                send1.write(dm)
                send1.flush()
                recv_msg = recv.readline()[:-1]
                print(recv_msg)

                f = open('sent.txt', 'a', encoding='utf-8')
                f.write(str(ds_protocol.extract_sender_info(dm)) + '\n')
                f.close()

                return True
        except TypeError as er:
            print('ERROR', er)
            return False
        except socket.gaierror as er:
            print('ERROR', er)
            return False
        except ConnectionRefusedError as er:
            print('ERROR', er)
            return False
        except TimeoutError as er:
            print('ERROR', er)
            return False
        except OSError as er:
            print('ERROR', er)
            return False

    def retrieve_new(self) -> list:
        '''
        Functionality to retrieve all new messages from server
        Returns a list of tuples aka DirectMessage objects
        '''
        # return a list of DirectMessage objects containing all new messages
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, self.port))

                send1 = client.makefile('w')
                recv = client.makefile('r')

                unread = '{"token":"' + self.token
                unread += '", "directmessage": "new"}'
                send1.write(unread)
                send1.flush()
                recv_msg = recv.readline()[:-1]
                new_messages = ds_protocol.extract_json_dm(recv_msg)
                dm_objects = []
                for i in new_messages:
                    create_object = DirectMessage(i[0], i[1])
                    dm_objects.append(create_object)
            return dm_objects
        except TypeError as er:
            print('ERROR', er)
            return False
        except socket.gaierror as er:
            print('ERROR', er)
            return False
        except ConnectionRefusedError as er:
            print('ERROR', er)
            return False
        except TimeoutError as er:
            print('ERROR', er)
            return False
        except OSError as er:
            print('ERROR', er)
            return False

    def retrieve_all(self) -> list:
        '''
        Functionality to retrieve all messages from server
        Returns a list of tuples aka DirectMessage objects
        '''
    # return a list of DirectMessage objects containing all messages
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server, self.port))

                send1 = client.makefile('w')
                recv = client.makefile('r')

                all = '{"token":"' + self.token + '", "directmessage": "all"}'
                send1.write(all)
                send1.flush()
                recv_msg = recv.readline()[:-1]
                all_messages = ds_protocol.extract_json_dm(recv_msg)
                dm_objects = []
                for i in all_messages:
                    create_object = DirectMessage(i[0], i[1])
                    dm_objects.append(create_object)

            return dm_objects
        except TypeError as er:
            print('ERROR', er)
            return False
        except socket.gaierror as er:
            print('ERROR', er)
            return False
        except ConnectionRefusedError as er:
            print('ERROR', er)
            return False
        except TimeoutError as er:
            print('ERROR', er)
            return False
        except OSError as er:
            print('ERROR', er)
            return False

    def load_data(self):
        '''
        Functionality to store the messages locally
        '''
        f = open('all.txt', 'w', encoding='utf-8')
        contents = self.retrieve_all()
        f.write(str(contents))
        f.close()
        return contents
