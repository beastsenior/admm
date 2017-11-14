import numpy as np

import globle as g
import database as db

#create data and save data to database
def data(problem):
	np.random.seed(1)
	
	#lasso
	if problem == 'L':   
		#create
		x0 = np.zeros((g.DD, 1))
		num_non_zeros = int(g.PNZ * g.DD)
		positions = np.random.randint(0, g.DD, num_non_zeros)
		print('positions=',positions)
		for i in positions:
			#x[i] = np.random.random()* (1.0e+7)
			x0[i] = np.random.random()
		A = np.random.normal(0.0, 1.0, (g.NW, g.ND, DD))
		b = A.dot(x0) + np.random.normal(0.0, 0.01, (g.NW, g.ND, 1))
		#b = A.dot(x)
		
		#save to database
		db.save(x0,'Lx0')
		db.save(A.reshape(g.NW*g.ND, DD),'LA')
		db.save(b.reshape(g.NW*g.ND, 1),'Lb')
		i=0
		for ip in g.IPLIST:
			db.save(A[i],'LA',ip)
			db.save(b[i],'Lb',ip)
			i+=1
		print('Create and save data...done!')
