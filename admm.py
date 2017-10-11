#每个worker计算一个S和多个V，每个bridge计算一个SB，另外每个worker还有一个C（这里暂时把每个worker的C都设为一样，以后可改为C[200]。这个所谓C，就是ADMM经典论文中的ρ[rəʊ]，在传感器那篇论文叫ρ，这里变量用RHO表示）
#各变量对应如下
#本程序中的变量：      Zk,   Zk1,    Yk[200], Yk_1[200], Xk,    Xk1,     RHO  
#传感器论文中的变量：  S(k), S(k+1), V(k)[b], V(k-1)[b], SB(k), SB(k+1), C[200] （每个node的ρ参数都一样时，就直接用一个RHO了）
#ADMM经典论文中的变量：Z(k), Z(k+1), Y(k)[b], Y(k-1)[b], X(k),  X(k+1),  ρ

#本例计算min |2x-6|^2

import struct

#value of RHO
RHO = 0.000001

#bridge compute Xk1, Yk and Zk1 
def get_Xk1(Xk, Yk, Zk, active_bridge, num_active_bridge):
	sum_Yk = 0.0
	sum_Zk = 0.0
	for addr in active_bridge:
		sum_Yk = sum_Yk + Yk[addr]
		sum_Zk = sum_Zk + Zk[addr]
	return (12.0 + RHO*(sum_Zk-sum_Yk))/(4.0+RHO*num_active_bridge)

def get_Yk(Xk, Yk_1, Zk):
	return Yk_1+RHO*(Xk-Zk)
	
def get_Zk1(Xk1, Yk, active_worker, num_active_worker):
	sum_tmp = 0.0
	for addr in active_worker:
		sum_tmp = sum_tmp + RHO*Xk1[addr] + Yk[addr]
	return sum_tmp/(RHO*num_active_worker)
