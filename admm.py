import numpy as np
import time 

import globle as g
import database as db
import command as c
import topology as tp

#soft thresholding operator, boyd paper P32
def sthresh(a, k):
    return np.sign(a) * np.maximum(0, np.absolute(a) - k)

def admm(mode_i):
	G, = db.load(['G'],mode_i)
	if g.L_MODE[mode_i][0] == 'Lasso':
		if g.L_MODE[mode_i][1] == 'SingleADMM':
			#u,x,z
			u = np.zeros([g.DD, 1])
			x = np.zeros([g.DD, 1])
			z = np.zeros([g.DD, 1])
			
			#time, Lagrangian funtion
			t = np.zeros([g.ITER]) 
			Lmin = np.zeros([g.ITER])  

			A, b = db.load(['A','b'],mode_i)
			#compute
			AtA = A.T.dot(A)
			Atb = A.T.dot(b)
			Q = AtA + g.RHO * np.identity(g.DD)
			Q = np.linalg.inv(Q)

			k = 0
			while (k < g.ITER):
				u = u + x - z
				x = Q.dot(Atb + g.RHO * (z - u))
				z = sthresh(x + u, g.THETA / g.RHO)

				Lmin[k]=0.5*np.square(np.dot(A,x)-b).sum()+g.RHO*np.dot(u.T,(x-z))+0.5*g.RHO*(np.square(x-z).sum())+g.THETA*np.linalg.norm(z, ord=1)
				t[k] = time.time()
				k += 1
			#save
			db.save({'t':t,'Lmin':Lmin},mode_i)
			
		elif g.L_MODE[mode_i][1] == 'StarADMM' or g.L_MODE[mode_i][1] == 'BridgeADMM':
			#get bridges and workers
			l_bridge, l_worker = tp.get_bridges_workers(G)
			#send command to bridges and workers
			c.init_bridge(l_bridge,mode_i)  #init bridge frist to stop the last compute
			c.init_worker(l_worker,mode_i)
			c.start_bridge(l_bridge)
			all_Lmin = np.zeros([g.ITER])
			for ip in l_bridge:
				Lmin[ip], = db.load(['Lmin'],mode_i,ip)
				all_Lmin = all_Lmin + Lmin[ip]
			db.save({'Lmin':all_Lmin},mode_i)
		
		else:
			print('Error: out of L_MODE.')
			input()

#compute Lagrangian function value (equation (5) in paper 'Asynchronous Distributed ADMM for Large-Scale Optimization—Part I' )
def get_Lmin(xu,z,A,b,l_row):
	L = 0.0
	for ip in l_row:
		L = L + 0.5*(np.array((np.square(np.dot(A[ip], xu[ip][0])-b[ip]))).sum()) + g.RHO*np.dot(xu[ip][1],(xu[ip][0]-z))+0.5*g.RHO*(np.array((np.square(xu[ip][0]-z))).sum())
	L = L + g.THETA*np.linalg.norm(z,ord = 1)
	return L

# def get_min(mode_i):
	# ac = np.zeros([g.ITER])  ++++++++++++++++
	# if g.L_MODE[mode_i][0] == 'Lasso':
		# CVXmin = db.load(['CVXmin'])
		# LLPmin = np.zeros([g.ITER])
		# LLPac = np.zeros([g.ITER])
		# if g.L_MODE[mode_i][1] == 'SingleADMM':
			# A, b, u, x, z = db.load(['A','b','u','x','z'],mode_i)
			# for k in range(g.ITER):
				# LLPmin[k]=0.5*np.square(np.dot(A,x[k])-b).sum()+g.RHO*np.dot(u[k].T,(x[k]-z[k]))+0.5*g.RHO*(np.square(x[k]-z[k]).sum())+g.THETA*np.linalg.norm(z[k], ord=1)
				# LLPac[k]=abs(LLPmin[k]-CVXmin)/CVXmin
		# elif g.L_MODE[mode_i][1] == 'StarADMM':
			# A,b,u,x,z={},{},{},{},{}
			# G, = db.load(['G'],mode_i)
			# l_bridge, l_worker = tp.get_bridges_workers(G)
			# for ip in l_worker:
				# A[ip], b[ip], u[ip], x[ip]= db.load(['A','b','u','x'],mode_i,ip)
			# for ip in l_bridge:
				# z[ip],= db.load(['z'],mode_i,ip)
			# for k in range(g.ITER):
				# all_L = 0.0
				# i = 0
				# for b_ip in l_bridge:
					# l_worker = tp.get_ow(G,ip)
					# L = 0.0
					# for w_ip in l_worker:
						# L = L + 0.5*(np.array((np.square(np.dot(A[w_ip][k], x[w_ip][k])-b[w_ip][k]))).sum()) + g.RHO*np.dot(u[w_ip][k][i],(x[w_ip][k]-z[b_ip][k]))+0.5*g.RHO*(np.array((np.square(x[w_ip][k]-z[b_ip][k]))).sum())
						# L = L + g.LAMBDA*np.linalg.norm(z[b_ip][k],ord = 1)	
					# i += 1
					# all_L += L
					
				# LLPmin[k]=all_L
				# LLPac[k]=abs(LLPmin[k]-CVXmin)/CVXmin

			
		# elif g.L_MODE[mode_i][1] == 'BridgeADMM':
			# LLPmin=[1,2,3]
			# LLPac=[0.1,0.2,0.3]	
		
		# db.save({'LLPmin':LLPmin,'LLPac':LLPac},mode_i)
			
def get_z(xu, l_row, nrow):
	sum = np.zeros([g.DD,1]) 
	for ip in l_row:
		sum = sum + xu[ip][0] + xu[ip][1]
	a = sum/nrow
	k = g.THETA/(g.RHO*nrow)
	return sthresh(a,k)	
	
def get_xu(x,u,z,l_rob,Q,Atb):
	xu = np.zeros([2,g.DD,1])
	sum = np.zeros([g.DD,1])
	for ip in l_rob:
		u[ip]=u[ip]+x-z[ip]
		sum = sum + z[ip] - u[ip]
	x = Q.dot(Atb + g.RHO * sum)
	xu = [x, u[ip]]
	return x,u,xu

