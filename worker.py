import socket
import netifaces
import userdefine
	 
ip=get_ip('eth1')
address = (ip, PORT)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  
  
while True:  
    data, addr = s.recvfrom(1024)  
    if not data:  
        print "client has exist"  
        break  
    print "received:", data, "from", addr  
  
s.close()  