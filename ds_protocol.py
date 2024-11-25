import json


def extract_json_dm(json_msg):
    '''
    extracts the neccesary data from the server response message
    '''
    json_obj = json.loads(json_msg)
    message_list = json_obj['response']['messages']
    messages = []

    for i in range(len(message_list)):
        message_tuple = (message_list[i]['from'], message_list[i]['message'])
        messages.append(message_tuple)

    return messages


def extract_sender_info(json_msg):
    '''
    extracts the sender info from the server message
    '''
    json_obj = json.loads(json_msg)
    entry = json_obj["directmessage"]['entry']
    recipient = json_obj["directmessage"]['recipient']
    time = json_obj["directmessage"]['timestamp']
    message_tuple = (entry, recipient, time)

    return message_tuple
