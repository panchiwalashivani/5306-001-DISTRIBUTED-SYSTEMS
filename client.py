# Client Code
from socket import *       # import socket module
import os


# Make a directory for the received files.
os.makedirs('client',exist_ok=True)

sock = socket()           # Build Socket Object
sock.connect(('localhost',5000))     #bind host address and port together and connect to the server A
with sock,sock.makefile('rb') as clientfile:
    while True:
        raw = clientfile.readline()    # read the file
        if not raw: break # no more files, server closed connection.
        print(raw.decode())  # print and decode the serverA file
        break    # no more files, server closed connection

