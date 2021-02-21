# Experimental Feature
# Connect to the SUIS Targets via TCP Socket
# Obtain data and output to user friendly format.
import socket
import re

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 4000       # The port used by the server

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def closesocketconnection():
    sock.close()

# Receive and sort target data

while True:
    #fixme correct decoding upon reconnection
    data = sock.recv(300)
    decoded = data.rstrip()
    decoded = data.decode('utf-8')


    if '_NAME;' in decoded:
        decodedname = (decoded[14:40])
        decodedname = re.sub(r'0;', '', decodedname)
        decodedname = list(decodedname.split("  "))

    # Get Start Numbers
    if '_SHOT;' in decoded:
        startnumber = (decoded[8:10])
        startnumber = re.sub(r';', '', startnumber)
        startnumber = list(startnumber.split("  "))
        rawstartnumber = (decoded[8:10])
        rawstartnumber = re.sub(r';', '', rawstartnumber)



    # Get 10 Shot Subtotal (Decimal)
    if '_SUBT;' in decoded:
        #Convert startnumber from str to int
        intstartnumber = int(rawstartnumber)

        if intstartnumber >= 10:

            subtotal = (decoded[38:44])
            subtotal = re.sub(r';:', '', subtotal)
            subtotal = list(subtotal.split("  "))
            print(subtotal)

        else:

            subtotal = (decoded[37:42])
            subtotal = re.sub(r';', '', subtotal)
            subtotal = list(subtotal.split("  "))
            print(subtotal)

    # Get Total Score from 60 shot match
    # If the _TOTL frame is less than a certain length , get the 60 shot score.

    if '_TOTL;' in decoded:

        x600framelength = len(decoded)

        integerscoretotal = (decoded[36:39])
        integerscoretotal = re.sub(r';', '', integerscoretotal)
        integerscoretotal = list(integerscoretotal.split("  "))
        print(integerscoretotal)








