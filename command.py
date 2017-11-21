import net_interface as ni
import globle as g
import numpy as np

def init_bridge(l_bridge,mode_i):
	ser = ni.init_socket('admin')
	for ip in l_bridge:
		ser.sendto(np.int8(mode_i).tostring(),(ip,g.BPORT))
	ready_ip = []
	while(set(ready_ip)!=set(l_bridge)):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		r_command = int(np.fromstring(r_msg,dtype=np.int8))
		if r_command == g.D_COMMAND['bridge ready']:
			ready_ip.append(addr[0])
	ser.close()
	print('All bridges are ready.')
	
def init_worker(l_worker,mode_i):
	ser = ni.init_socket('admin')
	for ip in l_worker:
		ser.sendto(np.int8(mode_i).tostring(),(ip,g.WPORT))
	ready_ip = []
	while(set(ready_ip)!=set(l_worker)):
		r_msg, addr = ser.recvfrom(g.BUFSIZE)
		r_command = int(np.fromstring(r_msg,dtype=np.int8))
		if r_command == g.D_COMMAND['worker ready']:
			ready_ip.append(addr[0])
	ser.close()
	print('All workers are ready.')
	
def start_bridge(l_bridge):
	ser = ni.init_socket('admin')
	for ip in l_bridge:
		ser.sendto(np.int8(g.D_COMMAND['bridge start']).tostring(),(ip,g.BPORT))
	ser.close()
	print('Bridges start.')
	