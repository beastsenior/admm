#node as client (bridge)

import userdefine as ud
import socket
import struct

import types #临时

address = ('172.16.100.1', ud.PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

num=0.0
while True:
	num = num+1.0
	#print(type(num))
	msg=struct.pack('d',num)

	s.sendto(msg, address)

s.close()