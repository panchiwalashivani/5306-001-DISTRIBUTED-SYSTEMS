# lab2_panchiwala_smp2478
# UTA ID: 1001982478
# Name: Shivani Manojkumar Panchiwala
# Completion Date: 10/31/2021


# Client Code
from socket import *  # import socket module

sock = socket()  # Build Socket Object
sock.connect(('localhost', 5009))  # bind host address and port together and connect to the server A
while True:
    data = sock.recv(4096)
    #print(data)
    if data:
        serverBFiles = data.decode("utf-8")
        print(serverBFiles)
# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(4096).decode()
merge_files, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(merge_files)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))






