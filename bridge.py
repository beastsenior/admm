#node as client (bridge)

import userdefine as ud
import socket
import struct

address = ('172.16.100.1', ud.PORT)
ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

num = 0.0
while True:
	num = num + 1.0
	msg = struct.pack('d',num)

	ser.sendto(msg, address)

ser.close()