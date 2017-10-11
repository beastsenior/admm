#node as server (worker)
import userdefine as ni
import topology as to
import admm as ad

import socket
import os
import struct
import time
import random

local_ip = (ni.get_local_ip('eth1'), ni.PORT)  
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
ser.bind(local_ip)  

r_msg={}

Xk = random.random()
Xk1 = 0
Yk = {}
Yk_1 = {}
Zk = {}

for addr in to.IPLIST:
	Yk[addr] = 0
	Yk_1[addr] = random.random()

active_bridge, num_active_bridge  = to.get_active_bridge()

while True:  
	num_r_msg = 0  #number of received massage
	r_msg_tmp, addr = ser.recvfrom(1024)  
	if r_msg_tmp == to.PMD:  #when some bridge leave, it will send a massage (PMD) to its worker  
		active_bridge.remove(addr)
		num_active_bridge = num_active_bridge - 1
	else:
		r_msg[addr] = r_msg_tmp
		if addr in active_bridge:
			num_r_msg = num_r_msg + 1
			if num_r_msg == num_active_bridge:
				for addr in active_bridge:
					Zk[addr] = struct.unpack('d', r_msg[addr])
					Yk[addr] = admm.get_Yk(Xk, Yk_1[addr], Zk[addr])
				Xk1 = admm.get_Xk1(Xk, Yk, Zk, active_bridge, num_active_bridge)
				for addr in active_bridge:
					s_msg = struct.pack('dd',Xk1, Yk[addr])
					ser.sendto(s_msg, addr)
				Xk=Xk1
				Yk_1=Yk.copy()
		else:   #when new bridge join
			active_bridge.append(addr)
			num_active_bridge = num_active_bridge + 1
			num_r_msg = num_r_msg + 1
ser.close()  