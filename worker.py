#node as server (worker)

import userdefine as ud
import socket
import struct
import time

import types #临时

ip=ud.get_ip('eth1')
address = (ip, ud.PORT)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  

num0=0
num1=0
while True:  
	msg, addr = s.recvfrom(1024)  
	
	if not msg:  
		print("client has exist.")  
		break
	else:
		num=struct.unpack('d',msg)
		time.sleep(1)
	
	#print("received:", num, "from", addr)  
	if addr[0]=='172.16.100.2':
		num0=num0+1
	elif addr[0]=='172.16.100.3':
		num1=num1+1
	else:
		print("from error ip")
	
	print("num0:", num0, "num1:", num1, "received:", num, "from", addr)

s.close()  