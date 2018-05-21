import timeit

pre = '''
import subprocess
import hashlib

'''


s = '''\
a = subprocess.Popen("cut -f4 -d' ' ../autoremind.txt | sort -u", shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")[:-1].split("\\n")'''

t = '''\
hashlib.md5(open('../autoremind.txt').read().encode()).hexdigest()'''

print(timeit.timeit(stmt=s, setup=pre, number=100))
print(timeit.timeit(stmt=t, setup=pre, number=100))
# HASH WINS!

'''
0.7845641640014946
0.00562750899916864

0.758089586001006
0.005485953002789756

0.7964948619992356
0.006987447999563301
'''