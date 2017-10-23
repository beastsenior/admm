import numpy as np
import struct

DD=10
Zk = np.random.random([DD])
Zk1 = np.zeros([DD])
s_msg = struct.pack('%ud'%DD,*Zk)

print(Zk,Zk1,type(Zk), type(Zk1), type(Zk[1]),type(Zk1[1]),s_msg)

Zk1=Zk
print(Zk1)

# def fun(a,b,c):
	# print(a,b,c)
	
# fun(1,2,3)
# fun(4,*[5,6])