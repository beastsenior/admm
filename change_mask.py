import topology as to

from sys import argv

adjacency_mask = to.load_mask()
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, adjacency_mask[(i,j)])
print('\n\n')
#######change######
print(argv[1], argv[2], adjacency_mask[(argv[1],argv[2])])
if adjacency_mask[(argv[1], argv[2])] == 1:
	adjacency_mask[(argv[1], argv[2])] = 0
elif adjacency_mask[(argv[1], argv[2])] == 0:
	adjacency_mask[(argv[1], argv[2])] = 1
else:
	print('ERROR!!')
print(argv[1], argv[2], adjacency_mask[(argv[1],argv[2])])
# adjacency_mask[('172.16.100.8', '172.16.100.10')] = 0
# adjacency_mask[('172.16.100.10', '172.16.100.8')] = 0
# adjacency_mask[('172.16.100.8', '172.16.100.9')] = 0
# adjacency_mask[('172.16.100.9', '172.16.100.8')] = 0
# adjacency_mask[('172.16.100.8', '172.16.100.6')] = 0
# adjacency_mask[('172.16.100.6', '172.16.100.8')] = 1
# adjacency_mask[('172.16.100.8', '172.16.100.8')] = 0

###################
to.save_mask(adjacency_mask)
