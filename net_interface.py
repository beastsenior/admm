import netifaces
import socket

import globle as g

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
	elif role == 'admin':
		ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	else:
		print('Error: wrong role.')
		input()
	return ser

#local ip
LOCAL_IP = get_local_ip('eth1')