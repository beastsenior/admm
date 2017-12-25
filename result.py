import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import database as db

def get_ac(Lmin,CVXmin):
	ac = np.zeros([g.ITER])
	for k in range(g.ITER):
		ac[k]=abs(Lmin[k]-CVXmin)/CVXmin
	return ac

def result(problem):
	print('Result:')
	if problem == 'Lasso':
		NORMx0, CVXmin = db.load(['NORMx0','CVXmin'])
		print('NORMx0=',NORMx0)		
		print('CVXmin=',CVXmin)	

		fig=plt.figure()
		axes = plt.subplot(111)
		axes.cla()
		plt.ylim(1.0e-16, 1.0e+16)
		plt.yscale('log')
		plt.xlim(-5, g.ITER)
			
		lineX = np.linspace(0, g.ITER, g.ITER)	
		
		d_Lmin = {}
		d_ac = {}
		for mode_i in range(len(g.L_MODE)):
			d_Lmin[mode_i], = db.load(['Lmin'], mode_i)  
			d_ac[mode_i] = get_ac(d_Lmin[mode_i], CVXmin)
			print('mode_i=',mode_i)
			print(d_Lmin[mode_i][g.ITER-1])
			print(ac[mode_i][g.ITER-1])
			plt.plot(lineX, d_ac[mode_i], label=str(mode_i))	
			
		plt.legend()
		plt.show()
