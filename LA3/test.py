import socket
import threading
import argparse
import os
import datetime

def read_text_from_user_input(string):
    return input(string)
    
def build_message(user_message, user_command, user_name):
    return '' + user_name + '\n' + user_command  + "\n" + user_message + '\n'

def parse_message(application_message):
    user_name = application_message.split("\n")[0]
    user_command = application_message.split("\n")[1]
    user_message = application_message.split("\n")[2]
    return user_name, user_command, user_message

def chat():
    serverName = '127.0.0.1'
    serverPort = 8070
    user_name = read_text_from_user_input("Enter your name: ")
    threading.Thread(target=client, args=(user_name, serverName, serverPort)).start()
    threading.Thread(target=server, args=(serverName, serverPort)).start()


def client(user_name, serverName, serverPort):
    welcomeMessage = build_message('', 'JOIN', user_name)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    clientSocket.sendto(welcomeMessage.encode('ascii'),('255.255.255.255', serverPort))
    clientSocket.close()

    while True:
        user_message = read_text_from_user_input('')
        if(user_message.split(' ')[0] == "/private"):
            user_command = "PRIVATE-TALK"
            user_name_private = user_message.split(' ')[1]
            user_message = ''
            application_message = build_message(user_message, user_command, user_name_private)
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientSocket.sendto(application_message.encode('ascii'), (serverName, serverPort))
            privateAddress, serverAddress = clientSocket.recvfrom(2048)
            privateAddress = privateAddress.decode('utf-8')
            if(privateAddress == 'Name not found'):
                print(user_name_private + " is not currently logged in")
            else:
                user_message = read_text_from_user_input('Private message to ' + user_name_private + ': ')
                user_command = "TALK"
                application_message = build_message(user_message, user_command, user_name_private + " (PRIVATE)")
                clientSocket.sendto(application_message.encode('ascii'), (privateAddress, serverPort))

            clientSocket.close()
        else:
            user_command = 'TALK'
            if(user_message == '/leave'):
                user_command = "LEAVE"
            if(user_message == '/who'):
                user_command = "WHO"
            application_message = build_message(user_message, user_command, user_name)
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            if(user_command == "WHO"):
                clientSocket.sendto(application_message.encode('ascii'), (serverName, serverPort))
            else:
                clientSocket.sendto(application_message.encode('ascii'), ('255.255.255.255', serverPort))
            clientSocket.close()
            if(user_command == "LEAVE"):
                user_command = "QUIT"
                application_message = build_message(user_message, user_command, user_name)
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                clientSocket.sendto(application_message.encode('ascii'), (serverName, serverPort))
                clientSocket.close()
                exit(0)
        

def server(serverName, serverPort):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    users = []
    while True:
        application_message, address = serverSocket.recvfrom(2048)
        user_name, user_command, user_message = parse_message(application_message.decode('utf-8'))
        timestamp = datetime.datetime.now()
        if(user_command == "JOIN"):
            user_command = "PING"
            users.append((user_name, address[0]))
            print(str(timestamp) + ' ' + user_name + ' joined!')
            user_name = (users[0][0], address[0])
            if(address[0] != socket.gethostbyname(socket.gethostname())):
                application_message = build_message(user_message, user_command, user_name[0])
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                clientSocket.sendto(application_message.encode('ascii'), (address[0], serverPort))
                clientSocket.close()
        elif(user_command == "TALK"):
            if(len(user_name.split(' ')) == 2):
                print(str(timestamp) + ' [' + user_name.split(' ')[0] + '] ' + user_name.split(' ')[1] + ': ' + user_message)
            else:
                print(str(timestamp) + ' [' + user_name + ']: ' + user_message)
        elif(user_command == "LEAVE"):
            users.remove((user_name, address[0]))
            print(str(timestamp) + ' ' + user_name + ' left!')
        elif(user_command == "WHO"):
            print("Connected users: " + str([x[0] for x in users]))
        elif(user_command == "QUIT"):
            print("Bye now!")
            exit(0)
        elif(user_command == "PING"):
            users.append((user_name, address[0]))
        elif(user_command == "PRIVATE-TALK"):
            for x in users:
                if x[0] == user_name:
                    serverSocket.sendto(x[1].encode('ascii'), address)
            serverSocket.sendto('Name not found'.encode('ascii'), address)
        #else:
            #do nothing
chat()