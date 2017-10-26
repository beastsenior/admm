#node as client (bridge)
import net_interface as ni
import topology as to
import admm as ad
import numpy as np

import socket
import pymysql
import struct
import time
import random

#creat socket
local_addr = (ni.LOCAL_IP, ni.OUTPORT)  
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ser.bind(local_addr)  

#connect to mysql
conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
cursor = conn.cursor()

r_msg={}  #received massage
num_err_r_msg = 0  #number of error received massage
num_active_worker = 0 #number of active neighbor worker. 
old_active_worker = [] #list of active workers on last polling

#receive Xk1 and Uk
#own Zk
#compute Zk1
Xk1 = {}
Uk = {}
Xk1_and_Uk = {}  #Xk1+Uk
Zk = np.random.random(ad.DD)
Zk1 = np.zeros(ad.DD) 

time.sleep(6)

while True:
	#get adjacency matrix of the network
	adjacency_matrix = to.load_topology(conn, cursor)
	#poll mask, get the list of active worker. 
	active_worker, num_active_worker = to.get_active_worker(to.load_mask(conn, cursor))  
	if num_active_worker == 0:
		while num_active_worker == 0:	
			time.sleep(2)
			active_worker, num_active_worker = to.get_active_worker(to.load_mask(conn, cursor)) 		
	print('\n')
	print('number of active worker:', num_active_worker)

	#send PMD to nodes, which have left
	for addr in list(set(old_active_worker).difference(set(active_worker))):	#list(set(active_worker).difference(set(active_worker_renew)) is (active_worker - active_worker_renew), to find which nodes have left
		ser.sendto(to.PMD, addr)		#send the PMD packet to workers to notice bridge leave
		print('Send:', '---PMD---', to.PMD, '-->', addr) 
	old_active_worker = active_worker
	#send Zk to active worker
	s_msg = struct.pack('%ud'%ad.DD,*Zk)
	print('s_msg=', s_msg)
	for addr in active_worker:
		ser.sendto(s_msg, addr)
		print ('Send:', 'Zk=', Zk, '-->', addr)
		
	num_r_msg = 0  #number of received massage (massage of Xk1 and Uk)
	while True:
		#r_msg_tmp, addr = ser.recvfrom(ad.DD*2*Zk.itemsize) #(len(Xk1[])+len(Uk[]))*sizeof(double)
		r_msg_tmp, addr = ser.recvfrom(ad.DD*Zk.itemsize) #(len(Xk1[]+Uk[])*sizeof(double)
		r_msg[addr] = r_msg_tmp
		if addr in active_worker:
			num_r_msg = num_r_msg + 1
			print('A massage from', addr, '... (', num_r_msg, '/', num_active_worker, ')')
			#when get all data to compute
			if num_r_msg == num_active_worker:
				net_delay = to.max_delay(adjacency_matrix, active_worker)
				time.sleep(net_delay) #simulate network delay, before compute the data
				print('network delay: ', net_delay)
				for addr in active_worker:
					# Xk1_and_Uk_tmp = np.array(struct.unpack('%ud'%(ad.DD*2), r_msg[addr]))
					# Xk1[addr] = Xk1_and_Uk_tmp[:ad.DD]
					# Uk[addr] = Xk1_and_Uk_tmp[ad.DD:]
					Xk1_and_Uk_tmp = np.array(struct.unpack('%ud'%ad.DD, r_msg[addr]))
					Xk1_and_Uk[addr] = Xk1_and_Uk_tmp
					print('Receive: (Xk1+Uk) <--', addr)
					print('Xk1+Uk=', Xk1_and_Uk[addr])
				Zk1 = ad.get_Zk1(Xk1_and_Uk, active_worker, num_active_worker)
				Zk = Zk1
				break
		else:
			num_err_r_msg = num_err_r_msg + 1
			print (num_err_r_msg, ' EEEEEEEEEEEEEEEEEEEEEEEError_______________msg <- ', addr) 
			time.sleep(5000)
cursor.close()
conn.close()
ser.close()