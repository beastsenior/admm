import networkx as nx
import database as db
import globle as g
import numpy as np

#create topology
def topology():
	G = nx.gnp_random_graph(g.NW, g.POC, seed=g.SEED)
	nx.relabel_nodes(G, g.D_IP, False)
	for edge in G.edges():
		G.edges[edge]['weight'] = np.random.rand()
		G.edges[edge]['b2w'] = True  #bridge to worker
	G = G.to_directed()
	db.save({'G':G})
	print('Create topology...done!')