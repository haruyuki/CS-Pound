import timeit

s = '''\
x="17:24:50n"
y=x[:-1]'''

t = '''\
x="17:24:50n"
y=x.replace("n","")'''

print(timeit.timeit(stmt=s,number=100000))  # FASTER
print(timeit.timeit(stmt=t,number=100000))