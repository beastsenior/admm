#node as client (bridge)
import net_interface as ni
import topology as to
import admm as ad

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

#receive Xk1 and Yk
#own Zk
#compute Zk1
Xk1 = {}
Yk = {}
Zk = random.random()
Zk1 = 0

time.sleep(10)

while True:
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
		ser.sendto(to.PMD, addr)		
		print('Send:', '---PMD---', to.PMD, '-->', addr)
	old_active_worker = active_worker
	#send Zk to active worker
	s_msg = struct.pack('d',Zk)
	for addr in active_worker:
		ser.sendto(s_msg, addr)
		print ('Send:', 'Zk=', Zk, '-->', addr)
		
	num_r_msg = 0  #number of received massage (massage of Xk1 and Yk)
	while True:
		r_msg_tmp, addr = ser.recvfrom(1024) 
		r_msg[addr] = r_msg_tmp
		if addr in active_worker:
			num_r_msg = num_r_msg + 1
			print('A massage from', addr, '... (', num_r_msg, '/', num_active_worker, ')')
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

cursor.close()
conn.close()
ser.close()