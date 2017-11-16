#import pymysql
import networkx as nx
import numpy as np

import globle as g

#try:
	#connect to mysql database
	# conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
	# cursor = conn.cursor()
	
def save(d_data, mode='o', ip='172.16.100.1', problem='L'):
	for name in d_data:
		if name == 'G':
			nx.write_gpickle(d_data[name], g.DATA_DIR+str(name)+'_'+mode+'_'+ip+'_'+problem)
		else:
			np.save(g.DATA_DIR+str(name)+'_'+mode+'_'+ip+'_'+problem, d_data[name])

def load(l_data, mode='o', ip='172.16.100.1', problem='L'):
	l_return = []
	for name in l_data:
		if name == 'G':
			l_return.append(nx.read_gpickle(g.DATA_DIR+'G'+'_'+mode+'_'+ip+'_'+problem))
		else:
			l_return.append(np.load(g.DATA_DIR+str(name)+'_'+mode+'_'+ip+'_'+problem+'.npy'))
	return l_return
	
#finally:
	# cursor.close()
	# conn.close()