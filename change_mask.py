import topology as to
from sys import argv
import pymysql

#connect to mysql
conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
cursor = conn.cursor()

adjacency_mask = to.load_mask(conn, cursor)
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
print('-->')
print(argv[1], argv[2], adjacency_mask[(argv[1],argv[2])])
###################

to.save_mask(adjacency_mask, conn, cursor)

#close mysql connection
cursor.close()
conn.close()