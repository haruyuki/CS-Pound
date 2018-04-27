import timeit

s = '''\
import os
import psutil
psutil.Process(os.getpid()).memory_info().rss'''

t = '''\
import os
import psutil
psutil.Process(os.getpid()).memory_info()[0]'''

print(timeit.timeit(stmt=s,number=100000))
print(timeit.timeit(stmt=t,number=100000))  # FASTER