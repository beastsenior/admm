import numpy as np
import time 
import matplotlib.pyplot as plt
from matplotlib import animation

import globle as g
import database as db

#soft thresholding operator
def sthresh(x, gamma):
    return np.sign(x) * np.maximum(0, np.absolute(x) - gamma)

def admm(problem,mode):
	if problem == 'L':
		if mode == 'o':
			#u,x,z
			u = np.zeros([g.DD, 1])
			x = np.zeros([g.DD, 1])
			z = np.zeros([g.DD, 1])
			
			#save time,u,x,z in iter k
			ts = np.zeros([g.ITER]) 
			us = np.zeros([g.ITER, g.DD, 1])  
			xs = np.zeros([g.ITER, g.DD, 1])
			zs = np.zeros([g.ITER, g.DD, 1])

			#compute
			print('Computing...(problem:%s,mode:%s)'%(problem,mode))
			start_time=time.time()
			x0, A, b = db.load(['x0','A','b'])
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
			print('Done! (problem:%s,mode:%s,time:%f)\n'%(problem,mode,end_time-start_time))			
			
			#save
			db.save({'t':ts,'u':us,'x':xs,'z':zs})

def get_min(problem):
	if problem == 'L':
		CVXmin = db.load(['CVXmin'])
		LLPmin = {}
		LLPac = {}
		for mode in g.L_MODE:
			if mode == 'o':
				A, b, u, x, z = db.load(['A','b','u','x','z'])
				lp = np.zeros([g.ITER])
				ac = np.zeros([g.ITER])
				for k in range(g.ITER):
					lp[k]=0.5*np.square(np.dot(A,x[k])-b).sum()+g.RHO*np.dot(u[k].T,(x[k]-z[k]))+0.5*g.RHO*(np.square(x[k]-z[k]).sum())+g.THETA*np.linalg.norm(z[k], ord=1)
					ac[k]=abs(lp[k]-CVXmin)/CVXmin
				LLPmin[mode]=lp
				LLPac[mode]=ac
			elif mode == 'sa':
				LLPmin[mode] = {}
				for submode in g.L_TAU:
					if submode == 1:
						LLPmin[mode][submode]=[1,2,3]
		return LLPmin, LLPac
			
def result(problem):
	print('Result:')
	if problem == 'L':
		NORMx0, CVXmin = db.load(['NORMx0','CVXmin'])
		print('NORMx0=',NORMx0)		
		print('CVXmin=',CVXmin)	
		LLPmin, LLPac = get_min(problem)  #LLPmin= Lasso LP funtion min value, LLPac = accuracy of LLP
		print(LLPmin['o'][g.ITER-1])
		print(LLPac['o'][g.ITER-1])

		lineX = np.linspace(0, g.ITER, g.ITER)			
		# fig1 = plt.figure('fig1')
		# plt.axhline(NORMx0, ls='--', label='NORMx0')
		# plt.axhline(CVXmin, ls='--', label='CVXmin')
		# plt.plot(lineX, LLPmin['o'], label='o')
		
		fig=plt.figure()
		axes = plt.subplot(111)   
		def init():
			axes.cla()
			plt.ylim(1.0e-16, 1.0e+16)
			plt.yscale('log')
			plt.xlim(-10, 60)
			lines,=plt.plot(lineX, LLPac['o'], label='o', linewidth=0.5, color='k')	
		def animate(k):
			axes.scatter(lineX[k], LLPac['o'][k], s=30, label='o')
		anim = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=80)  
		
		plt.legend()
		plt.show()
		
		# plt.ylim(1.0e-16, 1.0e+16)
		# plt.yscale('log')
		# lineX = np.linspace(0, g.ITER, g.ITER)
		# plt.axhline(NORMx0, ls='--', label='NORMx0')
		# plt.axhline(CVXmin, ls='--', label='CVXmin')		
		# plt.plot(lineX, LLPac['o'], label='o')
		# plt.legend()
		# plt.show()
		
		
		# for mode in g.L_MODE:
			# plt.plot(lineX, LLPac[mode], label=mode)