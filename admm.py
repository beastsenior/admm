#每个worker计算一个S和多个V，每个bridge计算一个SB，另外每个worker还有一个C（这里暂时把每个worker的C都设为一样，以后可改为C[200]。这个所谓C，就是ADMM经典论文中的ρ[rəʊ]，在传感器那篇论文叫ρ，这里变量用RHO表示）
#各变量对应如下
#本程序中的变量：      Zk,   Zk1,    Yk[200], Yk_1[200], Xk,    Xk1,     RHO  
#传感器论文中的变量：  S(k), S(k+1), V(k)[b], V(k-1)[b], SB(k), SB(k+1), C[200] （每个node的ρ参数都一样时，就直接用一个RHO了）
#ADMM经典论文中的变量：Z(k), Z(k+1), Y(k)[b], Y(k-1)[b], X(k),  X(k+1),  ρ

#use the scaled form. use Uk to instead Yk. (Yk=RHO*Uk)

#本例计算lasso, min (1/2)*(||Ax-b||22)-LAMBDA*(|x|1)

import numpy as np
import struct
import random

#dimension of the data, e.g. X_target,X,Y,Z...
DD = 100
#number of the data
ND = 200
#value of RHO
RHO = 500.0
#value of LAMBDA (parameter of lasso)
LAMBDA = 0.1
#percent of the non-zero value of X target (lasso)
POZ = 0.05

#soft thresholding operator for the computing of Zk in lasso, Page 32 in the paper of ADMM boyd
def soft_thresholding(a,k):
	magnitude = np.absolute(a)
	with np.errstate(divide='ignore'):
		thresholded = (1 - k/magnitude)
		thresholded.clip(min=0, max=None, out=thresholded)
		thresholded = a * thresholded
	return thresholded

#compute Xk1, Uk and Zk1. 
def get_Xk1(A, b , Uk, Zk, active_bridge, num_active_bridge):
	sum_tmp = np.zeros(DD) 
	for addr in active_bridge:
		sum_tmp = sum_tmp + Zk[addr] - Uk[addr]
	return np.dot(np.linalg.inv(np.dot(A.T,A)+num_active_bridge*RHO*np.eye(DD)),(np.dot(A.T,b)+RHO*sum_tmp))
	
def get_Uk(Xk, Uk_1, Zk):
	return Uk_1+Xk-Zk

def get_Zk1(Xk1_and_Uk, active_worker, num_active_worker):
	sum_tmp = np.zeros(DD) 
	for addr in active_worker:
		sum_tmp = sum_tmp + Xk1_and_Uk[addr]
	a = sum_tmp/num_active_worker
	k = LAMBDA/(RHO*num_active_worker)
	return soft_thresholding(a,k)
	
#generate X target and data A, b (lasso)
def lasso_data_generator():
	X_target = np.zeros(DD) 
	# for i in random.sample(range(DD), int(POZ*DD)):
		# X_target[i] = np.random.random()
	X_target[1]=0.1
	X_target[2]=0.2
	X_target[3]=-0.3
	X_target[97]=-0.97
	X_target[98]=0.98
	A = np.random.normal(0.0, 0.1, (ND, DD))
	b = np.dot(A, X_target)+np.random.normal(0.0, 0.01, ND)  #b=A*X_target+noise
	return X_target, A, b
	
	