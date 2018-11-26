from datetime import datetime
import json
import re
import sys


def write_update():
    new_version = f'{data["version"]}.{data["build"]}'

    g = open('constants.py', 'r')
    lines = g.readlines()
    g.close()

    with open('constants.py', 'w') as g:
        version = re.findall(r'\d{1,4}\.\d{1,4}\.\d{1,3}', lines[10])
        if version:
            lines[10] = lines[10].replace(version[0], new_version)
        for line in lines:
            g.write(line)

    f.seek(0)
    json.dump(data, f, indent=2)


if sys.argv[1] == 'startup':
    with open('counter.json', 'r+') as f:
        data = json.load(f)

        if data['version'] != datetime.today().strftime('%Y.%m%d'):
            data['version'] = datetime.today().strftime('%Y.%m%d')
            data['build'] = 0
        write_update()
        f.truncate()

if sys.argv[1] == 'update':
    with open('counter.json', 'r+') as f:
        data = json.load(f)
        data['build'] += 1
        write_update()
        f.truncate()
