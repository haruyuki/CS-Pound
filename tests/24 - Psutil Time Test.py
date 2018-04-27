import timeit

s = '''\
import psutil
psutil.time.time()'''

t = '''\
import time
time.time()'''

print(timeit.timeit(stmt=s,number=100000))
print(timeit.timeit(stmt=t,number=100000))  # FASTER