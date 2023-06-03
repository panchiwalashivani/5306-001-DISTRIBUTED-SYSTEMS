# lab2_panchiwala_smp2478
# UTA ID: 1001982478
# Name: Shivani Manojkumar Panchiwala
# Completion Date: 10/31/2021

import os
import socketserver
from helper import helper


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        dir_name = 'C:\\Users\\pshiv\\PycharmProjects\\lab#_panchiwala_smp2478\\SP'  # Path of the folder
        arr = os.listdir(dir_name)  # list out the files from directory
        help = helper()
        sending = help.getFilesWithMetadata(dir_name, arr)
        #print(sending)
        self.request.send(str(sending).encode()) # send the data


if __name__ == "__main__":
    HOST, PORT = "localhost", 5025  # bind host address and port together and connect to the client
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
