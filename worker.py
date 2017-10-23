#node as server (worker)
import net_interface as ni
import topology as to
import admm as ad

import socket
import struct
import time
import random
import numpy as np

#creat socket
local_addr = (ni.LOCAL_IP, ni.PORT)  
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
ser.bind(local_addr)  

r_msg={} #received massage
num_r_msg = 0  #number of received massage

#receive Zk
#own Xk and Yk_1
#compute Xk1 and Yk 
Xk = np.random.random([ad.DD])
Xk1 = np.zeros([ad.DD])
Yk = {}
Yk_1 = {}
Zk = {}  

active_bridge = []
num_active_bridge = 0

while True:  
	print('\n')
	print('number of active bridge:', num_active_bridge)
	r_msg_tmp, addr = ser.recvfrom(ad.DD*Xk.itemsize)  
	#print('Xk.itemsize=',Xk.itemsize,'len(r_msg_tmp)=', len(r_msg_tmp), 'r_msg_tmp=', r_msg_tmp);
	if r_msg_tmp == to.PMD:  #when some bridge leave, it will send a massage (PMD) to its worker  
		if addr not in active_bridge:
			print('EEEEEEEEEEEEEEEEEEEEEEEError_______________PMD msg <- ', addr)
			time.sleep(5000)
		print('---------------------bridge sleeps:', active_bridge, '-', addr) #addr bridge leave (sleep)
		active_bridge.remove(addr)
		Yk.pop(addr) 
		Yk_1.pop(addr)
		num_active_bridge = num_active_bridge - 1
	else:
		r_msg[addr] = r_msg_tmp
		if addr not in active_bridge:  #when new bridge join
			print('+++++++++++++++++++birdge wakes:', active_bridge, '+', addr) #addr join as a new bridge (wake)
			active_bridge.append(addr)
			Yk[addr] = np.zeros([ad.DD])
			Yk_1[addr] = np.random.random([ad.DD])
			num_active_bridge = num_active_bridge + 1
		num_r_msg = num_r_msg + 1
		print('A massage from', addr, '... (', num_r_msg, '/', num_active_bridge, ')')
	if num_r_msg == num_active_bridge:
		for addr in active_bridge:
			Zk[addr] = np.array(struct.unpack('%ud'%ad.DD, r_msg[addr]))
			#print ('Receive:', 'Zk=', Zk[addr], '<--', addr)
			print('Receive: Zk <--', addr)
			print('Zk[addr]=', Zk[addr])
			Yk[addr] = ad.get_Yk(Xk, Yk_1[addr], Zk[addr])
		Xk1 = ad.get_Xk1(Xk, Yk, Zk, active_bridge, num_active_bridge)
		for addr in active_bridge:
			s_msg = struct.pack('%ud'%ad.DD*2,*Xk1,*(Yk[addr]))
			ser.sendto(s_msg, addr)
			print ('Send:', '(Xk1, Yk)=', Xk1, ',', Yk[addr], '-->', addr)
		Xk=Xk1
		Yk_1=Yk.copy()
		num_r_msg = 0
ser.close()  