import netifaces

#-------funtion--------
#get host ip address
def get_local_ip(interface_name): 
	info = netifaces.ifaddresses(interface_name) 
	return info[netifaces.AF_INET][0]['addr']

#-------variable-------
#local ip
LOCAL_IP = get_local_ip('eth1')
#port of server
PORT=31500  
#port of client
OUTPORT=21500

