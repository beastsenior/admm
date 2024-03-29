import os
import time
import numpy as np

import net_interface as ni
import database as db
import globle as g
import admm as ad
import topology as tp
import environment as env

print('\n')
env.init_environment('node')
pid = os.fork()

#--------------------------------------------bridge---------------------------------------------
if pid==0:
	print('%s Bridge is running: (pid=%d, time=%s)'%(ni.LOCAL_IP, os.getpid(), time.time()))
	ser = ni.init_socket('bridge')
	mode_i = -1
	k = 0 #iter
	
	while(True):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		if addr[0] == g.IP_ADMIN:  #msg from admin node
			r_command = int(np.fromstring(r_msg,dtype=np.int8))
			if r_command >= 0:  #init and setup with mode_i=r_command
				#1.setup mode
				mode_i = r_command				
				#2.setup topology
				G, = db.load(['G'], mode_i)
				l_ow, now = tp.get_ow(G, ni.LOCAL_IP)  	#l_ow: list of own workers. #now: number of own workers
				l_row = [] #list of received own workers
				nrow = 0 #number of received own workers
				k = 0 
				#3.setup data
				if g.L_MODE[mode_i][1] == 'Lasso':
					z = np.zeros([g.DD,1])   
					xu = {} #x=xu[ip][0],u=xu[ip][1]
					Lmin = np.zeros([g.ITER]) #Lagrangian funtion
					t = np.zeros([g.ITER])  #time
					A={}
					b={}
					for ip in l_ow:
						A[ip],b[ip] = db.load(['A','b'], mode_i, ip)
				else:
					print('Bridge: Error: unknow problem.')
					input()	
				#4.setup socket
				ser.close()	
				ser = ni.init_socket('bridge') 					
				ser.sendto(np.int8(g.D_COMMAND['bridge ready']).tostring(),addr)  
				print('Bridge: mode_i=%d (%s): Init completed.'%(mode_i,str(g.L_MODE[mode_i])))
				print('+++Bridge: worker list:',l_ow)
			elif r_command == g.D_COMMAND['bridge reset']:
				mode_i = -1
				ser.close()	
				ser = ni.init_socket('bridge') 
				ser.sendto(np.int8(g.D_COMMAND['bridge ready']).tostring(),addr)  
				print('Bridge: bridge reset.')	
			elif r_command == g.D_COMMAND['bridge start']:
				if g.L_MODE[mode_i][1] == 'Lasso':			
					for ip in l_ow:
						ser.sendto(z.tostring(),(ip, g.WPORT))
					print('Bridge: mode_i=%d (%s): ADMM is running...'%(mode_i,str(g.L_MODE[mode_i])))
				else:
					print('Bridge: Error: unknow problem.')	
					input()	
		elif (addr[0] in l_ow) and (addr[0] not in l_row):  #msg from own workers
			if mode_i == -1:
				print('Bridge: Error: mode_i == -1')
				input()	
			else:
				if g.L_MODE[mode_i][1] == 'Lasso':
					if g.L_MODE[mode_i][2] == 'StarADMM' or g.L_MODE[mode_i][2] == 'BridgeADMM':				
						if g.L_MODE[mode_i][4] == g.L_TAU[0]:  #tau=1, synchronous
							xu[addr[0]] = np.fromstring(r_msg,dtype=z.dtype).reshape([2,g.DD,1])  
							l_row.append(addr[0])
							nrow+=1
							if nrow == now:
								z = ad.get_z(xu, l_row, nrow)
								Lmin[k] = ad.get_Lmin(xu,z,A,b,l_row)
								if k == 0:
									t0 = time.time()
								t[k] = time.time() - t0
								k+=1
								if k < g.ITER:								
									for ip in l_row:
										ser.sendto(z.tostring(),(ip, g.WPORT))	
									l_row = [] 
									nrow = 0
								else:
									db.save({'Lmin':Lmin,'t':t},mode_i,ni.LOCAL_IP) #save to basedata	
									ser.close()
									ser = ni.init_socket('bridge')
									ser.sendto(np.int8(g.D_COMMAND['bridge ready']).tostring(),(g.IP_ADMIN, g.APORT))  
									print('Bridge: mode_i=%d (%s): Done!'%(mode_i,str(g.L_MODE[mode_i])))									
				else:
					print('Bridge: Error: unknow problem.')
					input()	
		else:
			print('Bridge: Error: addr[0] is out of l_ow, or addr[0] has been in l_row.')
			input()
	
	ser.close()
	print('Bridge: Bridge has done. (%s)'%time.time())  
	
	
#------------------------------------------------worker------------------------------------------------
else:
	print('%s Worker is running: (pid=%d, time=%s)'%(ni.LOCAL_IP, os.getpid(), time.time()))
	ser = ni.init_socket('worker')
	mode_i = -1

	while(True):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		if addr[0]==g.IP_ADMIN:  #msg from admin node
			r_command = int(np.fromstring(r_msg,dtype=np.int8))
			if r_command >= 0: #init and setup with mode_i=r_command
				#1.setup mode
				mode_i = r_command
				#2.setup topology
				G, = db.load(['G'], mode_i)
				l_ob, nob = tp.get_ob(G, ni.LOCAL_IP)  	#l_ob: list of own bridges. nob: number of own bridges
				l_rob = [] #list of received own bridges
				nrob = 0 #number of received own bridges
				k = 0
				#3.setup data
				if g.L_MODE[mode_i][1] == 'Lasso':
					if g.L_MODE[mode_i][2] == 'StarADMM' or g.L_MODE[mode_i][2] == 'BridgeADMM':	
						A, b = db.load(['A','b'], mode_i, ip=ni.LOCAL_IP)
						AtA = A.T.dot(A)
						Atb = A.T.dot(b)
						Q = AtA + nob * g.RHO * np.identity(g.DD)
						Q = np.linalg.inv(Q)						
						x = np.zeros([g.DD,1])
						u = {}
						for ip in l_ob:
							u[ip]=np.zeros([g.DD,1])
						z = {}  
				#4.setup socket
				ser.close()			
				ser = ni.init_socket('worker')
				ser.sendto(np.int8(g.D_COMMAND['worker ready']).tostring(),addr)  
				print('Worker: mode_i=%d (%s): Init completed.'%(mode_i,str(g.L_MODE[mode_i])))
				print('+++Worker: bridge list:',l_ob)
			elif r_command == g.D_COMMAND['worker reset']:
				mode_i = -1
				l_ob = [] 
				nob = 0 
				l_rob = [] 
				nrob =0 
				k = 0
				ser.close()	
				ser = ni.init_socket('worker') 
				ser.sendto(np.int8(g.D_COMMAND['worker ready']).tostring(),addr)  
				print('Worker: worker reset.')				
		elif (addr[0] in l_ob) and (addr[0] not in l_rob):  #msg from own bridges
			if mode_i == -1:
				print('Worker: Error: mode_i == -1')
				input()	
			else:
				if g.L_MODE[mode_i][1] == 'Lasso':
					if g.L_MODE[mode_i][2] == 'StarADMM' or g.L_MODE[mode_i][2] == 'BridgeADMM':				
						if g.L_MODE[mode_i][4] == g.L_TAU[0]:  #tau=1, synchronous
							z[addr[0]] = np.fromstring(r_msg,dtype=x.dtype).reshape([g.DD,1])
							l_rob.append(addr[0])
							nrob += 1
							if nrob == nob:
								x,u,xu = ad.get_xu(x,u,z,l_rob,Q,Atb)
								for ip in l_rob:
									ser.sendto(xu[ip].tostring(),(ip, g.BPORT))	
								l_rob = [] 
								nrob = 0
								k += 1
								print(x)
								print(u)
								print(z)
								if k == g.ITER:
									ser.close()
									ser = ni.init_socket('worker') 
									print('Worker: mode_i=%d (%s): Done!'%(mode_i,str(g.L_MODE[mode_i])))									

				else:
					print('Worker: Error: unknow problem.')
					input()	
		else:
			print('Worker: Error: addr[0] is out of l_ob, or addr[0] has been in l_rob.')
			input()
		
	
	ser.close()
	print('Worker: Worker has done. (%s)'%time.time())
	
