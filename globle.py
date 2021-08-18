import numpy as np

#random seed
#SEED = 1
# SEED = np.random.randint(50)
# np.random.seed(SEED)

#network interface parameter
APORT=31500  #port of admin
BPORT=31501  #port of bridge
WPORT=31502  #port of worker
BUFSIZE = 2000 #recvfrom(bufsize)

#ip list. (admin ip is 172.16.100.1, which is not in the list)
L_IP = [\
'172.16.100.2',  '172.16.100.3',  '172.16.100.4',  '172.16.100.5',  '172.16.100.6',  \
'172.16.100.7',  '172.16.100.8',  '172.16.100.9',  '172.16.100.10', '172.16.100.11', \
'172.16.100.12', '172.16.100.13', '172.16.100.14', '172.16.100.15', '172.16.100.16', \
'172.16.100.17']
IP_ADMIN = '172.16.100.1'  #admin machine IP
NN = len(L_IP)  # number of node
#ip dict. {0:'172.16.100.2,1:'172.16.100.3'...}
def ipdict():  #iplist to ipdict
	keys=range(NN)
	return dict(zip(keys, L_IP))
D_IP = ipdict()  

#topology parameter
POC = 0.3667 #probability of connection between two nodes

#admm parameter
ITER = 200
THETA = 0.1
RHO = 500.0
DD = 100  #dimension of data
ND = 200  #number of data
PNZ = 0.05  # percent of non zeros
# R = 0
L_TAU = [1,3,10,50]

#mode of admm, single machine, star cluster, multiple bridge. As mode_i send as int8 over socket, len(L_MODE) should less than 128.
# L_MODE = [\
# ['mode label','Lasso','SingleADMM'],\
# ['mode label','Lasso','StarADMM','random',L_TAU[0]],\
# ['mode label','Lasso','StarADMM','random',L_TAU[1]],\
# ['mode label','Lasso','StarADMM','random',L_TAU[2]],\
# ['mode label','Lasso','StarADMM','random',L_TAU[3]],\
# ['mode label','Lasso','BridgeADMM','complete',L_TAU[0]],\
# ]
L_MODE = [\
#['Basic-ADMM-Allbatch','Lasso','SingleADMM','all_batch'],\
#['Basic-ADMM-Onebatch','Lasso','SingleADMM','one_batch'],\
['Star-ADMM','Lasso','StarADMM','random',L_TAU[0]],\
['Greedy-Bridge-ADMM','Lasso','BridgeADMM','complete',L_TAU[0]],\
]
#direction for saving data
DATA_DIR = './data/'

#command (0 -> 127 use to mode_i, -1 -> -128 use to command)
#for example: 
#sending np.int8(2).tostring to worker 7, means the command 'mode_i in worker 7 change to 2'
#sending np.int8(-2).tostring to bridge 10, means the command 'bridge 10 start'
D_COMMAND={'bridge reset':-1,'bridge start':-2,'bridge ready':-3,'worker ready':-4}
 
