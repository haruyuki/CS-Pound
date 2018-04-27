#Discord.py version
discord.__version__

#Server Count
str(len(client.servers))

#Member Count
str(len(set(client.get_all_members())))


server_memory_temp = subprocess.run(['free'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')[1].split()
server_memory = None

server_uptime = subprocess.run(['uptime'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()[2][:-1]