import socket
import threading
import os
import datetime

def read_text_from_user_input(string):
    return input(string)

def build_message(user_name, command_name, user_message):
    return 'user:'+user_name+'\ncommand:'+ command_name +'\nmessage:'+ user_message +'\n\n'

def parse_message(application_message):
    msg = application_message.split('\n')
    user_name = msg[0].split(':')
    command_name = msg[1].split(':')
    user_message = msg[2].split(':')
    return user_name[1], command_name[1], user_message[1]

def chat_application():
    ip_address = '255.255.255.255'
    port = 5001
    user_name = read_text_from_user_input('Enter your name: ')
    threading.Thread(target=sender, args=(user_name, ip_address, port)).start()
    threading.Thread(target=receiver, args=(port,)).start()


def sender(user_name, ip_address, port):
    global users
    command_name = 'JOIN'
    user_message = 'joined!'
    #users += user_name
    application_message = build_message(user_name, command_name, user_message)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(application_message.encode('ascii'),(ip_address, port))
    s.close()
    while True:
        command_name = 'TALK'
        user_message = read_text_from_user_input('')
        if user_message == '/leave':
            command_name = 'LEAVE'
            user_message = 'left!'
            print('Bye now!')
        if user_message == '/who':
            print('Connected Users: ', users)
            command_name = ''
            user_message = ''
        application_message = build_message(user_name, command_name, user_message)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(application_message.encode('utf-8'), (ip_address, port)) 
        s.close()

def receiver(port):
    global users
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    while True:
        application_message, address = s.recvfrom(port)
        #print(application_message.decode('utf-8'))
        (user_name, command_name, user_message) = parse_message(application_message.decode('utf-8'))
        timestamp = datetime.datetime.now()
        if command_name == 'JOIN':
            users += [user_name]
            print(str(timestamp) +' '+user_name+' '+user_message)
            command_name = 'PING'
            user_message = ''
            application_message = build_message(user_name, command_name, user_message)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(application_message.encode('utf-8'), (ip_address, port)) 
            s.close()
        if command_name == 'PING':
            users += [user_name]
        if command_name == 'TALK':
            print(str(timestamp) +' ['+ user_name +'] ' +user_message)
        if command_name == 'LEAVE':
            users.remove(user_name)
            print(str(timestamp) +' '+user_name+' '+user_message)
            os._exit(0)

users = []
chat_application()

#print (build_message('mike', 'JOIN', 'joined!'))