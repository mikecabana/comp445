import socket
import threading
import argparse
import os
import re
import httplib


def run_server(host, port, directory):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('The server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr, directory)).start()
    finally:
        listener.close()


def handle_client(conn, addr, directory):
    if args.v:
        print 'New client from', addr
    try:
        while True:
            data = conn.recv(1024)
            print data
            if not data:
                if args.v:
                    print 'Data error from sender'
                break
            
            #parse the request header
            parse = re.search('(GET|POST) \/(\w+.\w+)? (HTTP\/\d.\d)(?:\\r\\n)?\s*((?:\w+-?\w+: .*\s)*)(?:\\r\\n)?(\s?.*)?', data)

            method = parse.group(1)
            path = parse.group(2)
            ver = parse.group(3)
            header = parse.group(4)
            print method, path
           
            # if method == 'GET' and path == '/':
            #     files = os.listdir(directory)
            #     if args.v:
            #         for f in files:
            #             print f
            #     returnData = u'will display directory list\n'
            # elif method == 'GET' and re.search(ur'\/\w+', path):
            #     returnData = u'will display file content\n'
            # elif method == 'POST' and re.search(ur'\/\w+', path):
            #     returnData = u'will overwrite file content\n'
            # else:
            #     returnData = u'error occured\n'
        conn.sendall(data)
    finally:
        conn.close()



def checkIfDir (string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError()

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", help="server port to listen on", type=int, default=8080)
parser.add_argument("-d", help="path to directory", type=checkIfDir)
parser.add_argument("-v", help="enable verbosity", action='store_true')
args = parser.parse_args()
run_server('', args.p, args.d)
