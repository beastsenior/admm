import os
import time
import numpy as np

import net_interface as ni
import database as db
import globle as g


pid = os.fork()
if pid==0:
	print('%s Bridge is running: (pid=%d, time=%s)'%(ni.LOCAL_IP, os.getpid(), time.time()))
	ser = ni.init_socket('bridge')
	mode_i = -1
	while(True):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		if addr[0]==g.IP_ADMIN:
			r_command = int(np.fromstring(r_msg,dtype=np.int8))
			if r_command >= 0:
				#reset mode
				mode_i = r_command
				#reset socket
				ser.close()	
				ser = ni.init_socket('bridge')
				
				ser.sendto(np.int8(g.D_COMMAND['bridge ready']).tostring(),addr)
				print('Bridge: Init completed. Mode changed to', str(g.L_MODE[mode_i]))
			elif r_command == g.D_COMMAND['bridge start']:
				print('Brideg: Received command: bridge start')

	ser.close()	
	print('Bridge has done.(%s)'%time.time())
	
else:
	print('%s Worker is running: (pid=%d, time=%s)'%(ni.LOCAL_IP, os.getpid(), time.time()))
	ser = ni.init_socket('worker')
	mode_i = -1
	while(True):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		if addr[0]==g.IP_ADMIN:
			r_command = int(np.fromstring(r_msg,dtype=np.int8))
			if r_command >= 0:
				#reset socket
				ser.close()	
				#reset mode
				mode_i = r_command
				if g.L_MODE[mode_i][0] == 'Lasso':
					if g.L_MODE[mode_i][1] == 'StarADMM' or g.L_MODE[mode_i][1] == 'BridgeADMM':
						A, b = db.load(['A','b'], mode_i, ip=ni.LOCAL_IP)
				
				ser = ni.init_socket('worker')				
				ser.sendto(np.int8(g.D_COMMAND['worker ready']).tostring(),addr)

				print('Worker: Init completed. Mode changed to', str(g.L_MODE[mode_i]))
		#else:
		
	
	ser.close()
	print('Worker has done. (%s)'%time.time())
	
