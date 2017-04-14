import socket
import threading
import argparse
import os
import datetime

def read_text_from_user_input(string):
    return input(string)

def build_message(user_name, user_message):
    return 'user:'+user_name+'\nmessage:'+ user_message +'\n\n'

def parse_message(application_message):
    msg = application_message.split('\n')
    user_name = msg[0].split(':')
    user_message = msg[1].split(':')
    return user_name[1], user_message[1]

def chat_application():
    ip_address = '192.168.1.255'
    port = 2052
    user_name = read_text_from_user_input('Enter your name: ')
    threading.Thread(target=sender, args=(user_name, ip_address, port)).start()
    threading.Thread(target=receiver, args=(ip_address, port)).start()


def sender(user_name, ip_address, port):
    while True:
        user_message = read_text_from_user_input('')
        application_message = build_message(user_name, user_message)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(application_message.encode('utf-8'), (ip_address, port))
        s.close()

def receiver(ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip_address, port))
    while True:
        application_message, address = s.recvfrom(port)
        #print(application_message.decode('utf-8'))
        (user_name, user_message) = parse_message(application_message.decode('utf-8'))
        timestamp = datetime.datetime.now()
        print(str(timestamp) +' ['+ user_name +'] ' +user_message)

chat_application()