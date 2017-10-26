import numpy as np
# import struct

# DD=10
# Zk = np.random.random([DD])
# Zk1 = np.zeros([DD])
# s_msg = struct.pack('%ud'%DD,*Zk)

# print(Zk,Zk1,type(Zk), type(Zk1), type(Zk[1]),type(Zk1[1]),s_msg)

# Zk1=Zk
# print(Zk1)

# def fun(a,b,c):
	# print(a,b,c)
	
# fun(1,2,3)
# fun(4,*[5,6])

def soft_thresholding(a,k):
	magnitude = np.absolute(a)
	with np.errstate(divide='ignore'):
		thresholded = (1 - k/magnitude)
		thresholded.clip(min=0, max=None, out=thresholded)
		thresholded = a * thresholded
	return thresholded
	
a=np.array([-5,-4,-3,-2,-1,0,1,2,3,4,5])
b=soft_thresholding(a,3)
print(b)
print(b[3]==b[6])