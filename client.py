# Student Name: Shivani Panchiwala
# Student ID: 1001982478

import socket
import pickle


sock=socket.socket() # Create a socket object
sock.connect(("127.0.0.5",5067)) # Connect with Server A

data="Temp"

while True:
    Filename = input("Enter server lock or unlock index: ")  #Input from User
    sock.sendall(Filename.encode('utf-8')) # Sharing the Filename which is received from User to the Server A
    data=sock.recv(4096) # Data is received from Server A
    decodeData=pickle.loads(data) # Unpickling the data received from Server A
    print("Data is Appended")  # Print Append data
    print(decodeData) # Printing the Appended data which is shared by Server A


sock.close()  # Close the Client