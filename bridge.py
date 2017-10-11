#node as client (bridge)
import net_interface as ni
import topology as to
import admm as ad

import socket
import struct
import time
import random

#creat socket
local_addr = (ni.LOCAL_IP, ni.OUTPORT)  
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser.bind(local_addr)  

r_msg={}  #received massage
num_err_r_msg = 0  #number of error received massage

#receive Xk1 and Yk
#own Zk
#compute Zk1
Xk1 = {}
Yk = {}
Zk = random.random()
Zk1 = 0

#creat topology
tmp_to = rand_topology()
for i in IPLIST:
	for j in IPLIST:
		print(i, '-->', j, tmp_to[(i,j)])
time.sleep(10)
save_topology(tmp_to)
adjacency_matrix = load_topology()

while True:
	active_worker, num_active_worker  = to.get_active_worker(adjacency_matrix)  #renew the list of active neighbor worker. active_worker is active neighbor worker list, eg. [['172.16.100.3',27514],['172.16.100.7',27511]]. num_active_worker is the number of active neighbor worker
	s_msg = struct.pack('d',Zk)
	print ('\n')
	#time.sleep(2)  
	for addr in active_worker:
		ser.sendto(s_msg, addr)
		print ('Send:', 'Zk=', Zk, '-->', addr)
		
	num_r_msg = 0  #number of received massage
	while True:
		r_msg_tmp, addr = ser.recvfrom(1024) 
		r_msg[addr] = r_msg_tmp
		if addr in active_worker:
			num_r_msg = num_r_msg + 1
			if num_r_msg == num_active_worker:
				for addr in active_worker:
					(Xk1[addr], Yk[addr]) = (struct.unpack('dd',r_msg[addr]))[0:2]	
					print ('Receive:', '(Xk1, Yk)=', Xk1[addr], ',', Yk[addr], '<--', addr)
				Zk1 = ad.get_Zk1(Xk1, Yk, active_worker, num_active_worker)
				Zk = Zk1
				break
		else:
			num_err_r_msg = num_err_r_msg + 1
			print (num_err_r_msg, ' EEEEEEEEEEEEEEEEEEEEEEEError_______________msg <- ', addr) 
			time.sleep(100)
ser.close()