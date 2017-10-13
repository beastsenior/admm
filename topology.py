import net_interface as ni
import sys
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

#max double number
MAXDOUBLE = sys.float_info.max
#max double number in packed type
PMD = struct.pack('d', MAXDOUBLE)
#connetion rate of node pair
CONNETION_RATE = 0.5

#init a random delay network topology
def rand_topology():
	adjacency_matrix = {}  #adjacency matrix with delay value
	for i in range(NN):
		adjacency_matrix[(IPLIST[i], IPLIST[i])] = 0  #the delay between node and itself is 0
		for j in range(i):
			tmp = random.random()
			if tmp > CONNETION_RATE:
				adjacency_matrix[(IPLIST[i], IPLIST[j])] = adjacency_matrix[(IPLIST[j], IPLIST[i])] = tmp - CONNETION_RATE  #network delay between node pair
			else:
				adjacency_matrix[(IPLIST[i], IPLIST[j])] = adjacency_matrix[(IPLIST[j], IPLIST[i])] = MAXDOUBLE #when delay = MAXDOUBLE means delay = infinity
	return adjacency_matrix

#save topology to file
def save_topology(adjacency_matrix, saving_file='adjacency_matrix.txt'):
	fp = open(saving_file, 'w')
	fp.write(str(adjacency_matrix))
	fp.close

#load topology from file
def load_topology(loading_file='adjacency_matrix.txt'):
	fp = open(loading_file, 'r')
	adjacency_matrix_str = fp.read()
	fp.close
	return eval(adjacency_matrix_str)

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
	topology_mask={}
	for from_bridge in IPLIST:
		for to_worker in IPLIST:
			if adjacency_matrix[(from_bridge, to_worker)] == MAXDOUBLE:
				topology_mask[(from_bridge, to_worker)] = 0
			else:
				topology_mask[(from_bridge, to_worker)] = 1
	return topology_mask
	
#save topology to file
def save_mask(topology_mask, saving_file='topology_mask.txt'):
	fp = open(saving_file, 'w')
	fp.write(str(topology_mask))
	fp.close

#load topology from file
def load_mask(loading_file='topology_mask.txt'):
	fp = open(loading_file, 'r')
	topology_mask_str = fp.read()
	fp.close
	return eval(topology_mask_str)
	
#get active neighbor worker, include itself, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and the number of active neighbor worker, include itself
def get_active_worker(topology_mask):
	active_worker = []
	i = 0
	for ip in IPLIST:
		if topology_mask[(ni.LOCAL_IP, ip)] == 1:

			active_worker.append((ip, ni.PORT))
			i = i + 1
	return active_worker, i 	#eg. active_worker=[('172.16.100.2', ni.PORT), ('172.16.100.3', ni.PORT), ('172.16.100.5', ni.PORT)], i=3

#get active neighbor bridge, include itself, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and the number of active neighbor bridge, include itself
def get_active_bridge(topology_mask):
	active_bridge = []
	i = 0
	for ip in IPLIST:
		if topology_mask[(ip, ni.LOCAL_IP)] == 1:
			active_bridge.append((ip, ni.OUTPORT))
			i = i + 1
	return active_bridge, i    #eg. active_bridge=[('172.16.100.2', ni.OUTPORT),('172.16.100.3', ni.OUTPORT)], i=2


