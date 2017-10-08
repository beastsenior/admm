import socket
import userdefine

address = ('172.16.100.1', PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	msg = 'hello'
	if not msg:
		break
	s.sendto(msg, address)

s.close()