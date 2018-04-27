import timeit

s = '''\
x = ['Mem:', '1016056', '167088', '163396', '10916', '685572', '671148']
y=x[-1]'''

t = '''\
x = ['Mem:', '1016056', '167088', '163396', '10916', '685572', '671148']
y=x[6]'''

print(timeit.timeit(stmt=s,number=100000))
print(timeit.timeit(stmt=t,number=100000))  # FASTER