import numpy as np
import cvxpy as cvx

import globle as g
import database as db

#create data and save data to database
def data(problem):
	
	#lasso
	if problem == 'L':   
		#create
		x0 = np.zeros([g.DD,1])
		num_non_zeros = int(g.PNZ * g.DD)
		positions = np.random.randint(0, g.DD, num_non_zeros)
		for i in positions:
			#x[i] = np.random.random()* (1.0e+7)
			x0[i] = np.random.random()
		A = np.random.normal(0.0, 1.0, [g.NW*g.ND, g.DD])
		b = A.dot(x0) + np.random.normal(0.0, 0.01, [g.NW*g.ND,1])
		#b = A.dot(x)
		
		#compute theta*|x0|_1
		NORMx0 = g.THETA * np.linalg.norm(x0, ord=1)
		#compute min by cvx
		w = cvx.Variable(g.DD)
		objective = cvx.Minimize(0.5*cvx.sum_squares(A*w - b)+ g.THETA*cvx.norm(w,1))
		prob = cvx.Problem(objective)
		CVXmin = prob.solve()
		
		#save to database
		db.save({'NORMx0':NORMx0,'CVXmin':CVXmin,'x0':x0,'A':A,'b':b})

		print('Create data...done!')
		print('Non zeros positions in x0:',positions,'\n')
