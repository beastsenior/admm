# import tkinter
# import matplotlib.pyplot as plt

# plt.bar(left = (0,1),height = (1,0.5),width = 0.35)
# plt.show()
import numpy as np
DD=5
l_ob = [\
'172.16.100.2',    \
'172.16.100.7',  '172.16.100.8',  '172.16.100.9',  '172.16.100.10', '172.16.100.11', \
'172.16.100.12', '172.16.100.13', '172.16.100.14', '172.16.100.15', '172.16.100.16', \
'172.16.100.17']
print(l_ob[1])

u = {}
for ip in l_ob:
	u[ip]=np.zeros([DD,1])
z = {}
for ip in l_ob:
	z[ip]=np.zeros([DD,1])
x = np.zeros([DD,1])

for ip in l_ob:
    u[ip] = u[ip] + x - z[ip]

print(u)
print(u[l_ob[1]])