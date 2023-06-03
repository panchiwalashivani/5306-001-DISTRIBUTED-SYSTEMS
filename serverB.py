import socket     # import socket module
import os
import time       # import time module

# SERVER B CODE
# create a socket at server side
# using TCP / IP protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 5021))              # bind the socket with server and port number
sock.listen(2)                        #allow maximum 2 connection to the socket
client, addr = sock.accept()      #wait till a client accept and establish the connection
print("CONNECTION FROM:", str(addr))   # display client address
#client.send(b"This is Server B.")
dir_name = 'C:\\Users\\pshiv\\PycharmProjects\\pythonProject\\SP'   # Path of the folder
arr = os.listdir(dir_name)      # list out the files from directory


sending = []  # Get list
data = ""
for file_name in arr:

    file_path = os.path.join(dir_name, file_name) # join the file path with directory

    timestamp_str = time.strftime(  '%m/%d/%Y',                 # last modification date of file
                                time.gmtime(os.path.getmtime(file_path)))
    #print(timestamp_str)
    files_with_size = (os.stat(file_path).st_size)  # Get file Size in bytes
    def human_readable_size(size, decimal_places=2):   # Get human readable version of file size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f}{unit}"
    human_size = (human_readable_size(files_with_size))
    #data = []
    data = (file_name, human_size, timestamp_str)      # Get filename, human readable size, date into data
    sending.append(data)                      # append data to the sending which is list

client.sendall(str(sending).encode())      # send files to the client and encode it

# disconnect the server
client.close()