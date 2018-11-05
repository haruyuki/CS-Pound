from datetime import datetime
import json
import re


with open('counter.json', 'r+') as f:
    data = json.load(f)
    if data['version'] != datetime.today().strftime('%Y.%m%d'):
        data['version'] = datetime.today().strftime('%Y.%m%d')
        data['build'] = 0
    else:
        data['build'] += 1
    new_version = f'{data["version"]}.{data["build"]}'

    g = open('constants.py', 'r')
    lines = g.readlines()
    g.close()

    with open('constants.py', 'w') as g:
        version = re.findall(r'\d{1,4}\.\d{1,4}\.\d{1,3}', lines[9])
        if version:
            lines[9] = lines[9].replace(version[0], new_version)
        for line in lines:
            g.write(line)

    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
