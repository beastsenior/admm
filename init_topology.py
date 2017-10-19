import topology as to

#creat topology file with random
tmp_to = to.rand_topology()
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, tmp_to[(i,j)])
print('\n\n')
to.save_topology(tmp_to)


