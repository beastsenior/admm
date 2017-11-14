import socket
import pymysql
import os
import time

import net_interface as ni


pid = os.fork()
if pid==0:
	print('Bridge is running: (pid=%d, time=%s)'%(os.getpid(), time.time()))
	b_ser = ni.init_socket('bridge')

	b_ser.close()	
	print('Bridge has done.(%s)'%time.time())
	
else:
	print('Worker is running: (pid=%d, time=%s)'%(os.getpid(), time.time()))
	w_ser = ni.init_socket('worker')

	w_ser.close()
	print('Worker has done. (%s)'%time.time())
	
