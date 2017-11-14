#network interface parameter
BPORT=21500  #port of bridge
WPORT=31500  #port of worker
#ip list. (admin ip is 172.16.100.1, which is not in the list)
IPLIST = [\
'172.16.100.2',  '172.16.100.3',  '172.16.100.4',  '172.16.100.5',  '172.16.100.6',  \
'172.16.100.7',  '172.16.100.8',  '172.16.100.9',  '172.16.100.10', '172.16.100.11', \
'172.16.100.12', '172.16.100.13', '172.16.100.14', '172.16.100.15', '172.16.100.16', \
'172.16.100.17']

#topology parameter
NW = 16  # number of worker (node)
POC = 0.3 #probability of connection between two nodes

#admm parameter
MAX_ITER = 1000
THETA = 0.1
RHO = 500.0
DD = 100  #dimension of data
ND = 200  #number of data
PNZ = 0.05  # percent of non zeros
R = 0
LIST_TAU = [1,3,10,50]

#mode of admm, b=basic admm, s=star admm, sa=star adadmm, b=bridge admm
MOA = ['b','s','sa','b']

#problem, L=lasso
PROBLEM = ['L']

#data name in database, G=graph of the network topology, 
#Lam=min of lasso F(x) (or L(x)) based on admm, Lcm=min of lasso F(x) based on cvx, Lnm=theta*|x|_1 
DND = ['G', \  #graph
'Lx0','LA','Lb', \  #data
'Lx','Lu','Lz','Lam','Lcm','Lnm']    #result
 
