from socket import *     # import socket module
import os
import time           # import time module
import ast            # import ast module


# SERVER A CODE
sock = socket()          # Build Socket Object
sock.bind(('', 5000))            # bind the socket with server and port number
sock.listen(2)                 #allow maximum 2 connection to the socket
client, addr = sock.accept()     #wait till a client accept and establish the connection
print("CONNECTION FROM:", str(addr))  # display client address
#client.send(b"This is Server A.")
dir_name = 'C:\\Users\\pshiv\\PycharmProjects\\pythonProject\\MP'    # path of the folder
arr = os.listdir(dir_name)      # list out the files from directory

d = []   # list
for file_name in arr:

    file_path = os.path.join(dir_name, file_name)   # join the file path with directory
    timestamp_str = time.strftime(  '%m/%d/%Y',            # last modification date of file
                                time.gmtime(os.path.getmtime(file_path)))

    files_with_size = (os.stat(file_path).st_size)     # Get file Size in bytes
    def human_readable_size(size, decimal_places=2):   # Get human readable version of file size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f}{unit}"
    human_size = (human_readable_size(files_with_size))
    #data1 = []
    data1 = (file_name, human_size, timestamp_str)    # Get filename, human readable size, date into data
    d.append(data1)           # append all three file into d




#CLIENT CODE FOR THE SERVER B

from socket import *       # import socket module
import os

os.makedirs('client',exist_ok=True)       # Make a directory for the received files

sock = socket()           # Build Socket Object
sock.connect(('localhost',5021))     #bind host address and port together and connect to the server B
with sock,sock.makefile('rb') as clientfile:
    while True:
        raw = clientfile.readline()  # read the file
        if not raw: break  # no more files, server closed connection
        #print(raw.decode())  # print and decode the serverB file
        break      # no more files, server closed connection

# Merge Server A and Server B file


type(raw)   # show the type of raw which contain server B files
raw = raw.decode("utf-8")   # decode the raw
#print("---")
raw = ast.literal_eval(raw)   # convert a string to dictionary
for i in raw:
    d.append(i)

# Sort the files by file name
d = sorted(d , key=lambda x: x[0])
#print(d)

client.sendall(str(d).encode())      # send files to the client and encode it

# disconnect the server
client.close()
