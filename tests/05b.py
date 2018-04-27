from subprocess import call
call(['scrapy', 'runspider', 'test5.py', '-o', 'quotes.json'])
print('done')