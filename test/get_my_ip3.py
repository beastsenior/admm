import netifaces

def get_local_ipaddr(interface_name): 
     info = netifaces.ifaddresses(interface_name) 
     return info[netifaces.AF_INET][0]['addr'] 
  
if __name__ == '__main__': 
     print(get_local_ipaddr('eth0'))
