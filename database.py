import pymysql

try:
	#connect to mysql database
	conn = pymysql.connect(host='172.16.100.1', port=3306, user='nodes', passwd='172.nodes', db='admm')
	cursor = conn.cursor()
	
	def save(data,name,ip='172.16.100.1'):
		if name not in g.DND:
			print('Error: name not in g.DND.')
			inpurt()

	def load(name,ip='172.16.100.1'):
		if name not in g.DND:
			print('Error: name not in g.DND.')
			inpurt()
		return 0
	

finally:
	cursor.close()
	conn.close()