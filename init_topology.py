import topology as to
import pymysql

#creat connected topology by random
tmp_to = to.rand_topology()
while to.is_connected(tmp_to, to.NN) == False:
	tmp_to = to.rand_topology()
#creat full mask by topology 
tmp_mask = to.get_full_mask(tmp_to)

#show topology and mask
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, tmp_to[(i,j)])
print('\n\n')
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, tmp_mask[(i,j)])
print('\n\n')

#save topology and mask to database 
conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
cursor = conn.cursor()
to.save_topology(tmp_to, conn, cursor)
to.save_mask(tmp_mask, conn, cursor)
cursor.close()
conn.close()


