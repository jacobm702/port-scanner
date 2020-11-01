#!/usr/bin/env python
import socket
import subprocess
import sys
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

remoteServer = ""
remoteServerIP = ""
ip_range = []

#Sys Args for defining a host
if len(sys.argv) == 2:
    remoteServerIP = socket.gethostbyname(sys.argv[1])
    print ("2 args")

elif len(sys.argv) == 3:
    print("3 args")
    start_ip = sys.argv[1]
    end_ip = sys.argv[2]

    def ipRange(start_ip, end_ip):
        start = list(map(int, start_ip.split(".")))
        end = list(map(int, end_ip.split(".")))
        temp = start
        ip_range = []
        ip_range.append(start_ip)
        while temp != end:
            start[3] += 1
            for i in (3, 2, 1):
                if temp[i] == 256:
                    temp[i] = 0
                    temp[i-1] += 1
            ip_range.append(".".join(map(str, temp)))
        return ip_range

    ip_range = ipRange(start_ip, end_ip)

else:
    # Ask for input
    remoteServer = input("Enter a remote host to scan: ")
    remoteServerIP = socket.gethostbyname(remoteServer)

# Print a nice banner with information on which host we are about to scan
    print("-" * 60)
    print("Please wait, scanning remote host", remoteServerIP)
    print("-" * 60)

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)

# We also put in some error handling for catching errors

for remoteServerIP in ip_range:
    try:
        for port in range(1,1025): 
            print(port) 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print("Port {}: 	 Open".format(port))
        sock.close()

    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

# Checking the time again
t2 = datetime.now()

# Calculates the difference of time, to see how long it took to run the script
total =  t2 - t1

# Printing the information to screen
print('Scanning Completed in: ', total)
