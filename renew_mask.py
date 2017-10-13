import topology as to
import net_interface as ni

#creat topology
tmp_to = to.rand_topology()
for i in ni.IPLIST:
	for j in ni.IPLIST:
		print(i, '-->', j, tmp_to[(i,j)])
print('\n\n')
to.save_topology(tmp_to)
adjacency_matrix = to.load_topology()
for i in ni.IPLIST:
	for j in ni.IPLIST:
		print(i, '-->', j, adjacency_matrix[(i,j)])
print('\n\n')

topology_mask = to.get_full_mask(adjacency_matrix)
for i in ni.IPLIST:
	for j in ni.IPLIST:
		print(i, '-->', j, to.topology_mask[(i,j)])
print('\n\n')
to.save_mask(topology_mask)
topology_mask = to.load_mask()
for i in ni.IPLIST:
	for j in ni.IPLIST:
		print(i, '-->', j, topology_mask[(i,j)])
print('\n\n')