import os
import argparse
import socket
import re

def runHttpfs(port, directory):
    host = ''
    localdir = directory
    if directory is None:
        localdir = os.path.dirname(os.path.realpath(__file__))
    
    
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host, port))
    listener.listen(5)
    if args.verbose:
        print('Httpfs server is listening at port', port)
    while True:
        files = os.listdir(localdir)
        conn, addr = listener.accept()
        request = conn.recv(1024).decode("utf-8")
        #breaking up the request
        request = request.split('\r\n')
        mpv = request[0].split()
        method = mpv[0]
        path = mpv[1]

        index = request.index('') 
        data = ''
        for l in request[index+1:]:
            data += l + '\n'

        response = ''
        
        if method == 'GET':
            if path == '/':
                if args.verbose:
                    print 'Responding with list of files'
                for f in files:
                    response += f + '\n'
            elif re.search(r'\/\w+.\w+', path):
                path = path.strip('/')
                if args.verbose:
                    print 'Responding with contents of', path
                if path in files:
                    theFile = open(localdir +'/'+ path, 'r')
                    response = theFile.read() + '\n'
                    theFile.close()
                else:
                    if args.verbose:
                        print 'Responding with HTTP 404 - file(s) not found', path
                    response = 'HTTP 404 - file(s) not found\n'
        elif method == 'POST':
            path = path.strip('/')
            if path in files:
                if args.verbose:
                    print 'Responding with data overwritten to file', path
                theFile = open(localdir +'/'+ path, 'w+')
                theFile.write(data)
                theFile.close()
                response = 'Data overwritten to file '+path
            elif path not in files:
                if args.verbose:
                    print 'Responding with data written to new file '+ path
                theFile = open(localdir +'/'+ path, 'w+')
                theFile.write(data)
                theFile.close()
                response = 'Data written to new file '+ path
            else:
                if args.verbose:
                    print 'Responding with HTTP 403 - action refused'
                response = "HTTP 403 - action refused \n"

        conn.sendall(response.encode('utf-8'))
        conn.close()


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='verbosity', action='store_true')
parser.add_argument('-p', '--port', help='Spcify port - Default is 8007', type=int, default=8007)
parser.add_argument('-d', '--directory', help='Specify directory - Default is current', type=str)
args = parser.parse_args()
runHttpfs(args.port, args.directory)