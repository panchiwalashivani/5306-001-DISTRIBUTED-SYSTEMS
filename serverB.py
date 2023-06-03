# Student Name: Shivani Panchiwala
# Student ID: 1001982478

import socket
import pickle
import time
import os
import pandas as pd
import threading

directory = "C:\\Users\\pshiv\\Desktop\\"

host = '127.0.0.6'  # IP address for Server B
df_1 = pd.DataFrame()  # Pandas dataframe
df_2 = pd.DataFrame() # Pandas dataframe

sock2 = socket.socket()  # Create a socket object
sock2.bind((host, 5059))  # Binds server with IP address and Port Number
sock2.listen(2)  # Waiting for a connection and max limit is 2
bFileFound = 0

Fname = "server_B"  # Folder name


def serverA_Files(scr): # A function to receive data from the other server
    while True:
        recv_file = scr.recv(4096)   # receive the data
        serverA_data = pickle.loads(recv_file)  # load the data using pickel
        print("Appended Data")
        print(serverA_data)


dir_name = 'C:\\Users\\pshiv\\PycharmProjects\\lab3\\serverA'  # Path of the folder
arr = os.listdir(dir_name)  # list out the files from directory

sending = []  # Get list
data = ""
for file_name in arr:

    file_path = os.path.join(dir_name, file_name)  # join the file path with directory

    timestamp_str = time.strftime('%m/%d/%Y',  # last modification date of file
                                  time.gmtime(os.path.getmtime(file_path)))
    # print(timestamp_str)
    files_with_size = (os.stat(file_path).st_size)  # Get file Size in bytes


    def human_readable_size(size, decimal_places=2):  # Get human readable version of file size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f}{unit}"


    human_size = (human_readable_size(files_with_size))


def get_data(): # A function to retrieve data from a directory
    sent = os.listdir(directory + Fname)
    df = pd.DataFrame()
    max_mtime = 0
    for file in sent:  # appending filesize,filename, date created for files in Directory B
        stats = os.stat(os.path.join(directory, Fname, file))
        df = df.append({"Filename": file,
                        "Size(KB)": float(stats.st_size) / 1000,
                        "Date modified": time.ctime(stats.st_mtime)},
                       ignore_index=True)
        if max_mtime < stats.st_mtime:
            max_mtime = stats.st_mtime
    return df, max_mtime


df_2 = get_data()
print("Server B Data")
print(df_2)


def send_data(df1): # A function to Send data from the Other Server
    data = pickle.dumps(df1)
    sock.sendall(data)
    #print("Data Sent")


def check_modification(): # operations like Adding,removing,modifying a file in the directory in serverB
    local_df, pre_filemtime=get_data()
    t=os.stat(directory + Fname)
    pre_mtime=t.st_mtime
    pre_atime=t.st_atime
    send_data(local_df)
    while True:
        k=os.stat(directory + Fname)
        curr_mtime=k.st_mtime
        curr_atime=k.st_atime

        if curr_mtime != pre_mtime:
            print("Files Added or Deleted")
            pre_mtime=curr_mtime
            pre_atime = curr_atime
            local_df, pre_filemtime=get_data()
            print(local_df)
            send_data(local_df)

        elif curr_atime != pre_atime:
            files=os.listdir(directory + Fname)
            try:
                files_mtime=[os.stat(directory + Fname + "\\" + file).st_mtime
                              for file in files]
                latest_filemtime=max(files_mtime)
                if latest_filemtime != pre_filemtime:
                    print("Files is Modified")
                    pre_mtime = curr_mtime
                    pre_atime = curr_atime
                    local_df, pre_filemtime=get_data()
                    print(local_df)
                    send_data(local_df)
            except:
                print("Files is Renamed")
                k = os.stat(directory + Fname)
                curr_mtime = k.st_mtime
                curr_atime = k.st_atime
                pre_mtime = curr_mtime
                pre_atime = curr_atime
                local_df, pre_filemtime = get_data()
                print(local_df)
                send_data(local_df)


while True:
    sock, Address = sock2.accept()  # Server A request Accept
    print(Address)
    t1 = threading.Thread(target=check_modification) # Check the modifications part in Server B
    t1.start()
    t2=threading.Thread(target=serverA_Files, args=(sock,)) # Check with the data received from Server A
    t2.start()

sock.close()
server.close()     # close the server
