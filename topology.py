import net_interface as ni
import struct
import random

#number of node
# NN = 20
NN = 10
#node ip list
# IPLIST = [\
# '172.16.100.2',  '172.16.100.3',  '172.16.100.4',  '172.16.100.5',  '172.16.100.6',  \
# '172.16.100.7',  '172.16.100.8',  '172.16.100.9',  '172.16.100.10', '172.16.100.11', \
# '172.16.100.12', '172.16.100.13', '172.16.100.14', '172.16.100.15', '172.16.100.16', \
# '172.16.100.17', '172.16.100.18', '172.16.100.19', '172.16.100.20', '172.16.100.21', \
# ]
IPLIST = [\
'172.16.100.2',  '172.16.100.3',  '172.16.100.4',  '172.16.100.5',  '172.16.100.6',  \
'172.16.100.7',  '172.16.100.8',  '172.16.100.9',  '172.16.100.10', '172.16.100.11', \
]

#max double number（本来应该是1.7976931348623157e+308，但有问题，不妨设为1.7976931348622e+308） 
MAXDOUBLE = 1.7976931348622e+308
#max double number in packed type
PMD = struct.pack('d', MAXDOUBLE)
#connetion rate of node pair
CONNETION_RATE = 0.3

#init a random delay network topology
def rand_topology():
	adjacency_matrix = {}  #adjacency matrix with delay value
	for i in range(NN):
		adjacency_matrix[(IPLIST[i], IPLIST[i])] = 0.0  #the delay between node and itself is 0
		for j in range(i):
			tmp = random.random()
			if tmp > (1-CONNETION_RATE):
				adjacency_matrix[(IPLIST[i], IPLIST[j])] = adjacency_matrix[(IPLIST[j], IPLIST[i])] = tmp - CONNETION_RATE  #network delay between node pair
			else:
				adjacency_matrix[(IPLIST[i], IPLIST[j])] = adjacency_matrix[(IPLIST[j], IPLIST[i])] = MAXDOUBLE #when delay = MAXDOUBLE means delay = infinity
	return adjacency_matrix

#save topology to file
def save_topology(adjacency_matrix, conn, cursor):
	cursor.execute('lock tables t write')
	cursor.execute('truncate table t')
	for b2w in adjacency_matrix:
		cursor.execute('insert into t(b2w,d) values(%s,%s)', (str(b2w),adjacency_matrix[b2w]))
	conn.commit()
	cursor.execute('unlock tables')

#load topology from file
def load_topology(conn, cursor):
	adjacency_matrix={}
	cursor.execute('select * from t')
	conn.commit()
	adjacency_matrix_tuple = cursor.fetchall()
	for i in range(NN*NN):
		adjacency_matrix[eval(adjacency_matrix_tuple[i][0])]=adjacency_matrix_tuple[i][1]
	return adjacency_matrix

#all neighbor worker and itself, include active and resting nodes, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and i is the number of neighbor worker, include itself
def get_neighbor_worker(adjacency_matrix):
	neighbor_worker = []
	i = 0
	for ip in IPLIST:
		if adjacency_matrix[(ni.LOCAL_IP, ip)] != MAXDOUBLE:
			neighbor_worker.append((ip, ni.PORT))
			i = i + 1
	return neighbor_worker, i 
	
#all neighbor bridge and itself, include active and resting nodes, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and i is the number of neighbor bridge, include itself
def get_neighbor_bridge(adjacency_matrix):
	neighbor_bridge = []
	i = 0
	for ip in IPLIST:
		if adjacency_matrix[(ip, ni.LOCAL_IP)] != MAXDOUBLE:
			neighbor_bridge.append((ip, ni.OUTPORT))
			i = i + 1
	return neighbor_bridge, i 
	
	
#mask of the bridge and worker
def get_full_mask(adjacency_matrix):
	adjacency_mask={}
	for from_bridge in IPLIST:
		for to_worker in IPLIST:
			if adjacency_matrix[(from_bridge, to_worker)] == MAXDOUBLE:
				adjacency_mask[(from_bridge, to_worker)] = -1  #no connection
			else:
				adjacency_mask[(from_bridge, to_worker)] = 1  #from_bridge is a bridge for to_worker; to_worker is a worker for from_bridge
	return adjacency_mask
	
#save mask to file
def save_mask(adjacency_mask, conn, cursor):
	cursor.execute('lock tables m write')
	cursor.execute('truncate table m')
	for b2w in adjacency_mask:
		cursor.execute('insert into m(b2w,c) values(%s,%s)', (str(b2w),adjacency_mask[b2w]))
	conn.commit()
	cursor.execute('unlock tables')

#load mask from file
def load_mask(conn, cursor):
	get_mask_dict={}
	cursor.execute('select * from m')
	conn.commit()
	get_mask_tuple = cursor.fetchall()
	for i in range(NN*NN):
		get_mask_dict[eval(get_mask_tuple[i][0])]=get_mask_tuple[i][1]
	return get_mask_dict
	
#get active neighbor worker, include itself, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and the number of active neighbor worker, include itself
def get_active_worker(adjacency_mask):
	active_worker = []
	i = 0
	for ip in IPLIST:
		if adjacency_mask[(ni.LOCAL_IP, ip)] == 1:
			active_worker.append((ip, ni.PORT))
			i = i + 1
	return active_worker, i 	#eg. active_worker=[('172.16.100.2', ni.PORT), ('172.16.100.3', ni.PORT), ('172.16.100.5', ni.PORT)], i=3

#get active neighbor bridge, include itself, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and the number of active neighbor bridge, include itself
def get_active_bridge(adjacency_mask):
	active_bridge = []
	i = 0
	for ip in IPLIST:
		if adjacency_mask[(ip, ni.LOCAL_IP)] == 1:
			active_bridge.append((ip, ni.OUTPORT))
			i = i + 1
	return active_bridge, i    #eg. active_bridge=[('172.16.100.2', ni.OUTPORT),('172.16.100.3', ni.OUTPORT)], i=2
