
import netifaces
import struct
import sys

#-------variable-------

#port of server
PORT=31500  

#max doulbe number in packed type
PMD = struct.pack('d', sys.float_info.max)

#-------funtion--------

#get host ip address
def get_local_ip(interface_name): 
	info = netifaces.ifaddresses(interface_name) 
	return info[netifaces.AF_INET][0]['addr']
