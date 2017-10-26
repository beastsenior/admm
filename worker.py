#node as server (worker)
import net_interface as ni
import topology as to
import admm as ad

import socket
import struct
import time
import random
import pymysql
import numpy as np

#creat socket
local_addr = (ni.LOCAL_IP, ni.PORT)  
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
ser.bind(local_addr)  

#connect to mysql
conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
cursor = conn.cursor()

r_msg={} #received massage
num_r_msg = 0  #number of received massage

#X target and data A, b
X_target, A, b = ad.lasso_data_generator()

#receive Zk
#own Xk and Uk_1
#compute Xk1 and Uk 
Xk = np.random.random(ad.DD)
Xk1 = np.zeros(ad.DD)
Uk = {}
Uk_1 = {}
Zk = {}  

active_bridge = []
num_active_bridge = 0

while True:  
	print('\n', end='\r', flush=True)
	print('-----------------------X_target vs. Xk-----------------------')
	print(X_target)
	print(Xk)
	print('-------------------------------------------------------------')
	#get adjacency matrix of the network
	adjacency_matrix = to.load_topology(conn, cursor)
	print('number of active bridge:', num_active_bridge)
	#receiving poll
	r_msg_tmp, addr = ser.recvfrom(ad.DD*Xk.itemsize)  

	if r_msg_tmp == to.PMD:  #when some bridge leave, it will send a massage (PMD) to its worker  
		if addr not in active_bridge:
			print('EEEEEEEEEEEEEEEEEEEEEEEError_______________PMD msg <- ', addr)
			time.sleep(5000)
		print('---------------------bridge sleeps:', active_bridge, '-', addr) #addr bridge leave (sleep)
		active_bridge.remove(addr)
		Uk.pop(addr) 
		Uk_1.pop(addr)
		num_active_bridge = num_active_bridge - 1
	else:
		r_msg[addr] = r_msg_tmp
		if addr not in active_bridge:  #when new bridge join
			print('+++++++++++++++++++birdge wakes:', active_bridge, '+', addr) #addr join as a new bridge (wake)
			active_bridge.append(addr)
			Uk[addr] = np.zeros(ad.DD)
			Uk_1[addr] = np.random.random(ad.DD)
			num_active_bridge = num_active_bridge + 1
		num_r_msg = num_r_msg + 1
		print('A massage from', addr, '... (', num_r_msg, '/', num_active_bridge, ')')
	#when get all data to compute
	if num_r_msg == num_active_bridge:
		net_delay = to.max_delay(adjacency_matrix, active_bridge)
		time.sleep(net_delay) #simulate network delay, before compute the data
		#print('network delay: ', net_delay)
		for addr in active_bridge:
			Zk[addr] = np.array(struct.unpack('%ud'%ad.DD, r_msg[addr]))
			#print('Receive: Zk <--', addr)
			#print('Zk[addr]=', Zk[addr])
			Uk[addr] = ad.get_Uk(Xk, Uk_1[addr], Zk[addr])
		Xk1 = ad.get_Xk1(A, b, Uk, Zk, active_bridge, num_active_bridge)
		for addr in active_bridge:
			s_msg = struct.pack('%ud'%ad.DD,*(Xk1+Uk[addr]))
			ser.sendto(s_msg, addr)
			#print ('Send:', '(Xk1+Uk)=', Xk1, '+', Uk[addr], '-->', addr)
		Xk=Xk1
		Uk_1=Uk.copy()
		num_r_msg = 0
cursor.close()
conn.close()
ser.close()  