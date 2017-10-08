#每个worker计算一个S和多个V，每个bridge计算一个SB
#变量包括Sk,   Sk1,    Vk[200], Vk_1[200], SBk,   SBk1
#分别对应S(k), S(k+1), V(k)[b], V(k-1)[b], SB(k), SB(k+1)

import netifaces

#-------variable-------

#port of server
PORT=31500  

#-------funtion--------

#get host ip address
def get_ip(interface_name): 
	info = netifaces.ifaddresses(interface_name) 
	return info[netifaces.AF_INET][0]['addr']
