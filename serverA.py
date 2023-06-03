# lab2_panchiwala_smp2478
# UTA ID: 1001982478
# Name: Shivani Manojkumar Panchiwala
# Completion Date: 10/31/2021


import os   # import the module for os
import os.path # import the module for os.path
import socketserver # import module for socketserver
import time   # import time module
from datetime import datetime   # import datetime module
from socket import *  # import socket module
import tqdm  # import tqdm module

from helper import helper   # import helper from helper.py file
import ast


class MyTCPHandlerServerSync(socketserver.BaseRequestHandler):     # class for serversync handler
    def doSync(self):                   # function for sync the files
        while True:
            dir_name = 'C:\\Users\\pshiv\\PycharmProjects\\lab#_panchiwala_smp2478\\MP'  # path of the folder
            arr = os.listdir(dir_name)  # list out the files from directory
            help = helper()    # helper file reference
            serverAFiles = help.getFilesWithMetadata(dir_name, arr)    # call the function from help for get file with metadata to server A
            #serverAFiles = eval(data.decode("utf-8"))
            #print(serverAFiles) Server A files with metadata
            sock2 = socket(AF_INET, SOCK_STREAM)  # Build Socket Object
            sock2.connect(('localhost', 5025))  # bind host address and port together and connect to the server B
            data = sock2.recv(4096)    # receive the files and buffer size is 4096
            #print(data) server B files with metadata
            serverBFiles = eval(data.decode("utf-8"))  # read the file
            serverBPath = serverBFiles[1][3]
            #print(serverBPath) server B path
            serverAPath = dir_name
            FilesToCopyB = list(map(lambda y: serverAPath + '\\' + y, list(                 # copy the file from server B to A using Lambda function
                set(list(map(lambda x: x[0], serverAFiles))) - set(list(map(lambda x: x[0], serverBFiles))))))
            #print(FilesToCopyB) print b and d files
            FilesToCopyA = list(map(lambda y: serverBPath + '\\' + y, list(                 # copy the file from server A to B using Lambda function
                set(list(map(lambda x: x[0], serverBFiles))) - set(list(map(lambda x: x[0], serverAFiles))))))
            FilesCommonInBoth = [x for x in list(map(lambda x: x[0], serverAFiles)) if      # find the common files from both server
                                 x in list(map(lambda x: x[0], serverBFiles))]

            latestCommonFiles = []
            for i in FilesCommonInBoth:
                name1, size1, date1, path1 = list(filter(lambda x: x[0] in FilesCommonInBoth, serverAFiles))[0]     # filter and list out the common files from serevr A
                name2, size2, date2, path2 = list(filter(lambda x: x[0] in FilesCommonInBoth, serverBFiles))[0]     # filter and list out the common files from serevr B
                dt1 = datetime.strptime(date1, '%m/%d/%Y')     # Convert timestring to datetime object
                time.mktime(dt1.timetuple()) * 1000    #Multiply the timestamp of the datetime object by 1000 to convert it to milliseconds
                dt2 = datetime.strptime(date2, '%m/%d/%Y')     # Convert timestring to datetime object
                time.mktime(dt2.timetuple()) * 1000   #Multiply the timestamp of the datetime object by 1000 to convert it to milliseconds
                if (dt1 > dt2):
                    latestCommonFiles.append(path1 + "\\" + name1)     # append the latest common files path1 to name1
                else:
                    latestCommonFiles.append(path2 + "\\" + name2)  # append the latest common files path2 to name2
            ############### FilesToCopyB , FilesToCopyA, latestCommonFiles ################
            if (len(latestCommonFiles) > 0):   # Found changes in following files
                self.request.send(str("Found changes in following files ... ").encode())
                self.request.send(str(latestCommonFiles).encode())
            if (len(FilesToCopyB) > 0):    # Adding following files to serverB
                self.request.send(str("\nAdding following files to serverB ... ").encode())
                self.request.send(str(FilesToCopyB).encode())
            if (len(FilesToCopyA) > 0):    # Adding following files to serverA
                self.request.send(str("\nAdding following files to serverA ... ").encode())
                self.request.send(str(FilesToCopyA).encode())
            time.sleep(3)

    def filetransfer(self):
        merge_files = (FilesToCopyA, FilesToCopyB, latestCommonFiles)   # Merge all the files
        filesize = os.path.getsize(merge_files)           # get the files size
        # send the filename and filesize
        sock2.send(f"{merge_files}{SEPARATOR}{filesize}".encode())
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {merge_files}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(merge_files, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                sock2.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))


    def doList(self):
        dir_name = 'C:\\Users\\pshiv\\PycharmProjects\\lab#_panchiwala_smp2478\\MP'  # path of the folder
        arr = os.listdir(dir_name)  # list out the files from directory
        help = helper()
        serverAFiles = help.getFilesWithMetadata(dir_name, arr)  # get filename and directory from helper.py
        self.request.send(str("\nList of files ... ").encode())   # send and print List of files statment
        self.request.send(str(serverAFiles).encode())    # encode the server A files

    def handle(self):   
        self.doList()
        self.doSync()
        self.filetransfer()


if __name__ == "__main__":
    HOST, PORT = "localhost", 5009     # # bind host address and port together and connect to the client
    serverSync = socketserver.TCPServer((HOST, PORT),
                                        MyTCPHandlerServerSync)  # run in thread(if any change happens call another function to send client)
serverSync.serve_forever()
