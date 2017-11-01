import struct
import random
import numpy as np

DD = 2
#max double number（本来应该是1.7976931348623157e+308，但有问题，不妨设为1.7976931348622e+308） 
MAXDOUBLE = 1.7976931348622e+308
#max double number in packed type
PMD = struct.pack('%ud'%DD, *([MAXDOUBLE]*DD))


Xk = np.random.random(DD)
rec=DD*Xk.itemsize


print('type(MAXDOUBLE)=',type(MAXDOUBLE))
print('PMD=',PMD)
print('struct.calcsize(PMD)=',struct.calcsize('%ud'%DD))
print('Xk=',Xk)
print('rec=', rec)