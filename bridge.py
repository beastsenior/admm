#node as client (bridge)
import net_interface as ni
import topology as to
import admm as ad

import socket
import struct
import time
import random

ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

r_msg={}
num_err_r_msg = 0  #number of error received massage

Zk = random.random()
Zk1 = 0

while True:
	active_worker, num_active_worker  = to.get_active_worker()  #renew the list of active neighbor worker. active_worker is active neighbor worker list, eg. [['172.16.100.3',27514],['172.16.100.7',27511]]. num_active_worker is the number of active neighbor worker
	s_msg = struct.pack('d',Zk)
	time.delay(2)  
	for addr in active_worker:
		ser.sendto(s_msg, addr)
		print ('Send:', 'Zk=', Zk, ' --> ', addr)
		
	num_r_msg = 0  #number of received massage
	while True:
		r_msg_tmp, addr = ser.recvfrom(1024) 
		r_msg[addr] = r_msg_tmp
		print ('Receive:', '(Xk1, Yk)=', r_msg[addr], ' <-- ', addr)
		print ('\n')
		if addr in active_worker:
			num_r_msg = num_r_msg + 1
			if num_r_msg == num_active_worker:
				for addr in active_worker:
					Xk1[addr], Yk[addr] = struct.unpack('dd',r_msg[addr])			
				Zk1 = admm.get_Zk1(Xk1, Yk, active_worker, num_active_worker)
				Zk = Zk1
		else:
			num_err_r_msg = num_err_r_msg + 1
			print (num_err_r_msg, ' EEEEEEEEEEEEEEEEEEEEEEEError_______________msg <- ', addr) 
ser.close()