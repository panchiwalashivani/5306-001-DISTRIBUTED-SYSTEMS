# Student Name: Shivani Panchiwala
# Student ID: 1001982478

import socket
import os
import pandas as pd
import pickle
import time
import threading
import datetime
import numpy as np
from queue import Queue
from dirsync import sync

directory= "C:\\Users\\pshiv\\Desktop\\"
df_1 = pd.DataFrame()  # Pandas dataframe
df_2 = pd.DataFrame() # Pandas dataframe

host = '127.0.0.5'  # IP address for Server A

sock1=socket.socket()  # Create a socket object
sock1.bind((host, 5067))  # Binds server with  IP address and Port Number
sock2=socket.socket()   # Create another socket object
sock1.listen(2) # Waiting for a connection
sock2.connect(("127.0.0.6", 5059))  # Connect with Server B
bFileFound=0

Fname= "server_A"    # Folder Path

# Syncing the files Vice-Versa
source_path = 'C:\\Users\\pshiv\\PycharmProjects\\lab3\\serverA\\'
target_path = 'C:\\Users\\pshiv\\PycharmProjects\\lab3\\serverB\\'

sync(source_path, target_path, 'sync')  # for syncing one way
sync(target_path, source_path, 'sync')  # for syncing the opposite way

serverA_que=Queue() # Create a Queue for server A
serverB_que=Queue() # Create a Queue for server B
client_que=Queue() # Create a Queue for Client
lock_que=Queue()  # Create Lock Queue
unlock_que=Queue() # Create Unlock Queue

def serverB_Files(queue): # Receive data from the Server B
    while True:
        recv_file = sock2.recv(4096)   # receive the data
        serverB_data = pickle.loads(recv_file)
        queue.put(serverB_data)
dir_name = 'C:\\Users\\pshiv\\PycharmProjects\\lab3\\serverA'   # Path of the folder
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
    #data = (file_name, human_size, timestamp_str)      # Get filename, human readable size, date into data
def get_data(): # Retrieve data from a directory
    sent=os.listdir(directory + Fname)
    df_1 = pd.DataFrame()
    max_mtime=0
    for file in sent: # appending filesize,filename, date created for files in server A
        stats=os.stat(os.path.join(directory, Fname, file))
        df_1 = df_1.append({"Filename": file,
                        "Size(KB)": float(stats.st_size) / 1000,
                        "Date modified": time.ctime(stats.st_mtime)},
                       ignore_index=True)
        if max_mtime < stats.st_mtime:
            max_mtime = stats.st_mtime
    return df_1, max_mtime

df_2= get_data()
print(df_2)

def send_data(df1): # A function to Send data from server B
    data = pickle.dumps(df1)
    sock2.sendall(data)

def check_modification(queue): # operations like Adding,removing,modifying a file in the server A
    df_2, pre_filemtime=get_data()
    queue.put(df_2)
    t=os.stat(directory + Fname)
    pre_mtime=t.st_mtime
    pre_atime=t.st_atime
    while True:
        k=os.stat(directory + Fname)
        curr_mtime=k.st_mtime
        curr_atime=k.st_atime

        if curr_mtime != pre_mtime:
            print("Files Added/Deleted")
            pre_mtime=curr_mtime
            pre_atime = curr_atime
            df_2, pre_filemtime=get_data()
            queue.put(df_2)
            #print("Server A Data")
            print(df_2)

        elif curr_atime != pre_atime:
            files=os.listdir(directory + Fname)
            try:
                files_mtime=[os.stat(directory + Fname + "\\" + file).st_mtime
                              for file in files]
                latest_filemtime=max(files_mtime)
                if latest_filemtime != pre_filemtime:
                    print("Files Modified")
                    pre_mtime = curr_mtime
                    pre_atime = curr_atime
                    local_df, pre_filemtime=get_data()
                    queue.put(local_df)
                    #print("Server A Data")
                    print(local_df)
            except:
                print("Files Renamed")
                k = os.stat(directory + Fname)
                curr_mtime = k.st_mtime
                curr_atime = k.st_atime
                pre_mtime = curr_mtime
                pre_atime = curr_atime
                local_df, pre_filemtime = get_data()
                queue.put(local_df)
                #print("Server A Data")
                print(local_df)

def update(data1, new_data):
    print(data1.columns)
    locked_files = data1[ data1['locked/unlocked']== 'locked']['Filename'].values
    #new_data['locked/unlocked'] = ["" for i in range(new_data.shape[0])]
    new_data = new_data.merge(data1[["Filename", 'locked/unlocked']], "left").fillna("")
    for index in range(new_data.shape[0]):
        if new_data.loc[index, "Filename"] in locked_files:
            print(data1[ data1['Filename'] == new_data.loc[index, "Filename"]]['Size'].values[0])
            new_data.loc[index, 'Size'] = data1[ data1['Filename'] == new_data.loc[index, "Filename"]]['Size'].values[0]
            new_data.loc[index, 'Date modified'] = data1[ data1['Filename'] == new_data.loc[index, "Filename"]]['Date modified'].values[0]

    return new_data


def append(server1data, server2data): # Function to append data from both the servers
    t = server1data.merge(server2data, 'outer', on='Filename')
    t = t.replace(np.NaN, 0)
    final_data=pd.DataFrame(columns=['Filename','Size','Date modified'])
    for values in t[['Date modified_x', 'Filename' , 'Size(KB)_x', 'Date modified_y', 'Size(KB)_y']].values:
        row_dict = {"Filename": values[1]}

        if values[0] == 0:
            row_dict['Date modified'] = values[3]
            row_dict['Size'] = values[4]

        elif values[3] == 0:
            row_dict['Date modified'] = values[0]
            row_dict['Size'] = values[2]

        elif datetime.datetime.strptime(values[0], '%c') > datetime.datetime.strptime(values[3], '%c'):
            row_dict['Date modified'] = values[0]
            row_dict['Size'] = values[2]

        else:
            row_dict['Date modified'] = values[3]
            row_dict['Size'] = values[4]

        final_data = final_data.append(row_dict, ignore_index=True)

    return final_data

def check_queue(q1,q2,q3,lockq,unlockq): # Check queues for the changes made on server A
    servera_data = pd.DataFrame()
    serverb_data = pd.DataFrame()

    while True:
        if not q1.empty() and not q2.empty():
            servera_data = q1.get()
            serverb_data = q2.get()
            combined_data=append(servera_data, serverb_data)
            print("Data is Appended")
            print(combined_data)
            send_data(combined_data)
            q3.put(combined_data)
            break

    while True:
        if not lockq.empty():
            print("lock accessed")
            if "locked/unlocked" not in combined_data.columns:
                combined_data["locked/unlocked"]=["" for i in range(combined_data.shape[0])]

            locked=lockq.get()
            print(locked)
            combined_data['locked/unlocked'] = ["locked" if filenme== locked else value for filenme, value in combined_data[['Filename', 'locked/unlocked']].values]
            q3.put(combined_data)
            print(combined_data)

        if not unlockq.empty():
            print("Unlock Accessed")
            unlocked=unlockq.get()
            print(unlocked)
            combined_data['locked/unlocked'] = ["unlocked" if filenme== unlocked else value for filenme, value in combined_data[['Filename', 'locked/unlocked']].values]
            combined_data_ = append(servera_data, serverb_data)
            combined_data = update(combined_data, combined_data_)
            q3.put(combined_data)
            print(combined_data)

        if not q2.empty():
            print("Modification in ServerB")
            serverb_data = q2.get()
            combined_data_ = append(servera_data, serverb_data)
            print("Appended Data")
            # print(combined_data_)
            send_data(combined_data_)
            combined_data = update(combined_data, combined_data_)
            print(combined_data)
            q3.put(combined_data)

        if not q1.empty():
            print("Modification in ServerA")
            servera_data = q1.get()
            combined_data_ = append(servera_data, serverb_data)
            print("Appended Data")
            #print(combined_data_)
            send_data(combined_data_)
            combined_data = update(combined_data, combined_data_)
            print(combined_data)
            q3.put(combined_data)

t1=threading.Thread(target=check_modification, args=(serverA_que,)) # Thread to check the modifications part in Server A
t1.start()

t2=threading.Thread(target=serverB_Files, args=(serverB_que,)) # Thread to check with the data received from Server B
t2.start()

t3=threading.Thread(target=check_queue, args=(serverA_que, serverB_que, client_que, lock_que, unlock_que,)) # Thread to check with the data consistency part in both the servers
t3.start()


while True:
    sock, Address=sock1.accept() # Accepts Client request
    print(Address)
    counter = 0

    while True:
        Filename_=str(sock.recv(1024).decode('utf-8')) # Receives the filename from Client
        input_cmnds=Filename_.strip().split()
        if len(input_cmnds)==1:
            while client_que.empty()==False: # Checking with the queue for latest updated data
                overall_data=client_que.get()
                data = pickle.dumps(overall_data)
            sock.sendall(data) #Sending the data to client
        else:
            if input_cmnds[1]=="lock":
                lock_filename=overall_data.iloc[int(input_cmnds[2])]["Filename"]
                lock_que.put(lock_filename)
                print(client_que.qsize())
                while client_que.empty():
                    counter+=1

                while client_que.empty()==False: # Checking with the queue for latest updated data in server B
                    overall_data = client_que.get()
                    data = pickle.dumps(overall_data)

                sock.sendall(data)

            elif input_cmnds[1]=="unlock":
                unlock_filename = overall_data.iloc[int(input_cmnds[2])]["Filename"]
                unlock_que.put(unlock_filename)
                while client_que.empty():
                    counter+=1

                while client_que.empty()==False: # Checking with the queue for latest updated data in server B
                    overall_data = client_que.get()
                    data = pickle.dumps(overall_data)

                sock.sendall(data)



sock.close()
sock1.close()
