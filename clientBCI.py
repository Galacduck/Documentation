import socket
import time
import matplotlib.pyplot as plt
import numpy as num

serverAddress = ('192.168.0.134', 2222)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClient.settimeout(2)  # Set a timeout for blocking socket operations
arr = []

def getData():
    while True:
        try:
            cmd = "go"
            cmd = cmd.encode('utf-8')
            UDPClient.sendto(cmd, serverAddress)
            print("Sent 'go' command to server")
            time.sleep(1)  # Adding a sleep to avoid sending too many requests too quickly
        
        except KeyboardInterrupt:
            print("triggered")
            return

def stopData():
    print("Stopping data collection")
    while True:
        cmd = "stop"
        cmd = cmd.encode('utf-8')
        
        for attempt in range(5):  # Retry sending the 'stop' command up to 5 times
            UDPClient.sendto(cmd, serverAddress)
            print(f"Sent 'stop' command to server, attempt {attempt + 1}")
            time.sleep(0.5)
        
        try:
            data, addr = UDPClient.recvfrom(bufferSize)
            data = data.decode('utf-8')
            print(f"Received data: {data}")

            if data == "ack":
                print("Stop command acknowledged by server")
                break
            
            arr.append(int(data))

            if arr[-1] < 0:
                print("Data stored")
                break
        except socket.timeout:
            print("Timeout waiting for server response, retrying...")

def pltData():
    xvals = list(range(len(arr)))
    yvals = [float(i) for i in arr]

    numpyarr = num.asarray(yvals)
    num.savetxt('data.csv', numpyarr, delimiter=',')
    print("Saved data")

    plt.stem(xvals, yvals)
    plt.show()
    
while True:
    instr = input("Enter your instruction: ")
    if instr == "read":
        getData()
        print("triggered")
    elif instr == "stop":
        stopData()
    elif instr == "plot":
        pltData()
    elif instr == "exit":
        exit()
