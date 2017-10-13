import topology as to

#creat topology
tmp_to = to.rand_topology()
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, tmp_to[(i,j)])
print('\n\n')
to.save_topology(tmp_to)
adjacency_matrix = to.load_topology()
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, adjacency_matrix[(i,j)])
print('\n\n')

topology_mask = to.get_full_mask(adjacency_matrix)
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, topology_mask[(i,j)])
print('\n\n')
to.save_mask(topology_mask)
topology_mask = to.load_mask()
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, topology_mask[(i,j)])
print('\n\n')