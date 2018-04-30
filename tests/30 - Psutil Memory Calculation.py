import timeit

pre='''import psutil'''

s ='''\
psutil.virtual_memory()[3] >> 20'''

t='''\
psutil.virtual_memory()[3] / 1000 / 1024'''

print(timeit.timeit(stmt=s, setup=pre, number=100000))
print(timeit.timeit(stmt=t, setup=pre, number=100000))  # FASTER

'''
1.0822654129997318
1.0822541570000794

1.200169280999944
1.1694283349997932

1.1262349870003163
1.1195576579998487

1.2149633290000565
1.2048704229996474