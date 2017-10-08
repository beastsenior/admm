#node as server (worker)

import userdefine as ud
import socket
import os
import struct
import time

ip = ud.get_ip('eth1')
address = (ip, ud.PORT)  
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
ser.bind(address)  

while True:  
	msg, addr = ser.recvfrom(1024)  
	
	pid = os.fork() #进入多进程处理
	if pid==0:      #子进程，pid=0
		ser.close()
		if not msg:  
			print("client has exist.")  
			break
		else:
			num=struct.unpack('d',msg)
		print("pid:", pid, "received:", num, "from", addr)
		os._exit(0)
	else:           #父进程，此时pid=子进程进程号
		continue

ser.close()  