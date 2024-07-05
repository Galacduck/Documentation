import socket
import time
import math
import random
import serial
#Analog inputs (14, 15, 16, 17, 18, 19) are (814, 869, 937, 996, 1023, 1023)

bufferSize = 1024
#msgFromServer = "Hello Client"
serverPort = 2222
serverIP = '192.168.0.134'
#bytesToSend = msgFromServer.encode('utf-8')
RPIsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPIsocket.bind((serverIP, serverPort))

print("Server listening...")

data = 0
arrServ = []

def readArdu():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 5)
    input_str = ser.readline()

#print("Read input " + input_str.decode("utf-8").strip() + from Arduino")

    while 1:
        ser.write(b'status\n')
        input_str = ser.readline().decode("utf-8").strip()
        if (input_str == ""):
            print(".")
        else:
            reading = int(input_str[19:23])
            return reading

while True:

    cmd, addr = RPIsocket.recvfrom(bufferSize)
    cmd = cmd.decode('utf-8')
    print(cmd)
    print('Client Address: ', addr[0])

    if cmd == "go":
        item = readArdu()
        arrServ.append(item)
        print(arrServ)

    elif cmd == "stop":
        arrServ.append(-1)
        print("hi")
        for i in range(len(arrServ)):
            data = arrServ[i]
            
            msg = str(data)
            msg = msg.encode("utf-8")
            RPIsocket.sendto(msg, addr)