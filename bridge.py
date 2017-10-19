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

#receive Xk1 and Yk
#own Zk
#compute Zk1
Xk1 = {}
Yk = {}
Zk = random.random()
Zk1 = 0

time.sleep(10)

#get the list of active neighbor worker. 
num_active_worker = 0
while num_active_worker == 0:
	active_worker, num_active_worker  = to.get_active_worker(to.load_mask(conn, cursor))  
	time.sleep(2)

while True:
	#send Zk to worker
	s_msg = struct.pack('d',Zk)
	print('\n')
	print('number of active worker:', num_active_worker)
	#time.sleep(3)  
	for addr in active_worker:
		ser.sendto(s_msg, addr)
		print ('Send:', 'Zk=', Zk, '-->', addr)
		
	num_r_msg = 0  #number of received massage
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

	#renew the list of active neighbor worker. 
	#active_worker is active neighbor worker list, eg. [['172.16.100.3',27514],['172.16.100.7',27511]]. 
	#num_active_worker is the number of active neighbor worker
	#list(set(active_worker).difference(set(active_worker_renew)) is (active_worker - active_worker_renew), to find which nodes have left
	active_worker_renew, num_active_worker_renew  = to.get_active_worker(to.load_mask(conn, cursor))  
	for addr in list(set(active_worker).difference(set(active_worker_renew))):
		ser.sendto(to.PMD, addr)		
		print('Send:', '---PMD---', to.PMD, '-->', addr)
	while num_active_worker_renew <= 0:  #if there is no active worker
		time.sleep(2)
		active_worker_renew, num_active_worker_renew  = to.get_active_worker(to.load_mask(conn, cursor)) 
	active_worker, num_active_worker = active_worker_renew, num_active_worker_renew

cursor.close()
conn.close()
ser.close()