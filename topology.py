import net_interface as ni
import sys
import struct

#node ip list
IPLIST = (\
'172.168.100.2',  '172.168.100.3',  '172.168.100.4',  '172.168.100.5',  '172.168.100.6',  \
'172.168.100.7',  '172.168.100.8',  '172.168.100.9',  '172.168.100.10', '172.168.100.11', \
'172.168.100.12', '172.168.100.13', '172.168.100.14', '172.168.100.15', '172.168.100.16', \
'172.168.100.17', '172.168.100.18', '172.168.100.19', '172.168.100.20', '172.168.100.21', \
)

#max doulbe number in packed type
PMD = struct.pack('d', sys.float_info.max)

#number of node
NN = 20

#get active neighbor worker, include itself, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and the number of active neighbor worker, include itself
def get_active_worker():
	# fp = open('net.txt')
	# try:
		# all_the_text = file_object.read( )
	# finally:
		# file_object.close( )
	# an=[]
	# ann=
	tmp=[['172.16.100.2', ni.PORT], ['172.16.100.3', ni.PORT], ['172.16.100.5', ni.PORT]]
	return tmp, 3