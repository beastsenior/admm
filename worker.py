#node as server (worker)
import net_interface as ni
import topology as to
import admm as ad

import socket
import struct
import time
import random

#creat socket
local_addr = (ni.LOCAL_IP, ni.PORT)  
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
ser.bind(local_addr)  

r_msg={} #received massage
num_r_msg = 0  #number of received massage

#receive Zk
#own Xk and Yk_1
#compute Xk1 and Yk 
Xk = random.random()
Xk1 = 0
Yk = {}
Yk_1 = {}
Zk = {}  

active_bridge, num_active_bridge  = to.get_active_bridge(to.load_mask())
print('active bridge:', active_bridge)

for addr in active_bridge:
	Yk[addr] = 0
	Yk_1[addr] = random.random()

while True:  
	r_msg_tmp, addr = ser.recvfrom(1024)  
	if r_msg_tmp == to.PMD:  #when some bridge leave, it will send a massage (PMD) to its worker  
		if addr not in active_bridge:
			print('EEEEEEEEEEEEEEEEEEEEEEEError_______________PMD msg <- ', addr)
		print('---------------------bridge rest:', active_bridge, '-', addr) #addr bridge leave (rest)
		active_bridge.remove(addr)
		Yk.pop(addr) 
		Yk_1.pop(addr)
		num_active_bridge = num_active_bridge - 1
	else:
		r_msg[addr] = r_msg_tmp
		if addr not in active_bridge:  #when new bridge join
			print('+++++++++++++++++++birdge active:', active_bridge, '+', addr) #addr join as a new bridge (active)
			active_bridge.append(addr)
			Yk[addr] = 0
			Yk_1[addr] = random.random()
			num_active_bridge = num_active_bridge + 1
		num_r_msg = num_r_msg + 1
		print('A massage from', addr, '... (', num_r_msg, '/', num_active_bridge, ')')
		if num_r_msg == num_active_bridge:
			for addr in active_bridge:
				Zk[addr] = (struct.unpack('d', r_msg[addr]))[0]
				print ('Receive:', 'Zk=', Zk[addr], '<--', addr)
				Yk[addr] = ad.get_Yk(Xk, Yk_1[addr], Zk[addr])
			Xk1 = ad.get_Xk1(Xk, Yk, Zk, active_bridge, num_active_bridge)
			for addr in active_bridge:
				s_msg = struct.pack('dd',Xk1, Yk[addr])
				ser.sendto(s_msg, addr)
				print ('Send:', '(Xk1, Yk)=', Xk1, ',', Yk[addr], '-->', addr)
			Xk=Xk1
			Yk_1=Yk.copy()
			num_r_msg = 0
ser.close()  