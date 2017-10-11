import net_interface as ni
import sys
import struct
import random

#node ip list
IPLIST = [\
'172.16.100.2',  '172.16.100.3',  '172.16.100.4',  '172.16.100.5',  '172.16.100.6',  \
'172.16.100.7',  '172.16.100.8',  '172.16.100.9',  '172.16.100.10', '172.16.100.11', \
'172.16.100.12', '172.16.100.13', '172.16.100.14', '172.16.100.15', '172.16.100.16', \
'172.16.100.17', '172.16.100.18', '172.16.100.19', '172.16.100.20', '172.16.100.21', \
]

#max double number
MAXDOUBLE = sys.float_info.max
#max double number in packed type
PMD = struct.pack('d', MAXDOUBLE)
#number of node
NN = 20
#connetion rate of node pair
CONNETION_RATE = 0.5

#init a random delay network
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

#get active neighbor worker, include itself, eg. [('172.16.100.3',27514),('172.16.100.7',27511)], and the number of active neighbor worker, include itself
def get_active_worker(adjacency_matrix):
	active_worker = []
	i = 0
	for ip in IPLIST:
		if adjacency_matrix[(ni.LOCAL_IP, ip)] != MAXDOUBLE:
			active_worker.append((ip, ni.PORT))
			i = i + 1
	return active_worker, i 	#eg. active_worker=[('172.16.100.2', ni.PORT), ('172.16.100.3', ni.PORT), ('172.16.100.5', ni.PORT)]


def get_active_bridge(adjacency_matrix):
	active_bridge = []
	i = 0
	for ip in IPLIST:
		if adjacency_matrix[(ni.LOCAL_IP, ip)] != MAXDOUBLE:
			active_bridge.append((ip, ni.OUTPORT))
			i = i + 1
	return active_bridge, i    #eg. active_bridge=[('172.16.100.2', ni.OUTPORT),('172.16.100.3', ni.OUTPORT)]

#test-----------
# tmp_to = rand_topology()
# for i in IPLIST:
	# for j in IPLIST:
		# print(i, '-->', j, tmp_to[(i,j)])
# print('\n\n')
# save_topology(tmp_to)
# tmp_to = load_topology()
# print(tmp_to)
# print('\n\n')
# for i in IPLIST:
	# for j in IPLIST:
		# print(i, '-->', j, tmp_to[(i,j)])
# active_bridge, num = get_active_bridge(tmp_to)
# print('\n\n')
# print(num)
# print(active_bridge)

