import timeit

pre = '''
import requests
base = 'http://www.chickensmoothie.com/viewpet.php'
data = {'id':'54685939'}
'''


s = '''\
response = requests.post(base, params=data)'''

t = '''\
response = requests.post(base, params=data, headers={'Connection': 'close'})'''

print(timeit.timeit(stmt=s, setup=pre, number=2))
print(timeit.timeit(stmt=t, setup=pre, number=2))
# EVEN!?

'''
1.1658790830042562
1.1322457259957446

1.0622658489955938
1.2627639010024723

1.113664673997846
1.129015510006866

1.2555077569995774
1.2190989630034892
'''