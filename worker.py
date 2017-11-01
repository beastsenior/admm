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

try:
	#creat socket
	local_addr = (ni.LOCAL_IP, ni.PORT)  
	ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	ser.bind(local_addr)  

	#connect to mysql
	conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
	cursor = conn.cursor()

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

	r_msg={} #received massage
	active_bridge = []  
	num_active_bridge = 0
	received_active_bridge = []  #received active bridge
	num_received_active_bridge = 0  #number of received active bridge

	I = 0 #number of iteration
	while True:  
		if I % 1000 == 0:
			print('\n\n')
			print(I)
			#get adjacency matrix of the network
			#print(I,1)
			adjacency_matrix = to.load_topology(conn, cursor)
			print('active bridge:', active_bridge)
			print('-----------------------Xk-----------------------\n', Xk)

		#receiving poll
		#print(I,2)
		#print('num_received_active_bridge=', num_received_active_bridge)
		r_msg_tmp, addr = ser.recvfrom(ad.DD*Xk.itemsize)  
		#print(I,2.5)
		
		if r_msg_tmp == to.PMD:  #when some bridge leave, it will send a massage (PMD) to its worker  
			if addr not in active_bridge:
				print('Error PMD msg. <- ', addr)
				input()
			print('---------------------bridge sleeps:', active_bridge, '-', addr) #addr bridge leave (sleep)
			print('num_active_bridge=', num_active_bridge)
			active_bridge.remove(addr)
			Uk.pop(addr) 
			Uk_1.pop(addr)
			num_active_bridge = num_active_bridge - 1
			if addr in received_active_bridge:
				received_active_bridge.remove(addr)
				num_received_active_bridge = num_received_active_bridge - 1
		else:
			if addr not in active_bridge:  #when new bridge join
				print('+++++++++++++++++++birdge wakes:', active_bridge, '+', addr) #addr join as a new bridge (wake)
				print('num_active_bridge=', num_active_bridge)
				active_bridge.append(addr)
				Uk[addr] = np.zeros(ad.DD)
				Uk_1[addr] = np.random.random(ad.DD)
				num_active_bridge = num_active_bridge + 1
				received_active_bridge.append(addr)
				num_received_active_bridge = num_received_active_bridge + 1
			else:
				if addr not in received_active_bridge:
					received_active_bridge.append(addr)
					num_received_active_bridge = num_received_active_bridge + 1
				else:
					print('Error: got msg from same node twice. <- ', addr)
					input()
			r_msg[addr] = r_msg_tmp
			#print('A massage from', addr, '... (', num_received_active_bridge, '/', num_active_bridge, ')')
			Zk[addr] = np.array(struct.unpack('%ud'%ad.DD, r_msg[addr]))

			#print('Receive: Zk <--', addr)      ############
			#print('Zk[addr]=', Zk[addr])         #############
			#print('active bridge:', active_bridge)    #############

			#print('received active bridge:', received_active_bridge)
		#when get all data to compute
		if num_received_active_bridge == num_active_bridge:
			net_delay = to.max_delay(adjacency_matrix, received_active_bridge)
			time.sleep(net_delay) #simulate network delay, before compute the data
			#print('network delay: ', net_delay)
			for addr in received_active_bridge:
				#print(I,3)
				Zk[addr] = np.array(struct.unpack('%ud'%ad.DD, r_msg[addr]))
				#print('Receive: Zk <--', addr)
				#print('Zk[addr]=', Zk[addr])
				#print(I,4)
				Uk[addr] = ad.get_Uk(Xk, Uk_1[addr], Zk[addr])
			#print(I,5)
			Xk1 = ad.get_Xk1(A, b, Uk, Zk, received_active_bridge, num_received_active_bridge)
			for addr in received_active_bridge:
				#print(I,6)
				s_msg = struct.pack('%ud'%ad.DD,*(Xk1+Uk[addr]))
				#print(I,7)
				ser.sendto(s_msg, addr)
				#print ('Send:', '(Xk1+Uk)=', Xk1+Uk[addr], '-->', addr)
				#print ('Send:', '(Xk1+Uk)', '-->', addr)
			Xk=Xk1
			Uk_1=Uk.copy()
			received_active_bridge = []
			num_received_active_bridge = 0
		I = I + 1
finally:
	#print(8)
	cursor.close()
	conn.close()
	ser.close()  
