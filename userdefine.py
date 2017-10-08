import netifaces

#-------variable-------

#port of server
PORT=31500  

#-------funtion--------

#get host ip address
def get_ip(interface_name): 
	info = netifaces.ifaddresses(interface_name) 
	return info[netifaces.AF_INET][0]['addr']