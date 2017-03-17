import socket
import threading
import argparse
import os


def run_server(host, port, dir):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('The server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr, dir)).start()
    finally:
        listener.close()


def handle_client(conn, addr, dir):
    print 'New client from', addr
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                if args.v:
                    print 'Data error from sender'
                break
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
