import netifaces

import globle as g

#local ip
LOCAL_IP = get_local_ip('eth1')

#get host ip address
def get_local_ip(interface_name): 
	info = netifaces.ifaddresses(interface_name) 
	return info[netifaces.AF_INET][0]['addr']

#init socket
def init_socket(role):
	if role == 'bridge':
		local_addr = (LOCAL_IP, g.BPORT)  
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ser.bind(local_addr)
	elif role == 'worker':
		local_addr = (LOCAL_IP, g.WPORT)  
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ser.bind(local_addr)
	else:
		print('Error: wrong role.')
		input()
	return ser