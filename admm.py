import numpy as np
import time 
import matplotlib.pyplot as plt
from matplotlib import animation

import globle as g
import database as db
import command as c
import topology as tp

#soft thresholding operator
def sthresh(x, gamma):
    return np.sign(x) * np.maximum(0, np.absolute(x) - gamma)

def admm(mode_i):
	G, = db.load(['G'],mode_i)
	if g.L_MODE[mode_i][0] == 'Lasso':
		if g.L_MODE[mode_i][1] == 'SingleADMM':
			#u,x,z
			u = np.zeros([g.DD, 1])
			x = np.zeros([g.DD, 1])
			z = np.zeros([g.DD, 1])
			
			#save time,u,x,z in iter k
			ts = np.zeros([g.ITER]) 
			us = np.zeros([g.ITER, g.DD, 1])  
			xs = np.zeros([g.ITER, g.DD, 1])
			zs = np.zeros([g.ITER, g.DD, 1])

			A, b = db.load(['A','b'],mode_i)
			#compute
			print('Computing...(mode:%s)'%(str(g.L_MODE[mode_i])))
			start_time=time.time()
			AtA = A.T.dot(A)
			Atb = A.T.dot(b)
			Q = AtA + g.RHO * np.identity(g.DD)
			Q = np.linalg.inv(Q)

			k = 0
			while (k < g.ITER):
				u = u + x - z
				x = Q.dot(Atb + g.RHO * (z - u))
				z = sthresh(x + u, g.THETA / g.RHO)

				ts[k] = time.time()				
				us[k] = u
				xs[k] = x
				zs[k] = z
				
				k = k + 1
			end_time=time.time()
			print('Done! (mode:%s, time:%f)\n'%(str(g.L_MODE[mode_i]),end_time-start_time))			
			
			#save
			db.save({'t':ts,'u':us,'x':xs,'z':zs},mode_i)
			
		elif g.L_MODE[mode_i][1] == 'StarADMM':
			if g.L_MODE[mode_i][2] == 'random':  #-----------------------------------------这里有bug，随机不随机其实都一样处理
				#get bridges and workers
				l_bridge, l_worker = tp.get_bridges_workers(G)
				#send command to bridges and workers
				c.init_bridge(l_bridge,mode_i)  #init bridge frist to stop the last compute
				c.init_worker(l_worker,mode_i)
				c.start_bridge(l_bridge)
				
		elif g.L_MODE[mode_i][1] == 'BridgeADMM':
			pass
		
		else:
			print('Error: out of L_MODE.')
			input()
			#写图的'b2w'
			#初始化命令bridges workers，清空数据、获得data、读图等 （bridges workers返回就绪命令）
			#启动命令（当所有bridges workers都发来就绪命令）
			#重启命令
			#停止命令
			
			
def get_min(mode_i):
	if g.L_MODE[mode_i][0] == 'Lasso':
		CVXmin = db.load(['CVXmin'])
		LLPmin = np.zeros([g.ITER])
		LLPac = np.zeros([g.ITER])
		if g.L_MODE[mode_i][1] == 'SingleADMM':
			A, b, u, x, z = db.load(['A','b','u','x','z'],mode_i)
			for k in range(g.ITER):
				LLPmin[k]=0.5*np.square(np.dot(A,x[k])-b).sum()+g.RHO*np.dot(u[k].T,(x[k]-z[k]))+0.5*g.RHO*(np.square(x[k]-z[k]).sum())+g.THETA*np.linalg.norm(z[k], ord=1)
				LLPac[k]=abs(LLPmin[k]-CVXmin)/CVXmin
		elif g.L_MODE[mode_i][1] == 'StarADMM':
			LLPmin=[1,2,3]
			LLPac=[0.1,0.2,0.3]
		elif g.L_MODE[mode_i][1] == 'BridgeADMM':
			LLPmin=[1,2,3]
			LLPac=[0.1,0.2,0.3]		
		db.save({'LLPmin':LLPmin,'LLPac':LLPac},mode_i)
			
def result(problem):
	print('Result:')
	if problem == 'Lasso':
		NORMx0, CVXmin = db.load(['NORMx0','CVXmin'])
		print('NORMx0=',NORMx0)		
		print('CVXmin=',CVXmin)	
		LLPmin, LLPac = db.load(['LLPmin', 'LLPac'], mode_i=0)  #LLPmin= Lasso LP funtion min value, LLPac = accuracy of LLP
		print(LLPmin[g.ITER-1])
		print(LLPac[g.ITER-1])

		lineX = np.linspace(0, g.ITER, g.ITER)			
		# fig1 = plt.figure('fig1')
		# plt.axhline(NORMx0, ls='--', label='NORMx0')
		# plt.axhline(CVXmin, ls='--', label='CVXmin')
		# plt.plot(lineX, LLPmin['SingleADMM'], label='SingleADMM')
		
		fig=plt.figure()
		axes = plt.subplot(111)
		def init():
			axes.cla()
			plt.ylim(1.0e-16, 1.0e+16)
			plt.yscale('log')
			plt.xlim(-5, 105)
			plt.plot(lineX, LLPac, label='SingleADMM', linewidth=0.5, color='k')	
			plt.legend()
		def animate(k):
			axes.scatter(lineX[k], LLPac[k], s=30)
		anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=8)  
	
		plt.show()
