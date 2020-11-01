#!/usr/bin/env python
import socket
import subprocess
import sys
import ipaddress
from datetime import datetime

# PYTHON SCANNER USAGE
# Python Port Scanner
# You can run this with 0 arguments and specify 1 host to scan 
# with either hostname or IP address of host.
# ex: python3 ps.py

# For scanning a range of hosts on a given subnet. 2 examples
# CIDR
# ex: python3 ps.py 8.8.8.0/24 
# IP address must end in 0 for CIDR range to work properly

# Range of IPs
# ex: python3 ps.py 192.168.1.5 192.168.1.8
# Scans hosts
# 192.168.1.5
# 192.168.1.6
# 192.168.1.7
# 192.168.1.8

# Port Specification
# When prompted a port you can scan a single or multiple ports
# Single port
# ex: 22

# Multiple ports (spaces don't matter, must be comma separated)
# ex: 22,80,443,445


# Clear the screen
subprocess.call('clear', shell=True)

remoteServer = ""
remoteServerIP = ""
ip_range = []

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

if len(sys.argv) == 1:
	# Ask for input
	remoteServer = input("Enter a remote host to scan: ")
	ip_range.append(socket.gethostbyname(remoteServer))

elif len(sys.argv) == 2:
	if "/" in sys.argv[1]:
		ip_range = [str(i) for i in ipaddress.IPv4Network(sys.argv[1])]
	else:
		ip_range.append(socket.gethostbyname(sys.argv[1]))

elif len(sys.argv) == 3:
	ip_range = ipRange(sys.argv[1], sys.argv[2])

# Check what time the scan started
t1 = datetime.now()

port_range = input("Enter a port or range of ports to scan: ")
port_range = [int(port) for port in port_range.split(",")]

# Some error handling for catching errors

try:
	for remoteServerIP in ip_range:
		# Print a nice banner with information on which host we are about to scan
		print("-" * 60)
		print("Please wait, scanning remote host", remoteServerIP)
		print("-" * 60)
		for port in port_range:  
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((remoteServerIP, port))
			if result == 0:
				print("Port {}: 	 Open".format(port))
			else: 
				print("Port {}: 	 Closed".format(port))
			sock.close()
			# print(f"Port {port} scanning...")

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


# Sources
# https://tkit.dev/2011/09/11/how-to-generate-an-ip-range-list-in-python/
# https://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python