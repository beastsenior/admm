import numpy as np
import os

#random seed
#SEED = 1
SEED = np.random.randint(5)
np.random.seed(SEED)

#network interface parameter
BPORT=21500  #port of bridge
WPORT=31500  #port of worker
#ip list. (admin ip is 172.16.100.1, which is not in the list)
L_IP = [\
'172.16.100.2',  '172.16.100.3',  '172.16.100.4',  '172.16.100.5',  '172.16.100.6',  \
'172.16.100.7',  '172.16.100.8',  '172.16.100.9',  '172.16.100.10', '172.16.100.11', \
'172.16.100.12', '172.16.100.13', '172.16.100.14', '172.16.100.15', '172.16.100.16', \
'172.16.100.17']
NW = len(L_IP)  # number of worker (node)
#ip dict. {0:'172.16.100.2,1:'172.16.100.3'...}
def ipdict():  #iplist to ipdict
	keys=range(NW)
	return dict(zip(keys, L_IP))
D_IP = ipdict()  

#topology parameter
POC = 0.3 #probability of connection between two nodes

#admm parameter
ITER = 1000
THETA = 0.1
RHO = 500.0
DD = 100  #dimension of data
ND = 200  #number of data
PNZ = 0.05  # percent of non zeros
R = 0
L_TAU = [1,3,10,50]

#mode of admm, o=original admm, s=star admm, sa=star adadmm, b=bridge admm, 'b' also use to save G and data x0,A,b
L_MODE = ['o','s','sa','b']

#problem, L=lasso
L_PROBLEM = ['L']

#data name in database: G is graph of the network topology, x0,A,b are source data, x,u,z are results, NORMx0 means theta*|x0|_1.
L_DATA = ['G', \
'x0','A','b', \
't','x','u','z',\
'NORMx0','CVXmin']

#direction for saving data
DATA_DIR = './data/'
if os.path.isdir(DATA_DIR)!=True:
    os.mkdir(DATA_DIR)

 
