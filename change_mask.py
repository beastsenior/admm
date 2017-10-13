import topology as to

from sys import argv

topology_mask = to.load_mask()
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, topology_mask[(i,j)])
print('\n\n')
#######change######
print(argv[1], argv[2], topology_mask[(argv[1],argv[2])])
if topology_mask[(argv[1], argv[2])] == 1:
	topology_mask[(argv[1], argv[2])] = 0
elif topology_mask[(argv[1], argv[2])] == 0:
	topology_mask[(argv[1], argv[2])] = 1
else:
	print('ERROR!!')
print(argv[1], argv[2], topology_mask[(argv[1],argv[2])])
# topology_mask[('172.16.100.8', '172.16.100.10')] = 0
# topology_mask[('172.16.100.10', '172.16.100.8')] = 0
# topology_mask[('172.16.100.8', '172.16.100.9')] = 0
# topology_mask[('172.16.100.9', '172.16.100.8')] = 0
# topology_mask[('172.16.100.8', '172.16.100.6')] = 0
# topology_mask[('172.16.100.6', '172.16.100.8')] = 1
# topology_mask[('172.16.100.8', '172.16.100.8')] = 0

###################
to.save_mask(topology_mask)
