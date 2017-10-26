import topology as to
import pymysql

#connect to mysql
conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
cursor = conn.cursor()

#creat topology file with random
tmp_to = to.rand_topology()
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, tmp_to[(i,j)])
print('\n\n')
to.save_topology(tmp_to, conn, cursor)

#creat mask database with full mask
tmp_mask = to.get_full_mask(tmp_to)
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, tmp_mask[(i,j)])
print('\n\n')
to.save_mask(tmp_mask, conn, cursor)

#close mysql connection
cursor.close()
conn.close()


