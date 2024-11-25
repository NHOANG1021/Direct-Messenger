import socket
import time


def send_dm(server: str, port: int, username: str, password: str,
            message: str):
    '''
    Allows a user to send a direct message utilizing the DS server
    '''
    try:
        join_msg = '{"join": {"username": "' + username + '","password": "'
        join_msg += password + '", "token":""}}'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))
            send1 = client.makefile('w')
            recv = client.makefile('r')

            send1.write(join_msg + '\r\n')
            send1.flush()

            recv_msg = recv.readline()[:-1]
            print(recv_msg)

            user_token_start_index = recv_msg.rfind(':') + 3
            user_token_end_index = recv_msg.rfind('"')
            user_token = recv_msg[user_token_start_index:user_token_end_index]

            dm = '{"token":"' + user_token + '", "directmessage": {"entry": "'
            dm += message + '","recipient":"' + username
            dm += '", "timestamp": "' + str(time.time()) + '"}}\r\n'
            send1.write(dm)
            send1.flush()
            recv_msg = recv.readline()[:-1]
            print(recv_msg)

            unread_msg = unread(send1, recv, user_token)
            print(unread_msg)

            all_msg = all(send1, recv, user_token)
            print(all_msg)

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


def unread(send, recieve, user_token):
    '''
    functionality to recieve unread dms
    '''
    unread1 = '{"token":"' + user_token + '", "directmessage": "new"}'
    send.write(unread1)
    send.flush()
    recv_msg = recieve.readline()[:-1]

    return recv_msg


def all(send, recieve, user_token):
    '''
    functionality to recieve all dms
    '''
    all1 = '{"token":"' + user_token + '", "directmessage": "all"}'
    send.write(all1)
    send.flush()
    recv_msg = recieve.readline()[:-1]
    f = open('all.txt', 'w', encoding='utf-8')
    f.write(recv_msg)
    f.close()

    return recv_msg
