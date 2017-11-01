import topology as to
import pymysql

#connect to mysql
conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
cursor = conn.cursor()

tmp_mask={}
#creat star network mask
for i in to.IPLIST:
	for j in to.IPLIST:
		if i == '172.16.100.2':
			tmp_mask[(i,j)]=1
		else:
			tmp_mask[(i,j)]=-1

to.save_mask(tmp_mask, conn, cursor)
for i in to.IPLIST:
	for j in to.IPLIST:
		print(i, '-->', j, tmp_mask[(i,j)])
print('\n\n')

#close mysql connection
cursor.close()
conn.close()
