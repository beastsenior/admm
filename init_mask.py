import topology as to

#creat topology mask file with full mask
topology_mask = to.get_full_mask(to.load_topology())
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, topology_mask[(i,j)])
print('\n\n')
to.save_mask(topology_mask)
